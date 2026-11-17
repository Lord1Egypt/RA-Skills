#!/usr/bin/env python3
"""
webhook_publish.py - Outbound signed webhook (BidHunter v3.0, zero-cloud subset).

Pushes matched bid items to a user-configured external URL (your own CRM/ERP/
automation), with HMAC-SHA256 signature for integrity. This is the local
"开放能力" replacement for the cloud webhook marketplace — no paid infra.

Config (~/.config/bidhunter/webhook.json):
  {"url": "https://your-server/hook", "secret": "your-shared-secret"}

Usage:
  python3 webhook_publish.py <qual_file.jsonl>     # push investable items
  python3 webhook_publish.py --test                # send one ping
"""
import os
import sys
import json
import hmac
import hashlib
import urllib.request
import urllib.error
from datetime import datetime

CFG = os.path.expanduser("~/.config/bidhunter/webhook.json")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def load_cfg():
    if not os.path.exists(CFG):
        raise SystemExit(f"未配置 webhook：请创建 {CFG} = "
                          f'{{"url":"...","secret":"..."}}')
    with open(CFG, "r", encoding="utf-8") as f:
        return json.load(f)


def sign(secret, body):
    return hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()


def push(url, secret, payload):
    body = json.dumps(payload, ensure_ascii=False)
    sig = sign(secret, body)
    req = urllib.request.Request(url, data=body.encode("utf-8"), method="POST",
                                 headers={"Content-Type": "application/json",
                                           "X-BidHunter-Sig": sig})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.status


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        cfg = load_cfg()
        st = push(cfg["url"], cfg["secret"],
                  {"type": "ping", "ts": datetime.now().isoformat()})
        print(f"test push -> HTTP {st}")
        return
    if len(sys.argv) < 2:
        print("Usage: python3 webhook_publish.py <qual_file.jsonl> [--test]", file=sys.stderr)
        sys.exit(1)
    cfg = load_cfg()
    items = []
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            if d.get("verdict") in ("investable", "needs_review"):
                items.append(d)
    if not items:
        print("无可推送项。")
        return
    st = push(cfg["url"], cfg["secret"], {"type": "bids", "count": len(items), "items": items})
    print(f"已推送 {len(items)} 条 → HTTP {st}")


if __name__ == "__main__":
    main()
