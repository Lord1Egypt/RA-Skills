#!/usr/bin/env python3
"""
brand-sentinel — 品牌舆情哨兵
==============================
通用品牌舆情搜索+去重+时效过滤工具。

用法:
  python3 sentinel.py --brand "特斯拉" --keywords "刹车失灵,自燃" --hours 48
  python3 sentinel.py --brand "瑞幸咖啡" --keywords "食品安全,蟑螂" --hours 24 --output json
  python3 sentinel.py --config config.json

输出:
  --output text  → 人类可读的文本摘要（默认）
  --output json  → 结构化 JSON（供程序/LLM消费）
"""

import sys
import os
import json
import hashlib
import time
import urllib.request
import ssl
import re
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ── SSL 修复 ─────────────────────────────────────
def _fix_ssl():
    try:
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
        opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))
        urllib.request.install_opener(opener)
    except ImportError:
        pass
_fix_ssl()

# ── AutoGLM API ──────────────────────────────────
APP_ID     = "100003"
APP_KEY    = "38d2391985e2369a5fb8227d8e6cd5e5"
SEARCH_URL = "https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/web-search"
TOKEN_URL  = "http://127.0.0.1:18432/get_token"


def get_token():
    try:
        with urllib.request.urlopen(TOKEN_URL, timeout=5) as resp:
            token = resp.read().decode("utf-8").strip()
    except Exception as e:
        print(f"❌ Token 获取失败: {e}", file=sys.stderr)
        sys.exit(1)
    if not token:
        print("❌ Token 为空", file=sys.stderr)
        sys.exit(1)
    if not token.lower().startswith("bearer "):
        token = f"Bearer {token}"
    return token


def web_search(query: str, token: str) -> dict:
    timestamp = str(int(time.time()))
    sign = hashlib.md5(f"{APP_ID}&{timestamp}&{APP_KEY}".encode()).hexdigest()
    payload = json.dumps({"queries": [{"query": query}]}).encode()
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "X-Auth-Appid": APP_ID,
        "X-Auth-TimeStamp": timestamp,
        "X-Auth-Sign": sign,
    }
    req = urllib.request.Request(SEARCH_URL, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"⚠️ 搜索失败 [{query}]: {e}", file=sys.stderr)
        return {"code": -1, "msg": str(e)}


def extract_results(api_response: dict) -> list:
    items = []
    try:
        for r in api_response.get("data", {}).get("results", []):
            for p in r.get("webPages", {}).get("value", []):
                items.append({
                    "title":   p.get("name", ""),
                    "url":     p.get("url", ""),
                    "snippet": p.get("snippet", ""),
                })
    except Exception:
        pass
    return items


# ── 日期解析 ─────────────────────────────────────
def parse_date(text: str):
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)
    patterns = [
        (r'(\d{4})年(\d{1,2})月(\d{1,2})日', lambda m: datetime(int(m[1]), int(m[2]), int(m[3]), tzinfo=tz)),
        (r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})', lambda m: datetime(int(m[1]), int(m[2]), int(m[3]), tzinfo=tz)),
        (r'(\d{1,2})月(\d{1,2})日', lambda m: datetime(now.year, int(m[1]), int(m[2]), tzinfo=tz)),
        (r'(今天|刚刚|最新)', lambda m: now),
        (r'昨天', lambda m: now - timedelta(days=1)),
        (r'前天', lambda m: now - timedelta(days=2)),
        (r'(\d+)\s*小时前', lambda m: now - timedelta(hours=int(m[1]))),
        (r'(\d+)\s*天前', lambda m: now - timedelta(days=int(m[1]))),
        (r'(\d+)\s*分钟前', lambda m: now - timedelta(minutes=int(m[1]))),
    ]
    for pattern, builder in patterns:
        match = re.search(pattern, text)
        if match:
            try:
                return builder(match)
            except (ValueError, IndexError):
                continue
    return None


