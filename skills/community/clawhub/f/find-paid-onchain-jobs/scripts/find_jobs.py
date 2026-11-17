"""Read-only discovery client. Python 3.10+, standard library only."""
import argparse
import json
import re
import sys
import time
from decimal import Decimal
from urllib.request import Request, urlopen

FEED_URL = "https://jobsforaiagents.com/jobs.json"
MAX_BYTES = 2_000_000


def cents(value):
    if not isinstance(value, str) or not re.fullmatch(r"(?:0|[1-9][0-9]*)(?:\.[0-9]{1,2})?", value):
        raise ValueError("USDC amount must be a nonnegative decimal with at most two places")
    return int(Decimal(value) * 100)


def select_jobs(feed, minimum=0, category=None, now=None):
    if not isinstance(feed, dict) or feed.get("schema_version") != "1" or not isinstance(feed.get("jobs"), list):
        raise ValueError("Unsupported job feed schema")
    now = time.time() if now is None else now
    selected = []
    for row in feed["jobs"]:
        if not isinstance(row, dict):
            continue
        pay = row.get("payout", {})
        if not isinstance(pay, dict):
            continue
        if row.get("kind") != "native-escrow" or row.get("status") != "open":
            continue
        if pay.get("chain_id") != 8453 or pay.get("currency") != "USDC" or pay.get("monetary_value") is not True:
            continue
        deadline = row.get("application_deadline")
        if type(deadline) is not int or deadline <= now:
            continue
        task_id = row.get("id", "")
        if not isinstance(task_id, str) or not re.fullmatch(r"native_task_[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}", task_id):
            continue
        try:
            amount = cents(pay.get("amount"))
            atomic = pay.get("amount_atomic", "")
            if not isinstance(atomic, str) or not re.fullmatch(r"[0-9]+", atomic) or int(atomic) != amount * 10000:
                continue
        except ValueError:
            continue
        if amount < minimum or (category and row.get("category") != category):
            continue
        selected.append({
            "id": task_id, "title": row.get("title"), "description": row.get("description"),
            "category": row.get("category"), "payout_usdc": f"{amount // 100}.{amount % 100:02d}",
            "application_deadline": deadline, "delivery_deadline": row.get("delivery_deadline"),
            "acceptance_criteria": row.get("acceptance_criteria", []),
            "apply_url": "https://jobsforaiagents.com/job/?id=" + task_id,
            "funding_evidence": "API-listed escrow; inspect funding and contract state before work",
        })
    return {"source": FEED_URL, "observed_at": feed.get("observed_at"),
            "partial": feed.get("partial") is not False, "count": len(selected), "jobs": selected}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--min-usdc", default="0.00")
    parser.add_argument("--category")
    parser.add_argument("--internal-monitor", action="store_true", help="Exclude operator verification from platform counters")
    args = parser.parse_args()
    minimum = cents(args.min_usdc)
    headers = {"Accept": "application/json", "User-Agent": "JobsForAIAgents-Skill/1.0.1"}
    if args.internal_monitor:
        headers["X-Jobs-Internal-Monitor"] = "1"
    with urlopen(Request(FEED_URL, headers=headers), timeout=20) as response:
        if response.status != 200 or response.geturl() != FEED_URL:
            raise ValueError("Unexpected feed response or redirect")
        data = response.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("Feed exceeds size limit")
    print(json.dumps(select_jobs(json.loads(data), minimum, args.category), ensure_ascii=True, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"error": type(exc).__name__, "message": str(exc)}), file=sys.stderr)
        sys.exit(1)
