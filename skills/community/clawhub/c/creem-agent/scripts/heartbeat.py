#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE_FILE = Path(os.path.expanduser("~/.creem/heartbeat-state.json"))
STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

def run_cli(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return None
        return json.loads(result.stdout)
    except:
        return None

def load_state():
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE) as f:
                data = json.load(f)
                # Ensure all required keys exist
                return {
                    "lastCheckAt": data.get("lastCheckAt"),
                    "lastTransactionId": data.get("lastTransactionId"),
                    "transactionCount": data.get("transactionCount", 0),
                    "customerCount": data.get("customerCount", 0),
                    "subscriptions": data.get("subscriptions", {"active":0,"trialing":0,"past_due":0,"paused":0,"canceled":0,"expired":0,"scheduled_cancel":0}),
                    "knownSubscriptions": data.get("knownSubscriptions", {})
                }
        except:
            pass  # corrupt file → start fresh
    # First run or corrupt state → clean default
    return {
        "lastCheckAt": None,
        "lastTransactionId": None,
        "transactionCount": 0,
        "customerCount": 0,
        "subscriptions": {"active":0,"trialing":0,"past_due":0,"paused":0,"canceled":0,"expired":0,"scheduled_cancel":0},
        "knownSubscriptions": {}
    }

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def main():
    previous = load_state()

    # Fetch current data
    txns = run_cli("creem transactions list --limit 50 --json") or {"items":[]}
    subs = run_cli("creem subscriptions list --json") or {"items":[]}
    customers = run_cli("creem customers list --json") or {"items":[]}

    txs = txns.get("items", []) if isinstance(txns, dict) else[]
    current_subs = subs.get("items", []) if isinstance(subs, dict) else[]
    current_customers = customers.get("items", []) if isinstance(customers, dict) else[]

    # Build current counts
    current_counts = {"active":0,"trialing":0,"past_due":0,"paused":0,"canceled":0,"expired":0,"scheduled_cancel":0}
    current_known = {}
    for s in current_subs:
        status = s.get("status", "unknown")
        if status in current_counts:
            current_counts[status] += 1
        current_known[s.get("id")] = status

    # Detect changes
    alerts = []

    # New transactions
    new_txs =[t for t in txs if not previous["lastTransactionId"] or str(t.get("id")) > str(previous["lastTransactionId"])]
    if new_txs:
        alerts.append(f"📈 {len(new_txs)} new transaction(s) — revenue incoming!")

    # Subscription state changes
    for sid, new_status in current_known.items():
        old_status = previous["knownSubscriptions"].get(sid)
        if old_status and old_status != new_status:
            if new_status == "past_due":
                alerts.append(f"⚠️ Failed payment: {sid} (past_due)")
            if new_status in ("canceled", "scheduled_cancel"):
                alerts.append(f"🚨 Churn detected: {sid} → {new_status}")

    # New customers
    if len(current_customers) > previous["customerCount"]:
        alerts.append(f"👋 {len(current_customers) - previous['customerCount']} new customer(s)")

    # Save new state
    new_state = {
        "lastCheckAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "lastTransactionId": txs[0].get("id") if txs else previous["lastTransactionId"],
        "transactionCount": len(txs),
        "customerCount": len(current_customers),
        "subscriptions": current_counts,
        "knownSubscriptions": current_known
    }
    save_state(new_state)

    # Output for agent
    if alerts:
        print(json.dumps({"alerts": alerts, "changesDetected": True}))
    else:
        print("HEARTBEAT_OK")

if __name__ == "__main__":
    main()