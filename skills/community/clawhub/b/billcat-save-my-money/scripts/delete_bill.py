#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Any

from billcat_api import SKILL_API_URL, post_json


def delete_bill(bill_ids: list[str], timeout: int = 30) -> Any:
    return post_json(
        SKILL_API_URL,
        {
            "action": "delete",
            "param": {
                "billId": ",".join(bill_ids),
            },
        },
        timeout=timeout,
    )


def to_markdown(result: Any) -> str:
    if not isinstance(result, dict):
        return json.dumps(result, ensure_ascii=False, indent=2) + "\n"

    lines: list[str] = []
    code = result.get("code")
    message = result.get("message") or result.get("msg")
    data = result.get("data") if isinstance(result.get("data"), dict) else {}

    if code is not None:
        lines.append(f"- 响应码: {code}")
    if message:
        lines.append(f"- 结果: {message}")
    if data.get("billId"):
        lines.append(f"- 删除账单ID: {data['billId']}")
    if data.get("deletedCount") is not None:
        lines.append(f"- 删除数量: {data['deletedCount']}")

    if not lines:
        return json.dumps(result, ensure_ascii=False, indent=2) + "\n"

    extra = {
        k: v
        for k, v in result.items()
        if k not in {"code", "message", "msg", "data"}
    }
    if extra:
        lines.append("")
        lines.append("附加字段:")
        lines.append("```json")
        lines.append(json.dumps(extra, ensure_ascii=False, indent=2))
        lines.append("```")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Delete bills in BillCat via OpenClaw skill API")
    parser.add_argument("--bill-id", required=True, help="Single bill ID or comma-separated bill IDs")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--format", choices=["raw", "pretty", "md"], default="raw")
    args = parser.parse_args()

    bill_ids = [item.strip() for item in args.bill_id.split(",") if item.strip()]
    if not bill_ids:
        raise SystemExit("Provide at least one valid --bill-id")

    result = delete_bill(bill_ids=bill_ids, timeout=max(1, args.timeout))

    if args.format == "md":
        sys.stdout.write(to_markdown(result))
        return

    if args.format == "pretty":
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return

    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
