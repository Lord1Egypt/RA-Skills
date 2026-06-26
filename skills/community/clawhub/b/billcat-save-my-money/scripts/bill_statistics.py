#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Any

from billcat_api import SKILL_API_URL, post_json


def get_statistics(start_date: str, end_date: str, timeout: int = 30) -> Any:
    return post_json(
        SKILL_API_URL,
        {
            "action": "statics",
            "param": {
                "startDate": start_date,
                "endDate": end_date,
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
    if data.get("startDate"):
        lines.append(f"- 开始日期: {data['startDate']}")
    if data.get("endDate"):
        lines.append(f"- 结束日期: {data['endDate']}")
    if data.get("totalIncome") is not None:
        lines.append(f"- 总收入: {data['totalIncome']}")
    if data.get("totalExpense") is not None:
        lines.append(f"- 总支出: {data['totalExpense']}")
    if data.get("netAmount") is not None:
        lines.append(f"- 净额: {data['netAmount']}")

    if not lines:
        return json.dumps(result, ensure_ascii=False, indent=2) + "\n"

    extra = {
        k: v
        for k, v in data.items()
        if k not in {"startDate", "endDate", "totalIncome", "totalExpense", "netAmount"}
    }
    if extra:
        lines.append("")
        lines.append("附加字段:")
        lines.append("```json")
        lines.append(json.dumps(extra, ensure_ascii=False, indent=2))
        lines.append("```")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Get bill statistics in BillCat via OpenClaw skill API")
    parser.add_argument("--start-date", required=True, help="Start date in YYYYMMDD format")
    parser.add_argument("--end-date", required=True, help="End date in YYYYMMDD format")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--format", choices=["raw", "pretty", "md"], default="raw")
    args = parser.parse_args()

    result = get_statistics(
        start_date=args.start_date.strip(),
        end_date=args.end_date.strip(),
        timeout=max(1, args.timeout),
    )

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
