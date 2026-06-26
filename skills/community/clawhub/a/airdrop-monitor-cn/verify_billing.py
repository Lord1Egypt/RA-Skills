"""Quick billing integration check.

Usage:
  export SKILL_BILLING_API_KEY=...
  export SKILL_ID=39bf8448-ceba-4764-8f73-b58ed00e4f57
  python verify_billing.py --user-id test_123 --amount 0.001
"""

import argparse
import json

from billing import charge_user, get_balance, get_payment_link


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--user-id", required=True)
    p.add_argument("--amount", type=float, default=0.001)
    args = p.parse_args()

    out = {}
    try:
        out["balance"] = get_balance(args.user_id)
    except Exception as e:
        out["balance_error"] = str(e)

    try:
        out["charge"] = charge_user(args.user_id, amount=args.amount)
    except Exception as e:
        out["charge_error"] = str(e)

    try:
        out["payment_link"] = get_payment_link(args.user_id, amount=8)
    except Exception as e:
        out["payment_link_error"] = str(e)

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
