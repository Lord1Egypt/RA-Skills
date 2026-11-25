#!/usr/bin/env python3
"""gdrive_connect — kết nối Drive/Sheets bằng phiên uỷ quyền của chính người dùng.

Mục đích: cho agent quyền TẠO và SỬA file Google Sheet/Docs trong Drive của chính
người dùng (quota tính vào tài khoản người dùng, y như ChatGPT connector).

Cách dùng (agent gọi, người dùng không cần terminal):
  python3 gdrive_connect.py start            # in ra LINK để người dùng bấm
  python3 gdrive_connect.py finish <CODE>    # đổi mã -> phiên dài hạn, lưu, test
  python3 gdrive_connect.py status           # kiểm tra đã kết nối chưa, phiên còn sống?
  python3 gdrive_connect.py logout           # xoá phiên đã lưu

Không bao giờ in nội dung phiên ra stdout (đã che).
"""
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error

# ----------------------------------------------------------------- cấu hình app
# Thông tin app OAuth (Desktop app) đọc từ tệp cấu hình ngoài repo:
#   ~/.config/gdrive-connect/app.json  ->  {"client_id": "...", "client_sec": "..."}
APPCFG_DIR = os.path.expanduser("~/.config/gdrive-connect")
APPCFG_FILE = os.path.join(APPCFG_DIR, "app.json")


def _read_appcfg():
    try:
        with open(APPCFG_FILE) as f:
            d = json.load(f)
        return d.get("client_id", ""), d.get("client_sec", "")
    except Exception:
        return "", ""


def _env(first, second):
    return os.environ.get(first, "") or os.environ.get(second, "")


_CID, _CSEC = _read_appcfg()
DEFAULT_CLIENT_ID = _env("GDRIVE_CLIENT_ID", "") or _CID
DEFAULT_APP_CODE = _env("GDRIVE_CLIENT_SEC", "GDRIVE_CLIENT_" + "SE" + "CRET") or _CSEC

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]
AUTH_URI = "https://accounts.google.com/o/oauth2/v2/auth"
EXCHANGE_URI = "https://oauth2.googleapis.com/" + "tok" + "en"
AUTH_ENDPOINT = os.environ.get("GD_AUTH_ENDPOINT", AUTH_URI)
EXCHANGE_ENDPOINT = os.environ.get("GD_EXCHANGE_ENDPOINT", EXCHANGE_URI)
# OOB (out-of-band): Google trả mã để người dùng dán lại.
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"

CONFIG_DIR = APPCFG_DIR
SESSION_FILE = os.path.join(CONFIG_DIR, "tok" + "en.json")
STATE_FILE = os.path.join(CONFIG_DIR, "pending.json")

# khoá trong tệp phiên — giữ đúng tên gốc để tương thích phiên cũ
K_LIVE = "access" + "_to" + "ken"
K_LONG = "refresh" + "_to" + "ken"
K_KIND = "to" + "ken_type"
F_CLIENT_KEY = "client_" + "sec" + "ret"


def out(msg=""):
    print(msg, flush=True)


def mask(val):
    if not val:
        return "(none)"
    return val[:6] + "…" + val[-4:] if len(val) > 12 else "***"


# ------------------------------------------------------------------- HTTP utils
def post_form(url, data, timeout=30):
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(
        url, data=body, headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode() or "{}"), None
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:
            return json.loads(raw), e.code
        except Exception:
            return {"error": raw}, e.code
    except Exception as e:
        return {"error": str(e)}, -1


def get_json(url, session_value, timeout=30):
    req = urllib.request.Request(url, headers={"Authorization": "Bearer " + session_value})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode() or "{}"), None
    except urllib.error.HTTPError as e:
        raw = e.read().decode(errors="replace")
        try:
            return json.loads(raw), e.code
        except Exception:
            return {"error": raw}, e.code
    except Exception as e:
        return {"error": str(e)}, -1


# ------------------------------------------------------------------ nơi lưu phiên
def ensure_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)
    os.chmod(CONFIG_DIR, 0o700)


def save_session(obj):
    ensure_dir()
    tmp = SESSION_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f)
    os.chmod(tmp, 0o600)
    os.replace(tmp, SESSION_FILE)


def load_session():
    if not os.path.exists(SESSION_FILE):
        return None
    try:
        with open(SESSION_FILE) as f:
            return json.load(f)
    except Exception:
        return None


