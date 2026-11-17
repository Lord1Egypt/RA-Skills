#!/usr/bin/env python3
"""粉象 MCP 全链路自检：协议（initialize / tools/list / prompts/list）+ 8 个工具。

商品链接不写死：先用 goods_search 搜在售商品，取结果里的链接再测按链接的工具，
避免分享短链过期、商品下架造成误报。

用法：
  python3 verify.py
  python3 verify.py --url https://<测试环境>/njia/mcp
  python3 verify.py --insecure   # 仅内网自签名测试环境
"""

import argparse
import json
import os
import sys

from fenxiang_mcp import DEFAULT_URL, TOOLS, McpClient, McpError, load_api_key

SERVER_NAME = "fenxiang-saving-assistant"
SEARCH_KEYWORDS = ("iPhone 17 Pro 256G", "戴森吹风机", "小米手环 9")
MODEL_NAME = "iPhone 17 Pro 256G"
NEED = "500元以内送妈妈的生日礼物"
INTERNAL_METRIC_WORDS = ("评分", "置信度", "分位", "样本")


class Result:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def check(self, name, condition, detail=""):
        if condition:
            self.passed += 1
            print("PASS  %s" % name)
        else:
            self.failed += 1
            print("FAIL  %s  %s" % (name, detail))
        return condition

    def summary(self):
        total = self.passed + self.failed
        print("\nsummary: passed=%d failed=%d total=%d" % (self.passed, self.failed, total))
        return 0 if self.failed == 0 else 1


def keys_of(data, text):
    return sorted(data.keys()) if isinstance(data, dict) else (text or "")[:200]


def no_data(data):
    """业务上合法的“查不到”：带 message 且明确不可重试。"""
    return isinstance(data, dict) and bool(data.get("message")) and data.get("retryable") is False


def summary_ok(data):
    summary = data.get("summary") if isinstance(data, dict) else None
    return bool(summary) and not any(word in summary for word in INTERNAL_METRIC_WORDS)


def main():
    parser = argparse.ArgumentParser(description="粉象 MCP 全链路自检")
    parser.add_argument("--url", default=os.environ.get("FENXIANG_MCP_URL") or DEFAULT_URL)
    parser.add_argument("--api-key-file")
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--insecure", action="store_true",
                        help="仅内网自签名测试环境使用：跳过证书校验")
    args = parser.parse_args()

    client = McpClient(args.url, load_api_key(args.api_key_file),
                       timeout=args.timeout, insecure=args.insecure)
    result = Result()

    def call(tool, arguments):
        arguments = dict(arguments, responseFormat="json")
        text, data, _ = client.call_tool(tool, arguments)
        return text, data

    # ---- 协议 ----
    try:
        init = client.initialize()
        info = init.get("serverInfo") or {}
        result.check("initialize serverInfo", info.get("name") == SERVER_NAME, "serverInfo=%s" % info)
        result.check("initialize instructions", "buy_advice" in (init.get("instructions") or ""))
        tools = {tool.get("name"): tool for tool in client.list_tools()}
        result.check("tools/list has 8 tools", set(TOOLS).issubset(tools), "got=%s" % sorted(tools))
        result.check("tools are read-only",
                     all((tools[name].get("annotations") or {}).get("readOnlyHint") for name in TOOLS if name in tools))
        result.check("prompts/list", len(client.list_prompts()) >= 4)
    except Exception as error:
        result.check("protocol", False, str(error))
        return result.summary()

    # ---- 搜索，顺便拿在售链接 ----
    links = []
    for keyword in SEARCH_KEYWORDS:
        try:
            text, data = call("goods_search", {"keyword": keyword, "platform": "all", "size": 10})
        except McpError as error:
            result.check("goods_search %s" % keyword, False, str(error))
            continue
        items = data.get("goodsList") if isinstance(data, dict) else None
        links = [item["goodsUrl"] for item in items or [] if item.get("goodsUrl")]
        if len(links) >= 2:
            result.check("goods_search returns items with links", True)
            result.check("goods_search summary", summary_ok(data), "summary=%s" % (data or {}).get("summary"))
            break
    if len(links) < 2:
        result.check("goods_search returns items with links", False, "no keyword returned 2+ links")
        return result.summary()

    # ---- 按链接 ----
    link = links[0]
    try:
        text, data = call("buy_advice", {"goodsUrl": link})
        serialized = json.dumps(data, ensure_ascii=False) if data is not None else (text or "")
        if no_data(data):
            result.check("buy_advice no-data has next action", bool(data.get("suggestedNextAction")))
        else:
            result.check("buy_advice conclusion and price",
                         isinstance(data, dict)
                         and bool(data.get("conclusionText") or data.get("recommendation"))
                         and (data.get("currentPrice") or data.get("finalPrice") or 0) > 0
                         and bool(data.get("itemTitle")),
                         "keys=%s" % keys_of(data, text))
            result.check("buy_advice summary without internal metrics", summary_ok(data),
                         "summary=%s" % (data or {}).get("summary"))
            result.check("buy_advice has order link", bool(data.get("goodsUrl")), "keys=%s" % keys_of(data, text))
        result.check("buy_advice has no commissionRebate", "commissionRebate" not in serialized)
    except Exception as error:
        result.check("buy_advice", False, str(error))

    for tool, check_name, ok in (
            ("history_price", "history_price returns points",
             lambda d: isinstance(d, dict) and isinstance(d.get("points"), list) and bool(d.get("points"))),
            ("compare_price", "compare_price returns rows",
             lambda d: isinstance(d, dict) and isinstance(d.get("items"), list)),
            ("saving_plan", "saving_plan returns price and steps",
             lambda d: isinstance(d, dict) and (d.get("finalPrice") or 0) > 0 and bool(d.get("steps"))
             and bool(d.get("planKind")))):
        try:
            text, data = call(tool, {"goodsUrl": link})
            result.check(check_name, ok(data) or no_data(data), "keys=%s" % keys_of(data, text))
        except Exception as error:
            result.check(tool, False, str(error))

    try:
        text, data = call("batch_analyze", {"goodsUrls": "\n".join(links[:2])})
        items = data.get("items") if isinstance(data, dict) else None
        result.check("batch_analyze returns items", bool(items), "keys=%s" % keys_of(data, text))
    except Exception as error:
        result.check("batch_analyze", False, str(error))

    # ---- 按名比价、按需求推荐 ----
    try:
        text, data = call("compare_by_name", {"productName": MODEL_NAME})
        result.check("compare_by_name returns rows or candidates",
                     isinstance(data, dict) and (bool(data.get("items")) or bool(data.get("suggestions"))
                                                 or no_data(data)),
                     "keys=%s" % keys_of(data, text))
    except Exception as error:
        result.check("compare_by_name", False, str(error))

    try:
        text, data = call("recommend_goods", {"userQuery": NEED})
        result.check("recommend_goods returns groups or clarify",
                     isinstance(data, dict) and (bool(data.get("groups")) or bool(data.get("clarifyQuestions"))
                                                 or bool(data.get("reply")) or no_data(data)),
                     "keys=%s" % keys_of(data, text))
    except Exception as error:
        result.check("recommend_goods", False, str(error))

    return result.summary()


if __name__ == "__main__":
    try:
        sys.exit(main())
    except McpError as error:
        print("ERROR: %s" % error, file=sys.stderr)
        sys.exit(1)