# ── 核心流程 ─────────────────────────────────────
def run_sentinel(brand, keywords, hours=48, output="text"):
    """
    执行品牌舆情哨兵流程。
    返回结构化结果 dict。
    """
    tz = timezone(timedelta(hours=8))
    now = datetime.now(tz)
    cutoff = now - timedelta(hours=hours)
    run_time = now.strftime("%Y-%m-%d %H:%M:%S")
    ym = now.strftime("%Y年%-m月")

    # 1. 构建搜索词（原始 + "最新" + "年月" 限定）
    queries = []
    for kw in keywords:
        queries.append(kw)
        queries.append(f"{kw} 最新")
        queries.append(f"{kw} {ym}")

    # 2. 搜索
    token = get_token()
    all_items = []
    seen_urls = set()

    for q in queries:
        print(f"  🔎 {q}", file=sys.stderr)
        resp = web_search(q, token)
        items = extract_results(resp)
        for item in items:
            url = item.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                all_items.append(item)
        time.sleep(0.3)

    print(f"  📊 原始结果: {len(all_items)} 条", file=sys.stderr)

    # 3. 时效过滤
    recent = []
    expired = 0
    no_date = 0

    for item in all_items:
        combined = f"{item.get('title', '')} {item.get('snippet', '')}"
        dt = parse_date(combined)

        if dt is None:
            item["date_status"] = "unknown"
            item["parsed_date"] = None
            no_date += 1
            recent.append(item)
        elif dt >= cutoff:
            item["date_status"] = "recent"
            item["parsed_date"] = dt.strftime("%Y-%m-%d")
            recent.append(item)
        else:
            item["date_status"] = "expired"
            item["parsed_date"] = dt.strftime("%Y-%m-%d")
            expired += 1

    print(f"  ⏰ 保留 {len(recent)} 条（{expired} 条超{hours}h，{no_date} 条无日期默认保留）", file=sys.stderr)

    # 4. 构建输出
    result = {
        "brand": brand,
        "run_time": run_time,
        "time_window_hours": hours,
        "keywords": keywords,
        "stats": {
            "raw_count": len(all_items),
            "kept_count": len(recent),
            "expired_count": expired,
            "no_date_count": no_date,
        },
        "items": [
            {
                "title":       i.get("title", ""),
                "url":         i.get("url", ""),
                "snippet":     i.get("snippet", ""),
                "date_status": i.get("date_status"),
                "parsed_date": i.get("parsed_date"),
            }
            for i in recent
        ],
    }

    # 5. 输出
    if output == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_text(result)

    return result


def _print_text(result):
    """人类可读的文本输出"""
    lines = []
    lines.append(f"{'='*50}")
    lines.append(f"📡 品牌舆情哨兵 — {result['brand']}")
    lines.append(f"⏰ {result['run_time']}  |  窗口: {result['time_window_hours']}h")
    lines.append(f"{'='*50}")
    s = result["stats"]
    lines.append(f"原始: {s['raw_count']}  保留: {s['kept_count']}  过期: {s['expired_count']}  无日期: {s['no_date_count']}")
    lines.append(f"关键词: {', '.join(result['keywords'])}")
    lines.append(f"{'-'*50}")

    for i, item in enumerate(result["items"], 1):
        date_tag = ""
        if item["parsed_date"]:
            date_tag = f" [{item['parsed_date']} {'✅' if item['date_status']=='recent' else '⚠️'}]"
        else:
            date_tag = " [⚠️日期未知]"
        lines.append(f"\n{i}. {item['title']}{date_tag}")
        lines.append(f"   {item['snippet'][:120]}")
        lines.append(f"   {item['url'][:80]}")

    lines.append(f"\n{'='*50}")
    print("\n".join(lines))


# ── CLI 入口 ─────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="brand-sentinel: 品牌舆情哨兵")
    parser.add_argument("--brand", help="品牌名，如 '特斯拉'")
    parser.add_argument("--keywords", help="关键词，逗号分隔，如 '刹车失灵,自燃'")
    parser.add_argument("--hours", type=int, default=48, help="时效窗口（小时），默认48")
    parser.add_argument("--output", choices=["text", "json"], default="text", help="输出格式")
    parser.add_argument("--config", help="JSON配置文件路径（替代命令行参数）")
    args = parser.parse_args()

    if args.config:
        cfg = json.loads(Path(args.config).read_text("utf-8"))
        brand = cfg.get("brand", "")
        keywords = cfg.get("keywords", [])
        hours = cfg.get("hours", 48)
        output = cfg.get("output", "text")
    else:
        if not args.brand or not args.keywords:
            print("❌ 必须提供 --brand 和 --keywords，或使用 --config", file=sys.stderr)
            sys.exit(1)
        brand = args.brand
        keywords = [k.strip() for k in args.keywords.split(",")]
        hours = args.hours
        output = args.output

    run_sentinel(brand=brand, keywords=keywords, hours=hours, output=output)
