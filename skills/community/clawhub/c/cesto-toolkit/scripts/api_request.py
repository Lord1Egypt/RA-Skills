#!/usr/bin/env python3
"""
Make an authenticated Cesto API call. Reads session data internally
and prints only the response body. No sensitive values are exposed.

The URL is validated against an allowlist to prevent session keys
from being sent to unauthorized domains.

Usage:
  python3 api_request.py <METHOD> <URL> [JSON_BODY]

Examples:
  python3 api_request.py GET https://backend.cesto.co/tokens
  python3 api_request.py POST https://backend.cesto.co/labs/posts '{"title":"My Basket",...}'
"""

import sys

sys.dont_write_bytecode = True
import json, urllib.request
from _store import read_session, ACCESS_KEY

ALLOWED_ORIGINS = [
    "https://backend.cesto.co",
]

url = sys.argv[2] if len(sys.argv) > 2 else ""

if not any(url.startswith(origin) for origin in ALLOWED_ORIGINS):
    print(
        json.dumps(
            {
                "error": True,
                "status": 403,
                "message": f"Blocked: URL must start with one of {ALLOWED_ORIGINS}",
            }
        )
    )
    sys.exit(1)

_session = read_session()
if _session is None:
    print(
        json.dumps({"error": True, "status": 401, "message": "No valid session found"})
    )
    sys.exit(1)

_key = _session[ACCESS_KEY]

method = sys.argv[1]
body = sys.argv[3].encode() if len(sys.argv) > 3 else None

req = urllib.request.Request(url, data=body, method=method)
_h = "Authorization"
req.add_header(_h, f"Bearer {_key}")
if body:
    req.add_header("Content-Type", "application/json")

try:
    resp = urllib.request.urlopen(req)
    print(resp.read().decode())
except urllib.error.HTTPError as e:
    print(json.dumps({"error": True, "status": e.code, "message": e.read().decode()}))
    sys.exit(1)
