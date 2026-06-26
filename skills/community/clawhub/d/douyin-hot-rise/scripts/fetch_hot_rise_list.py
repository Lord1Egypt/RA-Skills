#!/usr/bin/env python3
"""
抖音上升热点榜 API 调用脚本
接口：POST https://coze-js-api.devtool.uk/douyin/billboard/fetch_hot_rise_list
购买/查看文档：https://devtool.uk/wiki
"""

import argparse
import json
import os
import sys

try:
    import requests
except ImportError:
    print("缺少依赖库，请先安装：pip install requests", file=sys.stderr)
    sys.exit(1)

API_URL = "https://coze-js-api.devtool.uk/douyin/billboard/fetch_hot_rise_list"


def get_api_key(arg_key: str | None) -> str:
    """优先使用参数传入的 key，否则读取环境变量 AZT_API_KEY"""
    key = arg_key or os.environ.get("AZT_API_KEY", "").strip()
    if not key:
        print(
            "❌ 未检测到 API Key。\n"
            "   请前往 https://devtool.uk/wiki 购买或查看使用说明，\n"
            "   然后通过以下任一方式提供 Key：\n"
            "   1. 设置环境变量：export AZT_API_KEY=\"your_key\"\n"
            "   2. 传入参数：python3 fetch_hot_rise_list.py --azt_api_key your_key",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def fetch_hot_rise_list(
    api_key: str,
    page: int = 1,
    page_size: int = 10,
    order: str = "rank",
    sentence_tag: str = "",
    keyword: str = "",
) -> dict:
    payload: dict = {
        "api_key": api_key,
        "page": page,
        "page_size": page_size,
        "order": order,
    }
    if sentence_tag:
        payload["sentence_tag"] = sentence_tag
    if keyword:
        payload["keyword"] = keyword

    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=30,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.Timeout:
        print("❌ 请求超时，请检查网络连接后重试。", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求失败：{e}", file=sys.stderr)
        sys.exit(1)


def print_results(data: dict) -> None:
    code = data.get("code")
    msg = data.get("msg", "")

    if code != 200:
        print(f"❌ 接口返回错误（code={code}）：{msg}")
        print("\n可能原因：")
        print("  - API Key 无效或已过期 → 前往 https://devtool.uk/wiki 重新购买")
        print("  - API Key 积分已用完 → 联系作者续费")
        print("  - 服务器错误 → 稍后重试")
        sys.exit(1)

    print(f"✅ 请求成功  {msg}")
    print("-" * 60)

    items = data.get("data", {})
    # 兼容列表或嵌套对象两种结构
    if isinstance(items, list):
        entries = items
    elif isinstance(items, dict):
        # 尝试常见的嵌套 key
        entries = items.get("word_list") or items.get("list") or items.get("items") or []
    else:
        entries = []

    if not entries:
        print("暂无数据，原始响应：")
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    for idx, item in enumerate(entries, start=1):
        rank = item.get("rank", idx)
        title = item.get("word", item.get("title", item.get("name", "—")))
        hot_value = item.get("hot_value", item.get("heat", "—"))
        print(f"  {rank:>3}. {title}  (热度: {hot_value})")

    print("-" * 60)
    print(f"共 {len(entries)} 条数据")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="调用抖音上升热点榜接口",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例：\n  python3 fetch_hot_rise_list.py --page 1 --page_size 20 --order hot --keyword 明星",
    )
    parser.add_argument("--azt_api_key", default=None, help="API Key（也可通过环境变量 AZT_API_KEY 设置）")
    parser.add_argument("--page", type=int, default=1, help="页码（默认 1）")
    parser.add_argument("--page_size", type=int, default=10, help="每页条数（默认 10）")
    parser.add_argument("--order", default="rank", choices=["rank", "hot"], help="排序方式（默认 rank）")
    parser.add_argument("--sentence_tag", default="", help="话题分类标签（可选）")
    parser.add_argument("--keyword", default="", help="关键词筛选（可选）")
    parser.add_argument("--json", action="store_true", dest="output_json", help="以 JSON 格式输出原始响应")
    args = parser.parse_args()

    api_key = get_api_key(args.azt_api_key)

    print(f"📡 请求接口：{API_URL}")
    print(f"   参数：page={args.page}, page_size={args.page_size}, order={args.order}", end="")
    if args.sentence_tag:
        print(f", sentence_tag={args.sentence_tag}", end="")
    if args.keyword:
        print(f", keyword={args.keyword}", end="")
    print()

    result = fetch_hot_rise_list(
        api_key=api_key,
        page=args.page,
        page_size=args.page_size,
        order=args.order,
        sentence_tag=args.sentence_tag,
        keyword=args.keyword,
    )

    if args.output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_results(result)


if __name__ == "__main__":
    main()
