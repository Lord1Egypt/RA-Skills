#!/usr/bin/env python3
"""Pure-HTTP client for the CATCH (凯琦) forwarder portal. No browser automation.

CATCH is a company name — an Amazon SEND partnered carrier — not the English
word. The same client shape works for similar forwarder portals; swap BASE and
the endpoint paths.

    python3 catch_api.py login                    # account+password -> token on disk
    python3 catch_api.py token <TOKEN>            # store a token copied from a browser
    python3 catch_api.py status                   # waybill counts by status
    python3 catch_api.py list [keyword]           # waybill list, optionally filtered
    python3 catch_api.py check FBA1... FBA2...    # are these checked in yet?
    python3 catch_api.py upload a.xls b.xls ...   # upload invoices = place the order

Configuration, all via environment (never hardcode credentials):

    CATCH_BASE_URL   portal origin, e.g. https://portal.example.com
    CATCH_USER       account
    CATCH_PASS       password
    CATCH_TOKEN      optional: use this token directly, skip login
    CATCH_VEN_ID     optional: pin the customer id instead of looking it up

Why HTTP and not browser automation
-----------------------------------
The CATCH portal is a SPA whose element ids shift between builds. Driving it by
clicking means re-finding elements every run, and the only way to read the
result is to screenshot a toast. Over HTTP the response is structured JSON:
per-file success flags and the exact rejection reason, which is what you
actually need to fix an invoice.

API conventions
---------------
auth      header `x-token` (in the browser the value is stored under the
          localStorage key `Authorization` — the key name and the header name
          differ, which is easy to get wrong)
paging    rows are at `data.data`, the count at `data.totalCount`
          (not `data.list` / `data.records` / `data.total`)
query     filter waybills with the `waybillNumber` field
upload    multipart field `multipartFiles`, repeatable — several files in one
          request, no zip needed (zipping is a web-UI limitation, not an API one)
          plus exportType=1, venId=<customer id>, isSmart=0
          returns data.voList[]: waybillNumber / checkOrder / returnMsg
          re-uploading the same waybill is an idempotent update, not a duplicate
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import config_dir  # noqa: E402

BASE = os.environ.get("CATCH_BASE_URL", "").rstrip("/")
TOKEN_FILE = config_dir() / "token.json"
COMMON = {"Accept": "application/json, text/plain, */*"}

# The invoice tab posts to batchForecast/import. There is a sibling endpoint
# fbaForecast/import whose permission key is literally "waybill:fbaForecast:import"
# — it looks like the right one and always returns 403. Use batchForecast.
UPLOAD_EP = "/v1/waybill/manage/order/batchForecast/import"


def _base() -> str:
    if not BASE:
        sys.exit("set $CATCH_BASE_URL to the portal origin, e.g. https://portal.example.com")
    return BASE


# ── token ────────────────────────────────────────────────────────────────────
def save_token(token: str):
    TOKEN_FILE.write_text(json.dumps({"token": token, "ts": int(time.time())}))
    try:
        TOKEN_FILE.chmod(0o600)          # no-op on Windows, harmless
    except OSError:
        pass


def load_token() -> str | None:
    if os.environ.get("CATCH_TOKEN"):
        return os.environ["CATCH_TOKEN"]
    if TOKEN_FILE.exists():
        return json.loads(TOKEN_FILE.read_text()).get("token")
    return None


def login() -> str:
    user, password = os.environ.get("CATCH_USER"), os.environ.get("CATCH_PASS")
    if not (user and password):
        sys.exit("set $CATCH_USER and $CATCH_PASS")
    r = _post("/v1/user/login", {"username": user, "password": password}, auth=False)
    token = (r.get("data") or {}).get("token")
    if not token:
        sys.exit(
            f"login failed: {json.dumps(r, ensure_ascii=False)[:300]}\n"
            "If the portal has added a captcha, password login stops working. Sign in\n"
            "with a browser, copy localStorage['Authorization'], and run:\n"
            "    python3 catch_api.py token <TOKEN>")
    save_token(token)
    return token


# ── HTTP ─────────────────────────────────────────────────────────────────────
def _req(method, path, data=None, headers=None, auth=True):
    h = dict(COMMON)
    if auth:
        token = load_token()
        if not token:
            sys.exit("no token — run `python3 catch_api.py login` or set $CATCH_TOKEN")
        h["x-token"] = token
    h.update(headers or {})
    req = urllib.request.Request(_base() + path, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"{method} {path} HTTP {e.code}: {e.read().decode()[:400]}") from None


def _post(path, body, auth=True):
    r = _req("POST", path, json.dumps(body).encode(),
             {"Content-Type": "application/json"}, auth)
    if r.get("code") == 999:
        sys.exit("code 999 (re-login) — the token expired. Run `catch_api.py login`.")
    return r


def _post_multipart(path, files, fields=None):
    """files: [(field_name, filename, bytes), ...] — the same field name repeats."""
    boundary = "----catch" + uuid.uuid4().hex
    buf = bytearray()
    for k, v in (fields or {}).items():
        buf += (f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n').encode()
    for field, filename, blob in files:
        buf += (f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="{field}"; filename="{filename}"\r\n'
                f"Content-Type: application/vnd.ms-excel\r\n\r\n").encode()
        buf += blob + b"\r\n"
    buf += f"--{boundary}--\r\n".encode()
    return _req("POST", path, bytes(buf),
                {"Content-Type": f"multipart/form-data; boundary={boundary}"})


def find_ven_id() -> int:
    """Customer id, required by the upload endpoint (omitting it returns 403)."""
    if os.environ.get("CATCH_VEN_ID"):
        return int(os.environ["CATCH_VEN_ID"])
    items = _post("/v1/company/listItem", {})["data"]
    if len(items) == 1:
        return items[0]["value"]
    listing = "\n".join(f"  {i['value']}  {i.get('label')}" for i in items)
    sys.exit(f"several customers on this account — pin one with $CATCH_VEN_ID:\n{listing}")


# ── commands ─────────────────────────────────────────────────────────────────
def cmd_status():
    for k, v in _post("/v1/waybill/manage/selectStatusCount", {})["data"].items():
        if v:
            print(f"  {k:24} {v}")


def waybills(page_size=50, keyword=None):
    body = {"pageNum": 1, "pageSize": page_size}
    if keyword:
        body["waybillNumber"] = keyword
    d = _post("/v1/waybill/manage/selectList", body)["data"]
    return d.get("data") or [], d.get("totalCount")


def cmd_list(keyword=None):
    rows, total = waybills(keyword=keyword)
    print(f"{total} waybills, showing {len(rows)}")
    for r in rows:
        print(f"  {r.get('waybillNumber', ''):<15}{r.get('systemOrderCode', ''):<18}"
              f"{r.get('channel', ''):<12}{r.get('pieces', '')} pcs  {r.get('statusName', '')}")


def cmd_check(ids):
    rows, _ = waybills(page_size=200)
    found = {r["waybillNumber"]: r for r in rows if r.get("waybillNumber") in set(ids)}
    for i in ids:
        r = found.get(i)
        print(f"  {i:<15}" + (f"{r['systemOrderCode']:<18}{r.get('channel', ''):<12}"
                              f"{r.get('pieces')} pcs  {r.get('statusName')}"
                              if r else "NOT FOUND"))
    print(f"\n{len(found)}/{len(ids)} found")


def cmd_upload(paths):
    paths = [Path(p) for p in paths]
    for p in paths:
        if not p.exists():
            sys.exit(f"{p} does not exist")
        if p.stat().st_size > 1024 * 1024:
            sys.exit(f"{p.name} exceeds the 1MB per-invoice limit")
    if len(paths) > 20:
        sys.exit("at most 20 invoices per batch")

    ven = find_ven_id()
    files = [("multipartFiles", p.name, p.read_bytes()) for p in paths]
    print(f"uploading {len(paths)} file(s), "
          f"{sum(len(f[2]) for f in files) / 1024:.0f} KB, venId={ven}…")

    r = _post_multipart(UPLOAD_EP, files,
                        {"exportType": "1", "venId": str(ven), "isSmart": "0"})
    print(f"code={r.get('code')} msg={r.get('msg')}")

    vo = (r.get("data") or {}).get("voList") or []
    for it in vo:
        print(f"  {it.get('waybillNumber', '?'):<15}{it.get('checkOrder', '?'):<8}"
              f"{it.get('returnMsg') or '-'}")
    if not vo:
        print("  " + json.dumps(r, ensure_ascii=False)[:600])
    return r


COMMANDS = {
    "login":  lambda a: print("token stored in", TOKEN_FILE) if login() else None,
    "token":  lambda a: (save_token(a[0]), print("stored in", TOKEN_FILE)),
    "status": lambda a: cmd_status(),
    "list":   lambda a: cmd_list(a[0] if a else None),
    "check":  lambda a: cmd_check(a),
    "upload": lambda a: cmd_upload(a),
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd not in COMMANDS:
        sys.exit(__doc__)
    COMMANDS[cmd](sys.argv[2:])
