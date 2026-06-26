#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from datetime import datetime
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(description="Update buyma last_state.json")
    parser.add_argument("--state", required=True)
    parser.add_argument("--last-order-number", type=int, required=True)
    parser.add_argument("--last-file", required=True)
    parser.add_argument("--last-mail-status", required=True)
    parser.add_argument("--last-mode", required=True)
    parser.add_argument("--last-start-order", type=int, required=True)
    parser.add_argument("--last-end-order", type=int, required=True)
    args = parser.parse_args()

    state = {
        "last_order_number": args.last_order_number,
        "last_run_date": datetime.now().strftime("%Y-%m-%d"),
        "last_file": args.last_file,
        "last_mail_status": args.last_mail_status,
        "last_mode": args.last_mode,
        "last_start_order": args.last_start_order,
        "last_end_order": args.last_end_order,
    }
    path = Path(args.state).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(state, ensure_ascii=False))


if __name__ == "__main__":
    main()
