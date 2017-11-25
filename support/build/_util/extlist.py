#!/usr/bin/env python
import os, sys, json, re, datetime
from collections import defaultdict

# iterate over sys.argv
# download each (packages.json)
# extract each heroku-sys-php-extension
# parse out PHP version requirement (e.g. "5.6.*")
# build a dict of extensions and PHP versions (latest versions only)
# build each of these dicts per stack?
# generate HTML

# "packages" key is a list with just one item: another list (of packages)
# read each of these lists, then flatten those lists into one using two "for" statements
extensions = [package for packages in [json.load(open(f))["packages"][0] for f in sys.argv[1:]] for package in packages if package["type"] == "heroku-sys-php-extension"]

extmap = defaultdict(dict)

for extension in extensions:
    if "heroku-sys/cedar" in extension["require"]:
        stack = "cedar-14"
    else:
        stack = "heroku-16"
    # if not extension["name"] in extmap:
    #     extmap[extension["name"]] = {}
    if not extension["require"]["heroku-sys/php"] in extmap[extension["name"]]:
        extmap[extension["name"]][extension["require"]["heroku-sys/php"]] = defaultdict(list)
    # if not stack in extmap[extension["name"]][extension["require"]["heroku-sys/php"]]:
    #     extmap[extension["name"]][extension["require"]["heroku-sys/php"]][stack] = []
    extmap[extension["name"]][extension["require"]["heroku-sys/php"]][stack].append(extension["version"])

json.dump(extmap, sys.stdout)
