"""
Airdrop Monitor CN - practical runnable entry

Usage:
  python app.py --config config.example.json
  python app.py --config config.example.json --channel discord --raw-user-id 12345

If billing env is configured, it charges before running monitor.
"""

import argparse
import json
import os
from typing import Dict, Any

from billing import BillingConfigError, charge_user
from monitor import format_markdown_report, run_monitor


def resolve_user_id(channel: str, raw_user_id: str) -> str:
    return f"{channel}_{raw_user_id}"


def maybe_charge(channel: str, raw_user_id: str) -> Dict[str, Any]:
    if not (os.environ.get("SKILL_BILLING_API_KEY") and os.environ.get("SKILL_ID")):
        return {"ok": True, "message": "billing disabled"}

    uid = resolve_user_id(channel, raw_user_id)
    amount_raw = os.environ.get("SKILL_PRICE_USDT")
    amount = float(amount_raw) if amount_raw else None
    try:
        return charge_user(uid, amount=amount)
    except BillingConfigError as e:
        return {"ok": False, "message": str(e)}
    except Exception as e:
        return {"ok": False, "message": f"billing error: {e}"}


def handle_request(config_path: str, channel: str, raw_user_id: str) -> Dict[str, Any]:
    charge = maybe_charge(channel, raw_user_id)
    if not charge.get("ok"):
        return {
            "ok": False,
            "type": "payment_required",
            "message": "余额不足或计费异常，请充值后重试。",
            "payment_url": charge.get("payment_url"),
            "balance": charge.get("balance", 0),
            "reason": charge.get("message"),
        }

    data = run_monitor(config_path=config_path)
    return {
        "ok": True,
        "type": "result",
        "balance": charge.get("balance"),
        "data": data,
        "markdown": format_markdown_report(data),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to monitor config JSON")
    parser.add_argument("--channel", default="local")
    parser.add_argument("--raw-user-id", default="demo")
    parser.add_argument("--json", action="store_true", help="Print full JSON output")
    args = parser.parse_args()

    result = handle_request(args.config, args.channel, args.raw_user_id)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if result.get("ok"):
        print(result["markdown"])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
