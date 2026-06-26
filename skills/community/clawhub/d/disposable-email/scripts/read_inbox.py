#!/usr/bin/env python3
import argparse
import json
import re
import time
from urllib import request

API = "https://api.mail.tm"


def http_json(url, token):
    req = request.Request(url=url, method="GET")
    req.add_header("Authorization", f"Bearer {token}")
    with request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def list_messages(token):
    data = http_json(f"{API}/messages", token)
    msgs = data.get("hydra:member", [])
    out = []
    for m in msgs:
        out.append({
            "id": m.get("id"),
            "from": m.get("from", {}).get("address"),
            "subject": m.get("subject"),
            "intro": m.get("intro"),
            "createdAt": m.get("createdAt"),
            "seen": m.get("seen"),
        })
    return out


def get_message(token, message_id):
    m = http_json(f"{API}/messages/{message_id}", token)
    text = m.get("text") or ""
    html = "\n".join(m.get("html") or [])
    return {
        "id": m.get("id"),
        "from": m.get("from", {}).get("address"),
        "subject": m.get("subject"),
        "createdAt": m.get("createdAt"),
        "text": text,
        "html": html,
    }


def extract_otp(content, pattern):
    match = re.search(pattern, content)
    return match.group(1) if match else None


def main():
    p = argparse.ArgumentParser(description="Read Mail.tm inbox and extract OTP")
    p.add_argument("--token", required=True, help="Mail.tm bearer token")
    p.add_argument("--list", action="store_true", help="List inbox messages")
    p.add_argument("--latest", action="store_true", help="Read latest message")
    p.add_argument("--wait-otp", action="store_true", help="Poll inbox until OTP found")
    p.add_argument("--timeout", type=int, default=60, help="Max seconds to wait for OTP")
    p.add_argument("--interval", type=float, default=3, help="Polling interval seconds")
    p.add_argument("--otp-regex", default=r"\b(\d{4,8})\b", help="Regex with capture group for OTP")
    args = p.parse_args()

    if not (args.list or args.latest or args.wait_otp):
        raise SystemExit("Specify one of --list, --latest, --wait-otp")

    if args.list:
        print(json.dumps({"messages": list_messages(args.token)}, ensure_ascii=False))
        return

    if args.latest:
        msgs = list_messages(args.token)
        if not msgs:
            print(json.dumps({"message": None}, ensure_ascii=False))
            return
        print(json.dumps({"message": get_message(args.token, msgs[0]["id"])}, ensure_ascii=False))
        return

    deadline = time.time() + args.timeout
    while time.time() < deadline:
        msgs = list_messages(args.token)
        if msgs:
            detail = get_message(args.token, msgs[0]["id"])
            content = (detail.get("text") or "") + "\n" + (detail.get("html") or "")
            otp = extract_otp(content, args.otp_regex)
            if otp:
                print(json.dumps({"otp": otp, "message": detail}, ensure_ascii=False))
                return
        time.sleep(args.interval)

    print(json.dumps({"otp": None, "message": "timeout"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
