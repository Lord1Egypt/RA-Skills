#!/usr/bin/env python3
import argparse
import json
import sys
from typing import Any

from billcat_api import EXTRACT_BILL_URL, post_json


def extract_bill(text: str, timeout: int = 30) -> Any:
    return post_json(EXTRACT_BILL_URL, {"text": text}, timeout=timeout)


def to_markdown(text: str, result: Any) -> str:
    lines: list[str] = [f"- 原始文本: {text}"]

    if isinstance(result, dict):
        code = result.get("code")
        message = result.get("message")
        data = result.get("data")

        if code is not None:
            lines.append(f"- 响应码: {code}")
        if message:
            lines.append(f"- 响应消息: {message}")

        if isinstance(data, dict):
            saved_bills = data.get("savedBills")
            ai_info = data.get("aiInfo")

            if isinstance(saved_bills, list) and saved_bills:
                lines.append("")
                lines.append("## 已保存账单")
                for index, bill in enumerate(saved_bills, start=1):
                    if not isinstance(bill, dict):
                        continue
                    lines.append(f"- 账单{index} ID: {bill.get('billId', '')}")
                    lines.append(f"- 账单{index} 金额: {bill.get('amount', '')}")
                    lines.append(f"- 账单{index} 分类: {bill.get('categoryName', '')}")
                    lines.append(f"- 账单{index} 备注: {bill.get('remark', '')}")
                    lines.append(f"- 账单{index} 时间戳: {bill.get('billTime', '')}")
                    lines.append(f"- 账单{index} 账本: {bill.get('bookName', '')}")

            if isinstance(ai_info, list) and ai_info:
                text_messages = []
                for item in ai_info:
                    if isinstance(item, dict) and item.get("type") == "text":
                        content = item.get("content")
                        if isinstance(content, str) and content.strip():
                            text_messages.append(content.strip())

                if text_messages:
                    lines.append("")
                    lines.append("## AI 回复")
                    for item in text_messages:
                        lines.append(f"- {item}")

            return "\n".join(lines) + "\n"

    lines.append("")
    lines.append("```json")
    lines.append(json.dumps(result, ensure_ascii=False, indent=2))
    lines.append("```")
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract and save bill data from natural language via BillCat API")
    parser.add_argument("--text", help="Natural language bill description to save, e.g. '中午吃饭160'")
    parser.add_argument("--stdin", action="store_true", help="Read bill description from stdin")
    parser.add_argument("--timeout", type=int, default=30)
    parser.add_argument("--format", choices=["raw", "pretty", "md"], default="raw")
    args = parser.parse_args()

    text = args.text
    if args.stdin:
        stdin_text = sys.stdin.read().strip()
        if stdin_text:
            text = stdin_text

    if not text or not text.strip():
        raise SystemExit("Provide --text '...' or pipe text with --stdin")

    result = extract_bill(text.strip(), timeout=max(1, args.timeout))

    if args.format == "md":
        sys.stdout.write(to_markdown(text.strip(), result))
        return

    if args.format == "pretty":
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")
        return

    json.dump(result, sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
