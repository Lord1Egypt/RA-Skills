#!/usr/bin/env python3
"""ChatBI Agent CLI — 问数 Agent 命令行工具.

Usage:
    python3 scripts/chatbi_cli.py -q "查询乳制品的销售情况"
    python3 scripts/chatbi_cli.py -q "各品类月度销售趋势" --output detail
    python3 scripts/chatbi_cli.py -q "查询销量Top10" --output sql-only
    python3 scripts/chatbi_cli.py -q "查询销售情况" --output raw

Author: ChatBI Skills
Created: 2026-04-01
"""

import argparse
import json
import sys
from pathlib import Path

# Ensure local packages are importable
_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from chatbi.config import ChatBIConfig
from chatbi.client import ChatBIClient
from chatbi.parser import SSEEventParser
from chatbi.formatter import ResultFormatter


def build_parser() -> argparse.ArgumentParser:
    """构建命令行参数解析器."""
    parser = argparse.ArgumentParser(
        prog="chatbi_cli",
        description="ChatBI 问数 Agent — 自然语言数据查询工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
输出模式说明:
  summary   (默认) 关键信息: 意图理解 + 选表结果 + SQL + 最终回答
  detail    完整过程: 含执行计划和数据预览
  sql-only  仅输出生成的 SQL
  raw       输出所有被过滤的事件 JSON（调试用）

示例:
  python3 scripts/chatbi_cli.py -q "查询乳制品的销售情况"
  python3 scripts/chatbi_cli.py -q "各品类月度销售趋势" --output detail
  python3 scripts/chatbi_cli.py -q "查询销量Top10" --output sql-only
""",
    )

    parser.add_argument(
        "--query", "-q",
        required=True,
        metavar="QUERY",
        help="自然语言查询问题",
    )

    parser.add_argument(
        "--output", "-o",
        choices=["summary", "detail", "sql-only", "raw"],
        default="summary",
        metavar="MODE",
        help="输出模式: summary (默认) | detail | sql-only | raw",
    )

    parser.add_argument(
        "--no-stream",
        action="store_true",
        help="使用非流式调用（调试用）",
    )

    parser.add_argument(
        "--save-raw",
        metavar="FILE",
        help="将所有原始 SSE 事件保存到指定 JSON 文件",
    )

    parser.add_argument(
        "--api-url",
        metavar="URL",
        help="覆盖 API 端点 URL",
    )

    return parser


def cmd_query(args: argparse.Namespace) -> None:
    """执行问数查询."""
    # 初始化配置
    config = ChatBIConfig.from_env()
    if args.api_url:
        config.api_url = args.api_url

    client = ChatBIClient(config)
    parser = SSEEventParser()
    formatter = ResultFormatter(output_mode=args.output)

    question = args.query
    output_mode = args.output

    if args.no_stream:
        # 非流式模式
        print(f"非流式调用: {question}")
        try:
            result = client.query(question)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # 流式模式
    print(formatter.format_stream_header(question), flush=True)

    try:
        event_count = 0
        filtered_count = 0

        for event in client.stream_query(question):
            event_count += 1

            # raw 模式：除了过滤结果外，也输出原始事件
            if output_mode == "raw":
                event_type = event.get("type", "?")
                data = event.get("data", {})
                tool_name = data.get("tool_name", "") if isinstance(data, dict) else ""
                label = f"[{event_type}]"
                if tool_name:
                    label += f" tool={tool_name}"
                print(f"\n--- Event #{event_count} {label} ---")

            # 解析并过滤
            filtered_results = parser.process_event(event)

            for result in filtered_results:
                filtered_count += 1
                formatted = formatter.format_event(result)
                if formatted:
                    print(formatted, flush=True)

            # raw 模式额外输出完整事件
            if output_mode == "raw" and not filtered_results:
                event_type = event.get("type", "?")
                print(f"  (skipped: type={event_type})", flush=True)

    except KeyboardInterrupt:
        print("\n\n已中断。", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # 无论正常结束还是连接中断，都输出已有结果的摘要
        response = parser.get_response()

        if output_mode != "raw":
            print(formatter.format_stream_footer(response), flush=True)

        if args.save_raw:
            save_path = Path(args.save_raw)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(response.raw_events, f, ensure_ascii=False, indent=2)
            print(f"\n原始事件已保存到: {save_path.resolve()}")

        print(f"\n共处理 {event_count} 个事件，提取 {filtered_count} 个关键结果。")


def main() -> None:
    arg_parser = build_parser()
    args = arg_parser.parse_args()
    cmd_query(args)


if __name__ == "__main__":
    main()
