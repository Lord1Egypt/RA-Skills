#!/usr/bin/env python3
"""
B2B Outbound Sniper — Hunter Campaign Manager
Usage:
  python3 scripts/hunter_campaigns.py metrics <campaign_id>
  python3 scripts/hunter_campaigns.py add <campaign_id> <email> <first> <last> <company> <website>

Full source: https://github.com/getlemnos32/b2b-outbound-sniper
"""

import json
import os
import sys
import requests

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "..", "config", "apis.json")

def load_api_key():
    key = os.environ.get("HUNTER_API_KEY", "")
    if not key and os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE) as f:
            key = json.load(f).get("hunter_api_key", "")
    if not key:
        print("ERROR: HUNTER_API_KEY not set. Export it or add to config/apis.json.")
        sys.exit(1)
    return key


def metrics(campaign_id):
    api_key = load_api_key()
    r = requests.get(
        f"https://api.hunter.io/v2/campaigns/{campaign_id}/recipients",
        params={"api_key": api_key, "limit": 100},
        timeout=15,
    )
    data = r.json().get("data", {})
    recipients = data.get("recipients", [])

    sent = [x for x in recipients if x.get("status") == "sent"]
    opened = [x for x in recipients if x.get("opened")]
    replied = [x for x in recipients if x.get("replied")]
    canceled = [x for x in recipients if x.get("status") == "canceled"]
    pending = [x for x in recipients if x.get("status") == "pending"]

    total = len(recipients)
    open_rate = f"{len(opened)/len(sent)*100:.1f}%" if sent else "—"
    reply_rate = f"{len(replied)/len(sent)*100:.1f}%" if sent else "—"

    print(f"\n{'='*80}")
    print(f"Campaign {campaign_id}")
    print(f"{'='*80}")
    print(f"Total: {total} | Sent: {len(sent)} | Opened: {len(opened)} ({open_rate}) | "
          f"Replied: {len(replied)} ({reply_rate}) | Canceled: {len(canceled)} | Pending: {len(pending)}")
    print()

    for r in recipients:
        status = r.get("status", "unknown")
        email = r.get("email", "")
        company = r.get("company", "")
        flag = "🔥" if r.get("opened") else ("❌" if status == "canceled" else "  ")
        print(f"  {flag} {email:<45} {company}")


def add(campaign_id, email, first, last, company, website):
    api_key = load_api_key()
    payload = {
        "emails": [{
            "value": email,
            "first_name": first,
            "last_name": last,
            "company": company,
            "website": website,
        }]
    }
    r = requests.post(
        f"https://api.hunter.io/v2/campaigns/{campaign_id}/recipients",
        params={"api_key": api_key},
        json=payload,
        timeout=15,
    )
    if r.status_code in (200, 201):
        print(f"✅ Added: {first} {last} <{email}> → campaign {campaign_id}")
    else:
        print(f"❌ Failed ({r.status_code}): {r.text[:200]}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    cid = sys.argv[2]

    if cmd == "metrics":
        metrics(cid)
    elif cmd == "add" and len(sys.argv) == 8:
        _, _, campaign_id, email, first, last, company, website = sys.argv
        add(campaign_id, email, first, last, company, website)
    else:
        print(__doc__)
        sys.exit(1)
