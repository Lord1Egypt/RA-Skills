"""
conftest.py — pytest session setup for depradar-skill tests.

CRITICAL: lib/http.py is named 'http' which shadows stdlib's http package.
When any lib module adds lib/ to sys.path then does 'from http import',
Python loads lib/http.py as sys.modules['http']. lib/http.py then calls
'import urllib.request', which internally does 'import http.client'.
At that point, sys.modules['http'] is lib/http.py (not a package), so
http.client lookup fails.

Fix: pre-load stdlib http, http.client, and urllib.request here, BEFORE
any lib module is imported. Once http.client is in sys.modules, all future
'import http.client' calls return the cached module object without looking
up http as a parent package again — even if sys.modules['http'] later gets
replaced by lib/http.py.

CRITICAL 2: lib modules do 'from schema import X' using sys.path tricks.
If this creates sys.modules['schema'] as a different object from
sys.modules['lib.schema'], isinstance() checks fail because the class
objects differ. Fix: set sys.modules['schema'] = sys.modules['lib.schema']
IMMEDIATELY after importing lib.schema, before importing any other lib
module. Do this for each module sequentially.

CRITICAL 3: lib modules each load http.py via importlib.util, creating
separate module instances. NotFoundError from one module != NotFoundError
from another, so except clauses fail. Fix: pre-load http.py as
sys.modules['_depradar_http'] once here; all modules check that first.
"""
import sys
import os

# Step 1: ensure scripts/ is on sys.path so 'import lib.*' works from test files
_scripts_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "scripts"))
if _scripts_dir not in sys.path:
    sys.path.insert(0, _scripts_dir)

# Step 2: pre-load stdlib http family into sys.modules while lib/ is NOT on sys.path.
# This ensures http, http.client, http.server, http.cookiejar are cached.
import http            # noqa: E402  — stdlib http package
import http.client     # noqa: E402  — used by urllib.request internally
import http.server     # noqa: E402  — warm-up the package namespace
import http.cookiejar  # noqa: E402  — used by urllib
import urllib          # noqa: E402
import urllib.request  # noqa: E402  — the one that does 'import http.client'
import urllib.error    # noqa: E402
import urllib.parse    # noqa: E402

# Step 3: stash references so they can't be garbage-collected even if
# sys.modules['http'] gets replaced later by lib/http.py.
_STDLIB_HTTP        = http
_STDLIB_HTTP_CLIENT = http.client
_STDLIB_URLLIB_REQ  = urllib.request

# Step 4: pre-load lib/http.py ONCE as '_depradar_http' using importlib.util.
# All lib backend modules will check sys.modules['_depradar_http'] before loading.
# This ensures every module shares the SAME exception class objects —
# so 'except NotFoundError' in npm_registry.py catches the same class that
# test files import via 'from lib.http import NotFoundError'.
import importlib.util as _ilu
_http_path = os.path.join(_scripts_dir, "lib", "http.py")
_http_spec = _ilu.spec_from_file_location("_depradar_http", _http_path)
_http_mod_shared = _ilu.module_from_spec(_http_spec)       # type: ignore[arg-type]
sys.modules["_depradar_http"] = _http_mod_shared           # store BEFORE exec
_http_spec.loader.exec_module(_http_mod_shared)             # type: ignore[union-attr]
# Also register as 'lib.http' so tests can do: from lib.http import NotFoundError
sys.modules["lib.http"] = _http_mod_shared

# Step 5: import lib.* modules and alias them under their bare names IMMEDIATELY,
# before importing the next lib module.  This guarantees that when lib/X.py does
# 'from schema import Foo', it finds sys.modules['schema'] == sys.modules['lib.schema']
# and gets the SAME class objects that tests use via 'from lib.schema import Foo'.

import lib.schema         # noqa: E402
sys.modules["schema"] = sys.modules["lib.schema"]          # FORCE, not setdefault

import lib.dates          # noqa: E402
sys.modules["dates"] = sys.modules["lib.dates"]

import lib.semver         # noqa: E402
sys.modules["semver"] = sys.modules["lib.semver"]

import lib.env            # noqa: E402
sys.modules["env"] = sys.modules["lib.env"]

import lib.ui             # noqa: E402
sys.modules["ui"] = sys.modules["lib.ui"]

import lib.cache          # noqa: E402
sys.modules["cache"] = sys.modules["lib.cache"]

import lib.dep_parser     # noqa: E402
sys.modules["dep_parser"] = sys.modules["lib.dep_parser"]

import lib.score          # noqa: E402
sys.modules["score"] = sys.modules["lib.score"]

import lib.render         # noqa: E402
sys.modules["render"] = sys.modules["lib.render"]

import lib.normalize      # noqa: E402
sys.modules["normalize"] = sys.modules["lib.normalize"]

import lib.dedupe         # noqa: E402
sys.modules["dedupe"] = sys.modules["lib.dedupe"]

import lib.changelog_parser   # noqa: E402
sys.modules["changelog_parser"] = sys.modules["lib.changelog_parser"]

import lib.usage_scanner  # noqa: E402
sys.modules["usage_scanner"] = sys.modules["lib.usage_scanner"]

import lib.impact_analyzer    # noqa: E402
sys.modules["impact_analyzer"] = sys.modules["lib.impact_analyzer"]

# Step 6: import all backend modules AFTER aliases are set.
# Their 'from schema import ...' calls will find sys.modules['schema'] == lib.schema.
import lib.npm_registry       # noqa: E402
sys.modules["npm_registry"] = sys.modules["lib.npm_registry"]

import lib.pypi_registry      # noqa: E402
sys.modules["pypi_registry"] = sys.modules["lib.pypi_registry"]

import lib.crates_registry    # noqa: E402
sys.modules["crates_registry"] = sys.modules["lib.crates_registry"]

import lib.maven_registry     # noqa: E402
sys.modules["maven_registry"] = sys.modules["lib.maven_registry"]

import lib.github_releases    # noqa: E402
sys.modules["github_releases"] = sys.modules["lib.github_releases"]

import lib.github_issues      # noqa: E402
sys.modules["github_issues"] = sys.modules["lib.github_issues"]

import lib.stackoverflow      # noqa: E402
sys.modules["stackoverflow"] = sys.modules["lib.stackoverflow"]

import lib.hackernews         # noqa: E402
sys.modules["hackernews"] = sys.modules["lib.hackernews"]

import lib.reddit_sc          # noqa: E402
sys.modules["reddit_sc"] = sys.modules["lib.reddit_sc"]

import lib.twitter_x          # noqa: E402
sys.modules["twitter_x"] = sys.modules["lib.twitter_x"]

import lib.ignores            # noqa: E402
sys.modules["ignores"] = sys.modules["lib.ignores"]

import lib.verbose_log        # noqa: E402
sys.modules["verbose_log"] = sys.modules["lib.verbose_log"]

import lib.notify             # noqa: E402
sys.modules["notify"] = sys.modules["lib.notify"]
