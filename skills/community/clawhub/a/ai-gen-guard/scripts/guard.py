#!/usr/bin/env python3
"""
ai-gen-guard — 生成式 AI 服务合规护栏

用法:
  python3 guard.py --text "描述文本"
  python3 guard.py --interactive
  python3 guard.py --json < data.json

示例:
  python3 guard.py --text "我们的生成式AI服务还没有做算法备案"
  python3 guard.py --interactive
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
from core.detector import scan_text


def format_result(result: dict) -> str:
    """格式化输出"""
    lines = []
    risk_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}
    icon = risk_icon.get(result["risk_level"], "⚪")

    lines.append(f"{icon} 风险等级: {result['risk_level'].upper()}")
    lines.append(f"  评估摘要: {result['summary']}")

    if result["scenario"]["matched_indicators"]:
        lines.append(
            f"  触发关键词: {', '.join(result['scenario']['matched_indicators'][:10])}"
        )

    lines.append("")
    lines.append("━━━ 合规检查明细 ━━━")
    for check in result["checks"]:
        status_icon = {
            "pass": "✅", "possible_pass": "✅",
            "warn": "⚠️", "needs_review": "⚠️",
            "fail": "❌", "unchecked": "⬜",
        }.get(check["status"], "⬜")
        lines.append(f"  {status_icon} {check['label']} ({check['regulation']})")
        if check.get("standard_ref"):
            lines.append(f"     国标: {check['standard_ref']}")
        lines.append(f"     状态: {check['status']}")
        if check["detail"]:
            lines.append(f"     说明: {check['detail']}")
        if check["findings"]:
            for f in check["findings"]:
                lines.append(f"      📎 {f}")

    lines.append("")
    lines.append("━━━ 建议动作 ━━━")
    for a in result["suggested_actions"]:
        lines.append(f"  · {a}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="生成式 AI 服务合规护栏")
    parser.add_argument("--text", help="待评估的生成式AI服务场景描述文本")
    parser.add_argument("--interactive", action="store_true", help="交互模式")
    parser.add_argument("--json", action="store_true", help="JSON输出模式")
    parser.add_argument("--format", choices=["text", "json"], default="text",
                        help="输出格式（默认text）")
    args = parser.parse_args()

    if args.text:
        text = args.text
    elif args.interactive:
        print("=" * 50)
        print("生成式 AI 服务合规护栏 (ai-gen-guard)")
        print("请输入待评估的场景描述，输入 exit 退出")
        print("=" * 50)
        lines = []
        while True:
            try:
                line = input()
                if line.lower() in ("exit", "quit", "q"):
                    break
                lines.append(line)
            except (EOFError, KeyboardInterrupt):
                break
        text = "\n".join(lines)
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)

    if not text.strip():
        print("错误: 未输入文本")
        sys.exit(1)

    result = scan_text(text)

    if args.format == "json" or args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_result(result))


if __name__ == "__main__":
    main()