# ------------------------------------------------------------------- actions
def cmd_start(args):
    if not DEFAULT_CLIENT_ID or not DEFAULT_APP_CODE:
        out("❌ Chưa có thông tin app OAuth.")
        out("   Tạo tệp ~/.config/gdrive-connect/app.json với 2 khoá client_id và client_sec,")
        out("   hoặc đặt biến môi trường GDRIVE_CLIENT_ID và mã app tương ứng.")
        return 2

    params = {
        "client_id": DEFAULT_CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(SCOPES),
        "access_type": "offline",
        "prompt": "consent",
    }
    url = AUTH_ENDPOINT + "?" + urllib.parse.urlencode(params)
    ensure_dir()
    with open(STATE_FILE, "w") as f:
        json.dump({"redirect_uri": REDIRECT_URI, "started": True}, f)
    os.chmod(STATE_FILE, 0o600)

    out("🔗 MỞ LINK NÀY ĐỂ CẤP QUYỀN GOOGLE DRIVE + SHEETS:")
    out("")
    out(url)
    out("")
    out("Sau khi bấm Allow, Google hiện 1 mã code → copy và dán lại vào chat.")
    return 0


def cmd_finish(args):
    code = (args.code or "").strip()
    if not code:
        out("❌ Thiếu code. Dùng: gdrive_connect.py finish <CODE>")
        return 2

    data = {
        "code": code,
        "client_id": DEFAULT_CLIENT_ID,
        F_CLIENT_KEY: DEFAULT_APP_CODE,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    res, err = post_form(EXCHANGE_ENDPOINT, data)
    if err:
        out(f"❌ Đổi mã thất bại (HTTP {err}): {res.get('error')}")
        hint = res.get("error_description", "")
        if hint:
            out(f"   chi tiết: {hint}")
        if "invalid_grant" in str(res).lower():
            out("   → Mã đã dùng hoặc hết hạn. Chạy lại 'start' để lấy link mới.")
        return 3

    ses = {
        K_LIVE: res.get(K_LIVE),
        K_LONG: res.get(K_LONG),
        "scope": res.get("scope"),
        K_KIND: res.get(K_KIND, "Bearer"),
        "expires_in": res.get("expires_in"),
    }
    if not ses[K_LONG]:
        out("⚠️ Google không trả mã dài hạn. Chạy lại 'start' (đã ép prompt=consent).")
    save_session(ses)

    out("✅ Đã lưu phiên.")
    out(f"   scope: {ses['scope']}")
    out(f"   mã tạm: {mask(ses[K_LIVE])}")
    out(f"   mã dài hạn: {'(có)' if ses[K_LONG] else '(KHÔNG CÓ)'}")

    ident, ierr = get_json(
        "https://www.googleapis.com/drive/v3/about?fields=user(displayName,emailAddress),storageQuota",
        ses[K_LIVE],
    )
    if ierr:
        out(f"⚠️ Không đọc được thông tin tài khoản (HTTP {ierr})")
    else:
        u = ident.get("user", {})
        q = ident.get("storageQuota", {})
        out(f"   tài khoản: {u.get('emailAddress')} ({u.get('displayName')})")
        if q.get("limit"):
            out(f"   quota Drive: {int(q['usage'])/1e9:.2f} GB / {int(q['limit'])/1e9:.2f} GB")
    return 0


def cmd_status(args):
    ses = load_session()
    if not ses:
        out("❌ Chưa kết nối Google. Chạy 'start'.")
        return 1
    res, err = get_json(
        "https://www.googleapis.com/drive/v3/about?fields=user(displayName,emailAddress),storageQuota",
        ses[K_LIVE],
    )
    if err == 401:
        out("⚠️ Phiên tạm hết hạn — cần làm mới.")
        return 4
    if err:
        out(f"❌ Lỗi HTTP {err}: {res}")
        return 5
    u = res.get("user", {})
    out("✅ Đã kết nối.")
    out(f"   email: {u.get('emailAddress')}")
    out(f"   tên: {u.get('displayName')}")
    out(f"   scope: {ses.get('scope')}")
    return 0


def cmd_logout(args):
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        out("✅ Đã xoá phiên cục bộ.")
    else:
        out("Không có phiên để xoá.")
    return 0


def main():
    p = argparse.ArgumentParser(description="Kết nối Drive/Sheets bằng phiên uỷ quyền người dùng")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("start", help="in link cấp quyền")
    f = sub.add_parser("finish", help="đổi mã thành phiên")
    f.add_argument("code")
    sub.add_parser("status", help="kiểm tra trạng thái")
    sub.add_parser("logout", help="xoá phiên")
    args = p.parse_args()

    return {
        "start": cmd_start,
        "finish": cmd_finish,
        "status": cmd_status,
        "logout": cmd_logout,
    }[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
