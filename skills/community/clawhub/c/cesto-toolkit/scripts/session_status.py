#!/usr/bin/env python3
"""
Check Cesto session status. Returns JSON with status and wallet address only.
All session handling is internal — no sensitive values are exposed.

Statuses:
  valid     — session is active
  refreshed — session was renewed
  expired   — session expired or file missing, login required
"""

import sys
sys.dont_write_bytecode = True
import json, base64, urllib.request
from datetime import datetime, timezone
from _store import read_session, write_session, ACCESS_KEY, REFRESH_KEY

_data = read_session()

if _data is None:
    print(json.dumps({"status": "expired"}))
    sys.exit(0)

now = datetime.now(timezone.utc)
_exp1 = datetime.fromisoformat(_data[f"{ACCESS_KEY}ExpiresAt"].replace("Z", "+00:00"))
_exp2 = datetime.fromisoformat(_data[f"{REFRESH_KEY}ExpiresAt"].replace("Z", "+00:00"))
wallet = _data.get("walletAddress", "")

if now < _exp1:
    print(json.dumps({"status": "valid", "wallet": wallet}))
elif now < _exp2:
    req = urllib.request.Request(
        "https://backend.cesto.co/auth/refresh",
        data=json.dumps({REFRESH_KEY: _data[REFRESH_KEY]}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        resp = json.loads(urllib.request.urlopen(req).read())
        for k in [ACCESS_KEY, REFRESH_KEY]:
            _data[k] = resp[k]
            p = json.loads(base64.urlsafe_b64decode(resp[k].split(".")[1] + "=="))
            _data[f"{k}ExpiresAt"] = datetime.fromtimestamp(
                p["exp"], tz=timezone.utc
            ).isoformat()
        write_session(_data)
        print(json.dumps({"status": "refreshed", "wallet": wallet}))
    except Exception:
        print(json.dumps({"status": "expired"}))
else:
    print(json.dumps({"status": "expired"}))
