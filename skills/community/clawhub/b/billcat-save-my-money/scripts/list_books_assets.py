#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Any

from billcat_api import SKILL_API_URL, post_json


def list_books_assets(start_date: str | None = None, end_date: str | None = None, timeout: int = 30) -> Any:
    payload: dict[str, Any] = {
        "action": "list",
        "param": {},
    }
    if start_date:
        payload["param"]["startDate"] = start_date
    if end_date:
        payload["param"]["endDate"] = end_date

    return post_json(SKILL_API_URL, payload, timeout=timeout)


def _append_group_lines(lines: list[str], title: str, items: list[Any], name_key: str, id_key: str) -> None:
    if not items:
        lines.append(f"## {title}")
        lines.append("- 无")
        return

    lines.append(f"## {title}")
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            lines.append(f"- {title}{index}: {item}")
            continue

        lines.append(f"- {title}{index} ID: {item.get(id_key, '')}")
        lines.append(f"- {title}{index} 名称: {item.get(name_key, '')}")
        if item.get("type") is not None:
            lines.append(f"- {title}{index} 类型: {item.get('type', '')}")
        if item.get("bookIcon") is not None:
            lines.append(f"- {title}{index} 图标: {item.get('bookIcon', '')}")
        if item.get("assetType") is not None:
            lines.append(f"- {title}{index} 资产类型: {item.get('assetType', '')}")
        if item.get("assetIcon") is not None:
            lines.append(f"- {title}{index} 资产图标: {item.get('assetIcon', '')}")
        if item.get("assetProps") is not None:
            lines.append(f"- {title}{index} 资产属性: {item.get('assetProps', '')}")
        if item.get("bookId") is not None and id_key != "bookId":
            lines.append(f"- {title}{index} 所属账本ID: {item.get('bookId', '')}")
        if item.get("totalIncome") is not None:
            lines.append(f"- {title}{index} 总收入: {item.get('totalIncome')}")
        if item.get("totalExpense") is not None:
            lines.append(f"- {title}{index} 总支出: {item.get('totalExpense')}")
        if item.get("netAmount") is not None:
            lines.append(f"- {title}{index} 净额: {item.get('netAmount')}")


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
    if data.get("action"):
        lines.append(f"- 动作: {data['action']}")
    if data.get("startDate"):
        lines.append(f"- 开始日期: {data['startDate']}")
    if data.get("endDate"):
        lines.append(f"- 结束日期: {data['endDate']}")

    books = data.get("books") if isinstance(data.get("books"), list) else []
    assets = data.get("assets") if isinstance(data.get("assets"), list) else []

    if lines:
        lines.append("")

    _append_group_lines(lines, "账本", books, "name", "bookId")
    lines.append("")
    _append_group_lines(lines, "资产", assets, "assetName", "assetId")

    extra = {
        k: v
        for k, v in data.items()
        if k not in {"action", "startDate", "endDate", "books", "assets"}
    }
    if extra:
        lines.append("")
        lines.append("附加字段:")
        lines.append("```json")
        lines.append(json.dumps(extra, ensure_ascii=False, indent=2))
        lines.append("```")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="List books and assets in BillCat via OpenClaw skill API")
    parser.add_argument("--start-date", help="Start date in YYYYMMDD format")
    parser.add_argument("--end-date", help="End date in YYYYMMDD format")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--format", choices=["raw", "pretty", "md"], default="raw")
    args = parser.parse_args()

    result = list_books_assets(
        start_date=args.start_date.strip() if args.start_date else None,
        end_date=args.end_date.strip() if args.end_date else None,
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