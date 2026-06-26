#!/usr/bin/env python3
import argparse
import json
import os
import random
import re
import string
import time
from urllib import request

API = "https://api.mail.tm"

WORDS = [
    "amber", "apple", "aqua", "bamboo", "berry", "blue", "brisk", "cedar", "cherry", "cloud",
    "coral", "cosmic", "dawn", "delta", "ember", "forest", "frost", "gold", "harbor", "hazel",
    "indigo", "ivory", "jade", "jolly", "lemon", "lotus", "lunar", "maple", "mist", "moss",
    "nova", "ocean", "olive", "opal", "pearl", "pine", "plum", "polar", "raven", "river",
    "rose", "ruby", "sable", "sage", "sky", "solar", "stone", "sunny", "violet", "willow",
]


def http_json(url, method="GET", data=None, headers=None):
    req = request.Request(url=url, method=method)
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    body = None
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        req.add_header("Content-Type", "application/json")
    with request.urlopen(req, body, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def random_local_part():
    word1 = random.choice(WORDS)
    word2 = random.choice(WORDS)
    digits = "".join(random.choices(string.digits, k=4))
    return f"{word1}.{word2}.{digits}"


def create_inbox():
    domains = http_json(f"{API}/domains").get("hydra:member", [])
    if not domains:
        raise RuntimeError("No Mail.tm domains available")

    domain = domains[0]["domain"]
    local = random_local_part()
    requested_address = f"{local}@{domain}"
    password = "Tmp!" + "".join(random.choices(string.ascii_letters + string.digits, k=12))

    account = http_json(f"{API}/accounts", method="POST", data={"address": requested_address, "password": password})
    canonical_address = account.get("address") or requested_address
    token_resp = http_json(f"{API}/token", method="POST", data={"address": canonical_address, "password": password})

    return {
        "address": canonical_address,
        "requestedAddress": requested_address,
        "password": password,
        "token": token_resp.get("token"),
        "accountId": account.get("id"),
        "domain": domain,
    }


def list_messages(token):
    data = http_json(f"{API}/messages", headers={"Authorization": f"Bearer {token}"})
    return data.get("hydra:member", [])


def get_message(token, message_id):
    m = http_json(f"{API}/messages/{message_id}", headers={"Authorization": f"Bearer {token}"})
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


def main():
    p = argparse.ArgumentParser(description="Create Mail.tm inbox and wait for OTP")
    p.add_argument("--timeout", type=int, default=120, help="Max seconds to wait for OTP")
    p.add_argument("--interval", type=float, default=3, help="Polling interval seconds")
    p.add_argument("--otp-regex", default=r"\b(\d{4,8})\b", help="Regex with capture group for OTP")
    p.add_argument("--save", help="Optional path to save final JSON result")
    args = p.parse_args()

    def emit(payload, flush=False):
        print(json.dumps(payload, ensure_ascii=False), flush=flush)
        if args.save:
            out_dir = os.path.dirname(os.path.abspath(args.save))
            os.makedirs(out_dir, exist_ok=True)
            with open(args.save, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)

    inbox = create_inbox()
    emit({"event": "inbox_created", **inbox}, flush=True)

    deadline = time.time() + args.timeout
    while time.time() < deadline:
        msgs = list_messages(inbox["token"])
        if msgs:
            detail = get_message(inbox["token"], msgs[0]["id"])
            content = (detail.get("text") or "") + "\n" + (detail.get("html") or "")
            match = re.search(args.otp_regex, content)
            if match:
                emit({"event": "otp_found", "otp": match.group(1), "message": detail, "inbox": inbox})
                return
            emit({"event": "message_received_no_otp", "message": detail, "inbox": inbox})
            return
        time.sleep(args.interval)

    emit({"event": "timeout", "inbox": inbox})


if __name__ == "__main__":
    main()
