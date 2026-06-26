#!/usr/bin/env python3
"""
国会山股神线索追踪 - 数据抓取脚本
从 Capitol Trades 获取美国国会议员的最新股票交易数据。

Capitol Trades 使用 Next.js App Router (RSC) 架构，交易数据嵌入在 HTML 的
React Server Components payload 中，本脚本通过解析 RSC payload 提取结构化数据。

用法：
    python fetch_trades.py [--days N] [--min-amount AMOUNT] [--politician NAME] [--output FILE]

参数：
    --days N           获取最近 N 天的交易记录（默认 90）
    --min-amount       最低交易金额筛选，如 50000（默认不筛选）
    --politician NAME  按议员姓名筛选（模糊匹配）
    --ticker SYMBOL    按股票代码筛选
    --chamber          筛选议院：senate / house（默认全部）
    --tx-type          筛选交易类型：buy / sell（默认全部）
    --output FILE      输出文件路径（默认输出到 stdout，支持 .json / .csv）
    --analyze          执行重仓分析和异常检测
    --pages N          抓取页数（默认 3 页，每页约 12 条）
"""

import argparse
import json
import sys
import re
import csv
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from io import StringIO


def fetch_page(page=1, page_size=96, sort="-pubDate"):
    """
    从 Capitol Trades 抓取单页交易数据。
    数据嵌入在 Next.js RSC payload 中，解析后返回交易记录列表。
    """
    params = {
        "page": str(page),
        "pageSize": str(page_size),
        "sortBy": sort,
    }
    url = f"https://www.capitoltrades.com/trades?{urllib.parse.urlencode(params)}"

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
    }

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            html = resp.read().decode("utf-8")
            return parse_rsc_trades(html)
    except Exception as e:
        print(f"⚠️ 抓取第 {page} 页失败: {e}", file=sys.stderr)
        return []


def parse_rsc_trades(html):
    """
    从 Next.js RSC payload 中解析交易数据。

    Capitol Trades 使用 React Server Components，数据以如下格式嵌入 HTML：
    self.__next_f.push([1,"...escaped JSON..."])

    交易记录是 JSON 数组，每条记录包含：
    _txId, _politicianId, chamber, txDate, txType, value,
    issuer{issuerName, issuerTicker, sector},
    politician{firstName, lastName, party}, pubDate, reportingGap 等字段
    """
    # 提取所有 RSC chunks
    chunks = re.findall(r'self\.__next_f\.push\(\[1,"(.*?)"\]\)', html, re.DOTALL)
    if not chunks:
        return []

    # 解码并合并所有 chunks
    full_rsc = ""
    for chunk in chunks:
        try:
            decoded = chunk.encode("utf-8").decode("unicode_escape")
        except (UnicodeDecodeError, ValueError):
            decoded = chunk
        full_rsc += decoded

    # 查找交易数据 - 匹配包含 _txId 的 JSON 数组
    trades = []

    # 方法1：提取完整的交易数组
    # 交易数据通常在 RSC 中以 JSON 数组形式出现
    # 找到所有 _txId 出现的位置，然后向前回溯找到数组起始
    tx_positions = [m.start() for m in re.finditer(r'"_txId"', full_rsc)]

    if not tx_positions:
        return []

    # 从第一个 _txId 向前找到包含它的数组起始
    first_pos = tx_positions[0]
    # 向前搜索 [ 或 { 开始
    array_start = full_rsc.rfind("[", max(0, first_pos - 500), first_pos)

    if array_start == -1:
        # 尝试找单个对象
        array_start = full_rsc.rfind("{", max(0, first_pos - 200), first_pos)

    if array_start == -1:
        return []

    # 从 array_start 开始，找到匹配的闭合括号
    bracket_char = full_rsc[array_start]
    close_char = "]" if bracket_char == "[" else "}"
    depth = 0
    array_end = array_start

    for i in range(array_start, min(len(full_rsc), array_start + 200000)):
        ch = full_rsc[i]
        if ch == bracket_char:
            depth += 1
        elif ch == close_char:
            depth -= 1
            if depth == 0:
                array_end = i + 1
                break

    json_str = full_rsc[array_start:array_end]

    try:
        data = json.loads(json_str)
        if isinstance(data, list):
            trades = data
        elif isinstance(data, dict) and "_txId" in data:
            trades = [data]
    except json.JSONDecodeError:
        # 如果整个数组解析失败，逐条提取
        trades = extract_individual_trades(full_rsc, tx_positions)

    return normalize_trades(trades)


def extract_individual_trades(rsc_text, positions):
    """逐条提取交易记录（当数组解析失败时的备用方案）"""
    trades = []
    for pos in positions:
        # 向前找到 { 开始
        obj_start = rsc_text.rfind("{", max(0, pos - 200), pos)
        if obj_start == -1:
            continue

        # 找到匹配的 } 结束
        depth = 0
        obj_end = obj_start
        for i in range(obj_start, min(len(rsc_text), obj_start + 5000)):
            if rsc_text[i] == "{":
                depth += 1
            elif rsc_text[i] == "}":
                depth -= 1
                if depth == 0:
                    obj_end = i + 1
                    break

        try:
            obj = json.loads(rsc_text[obj_start:obj_end])
            if "_txId" in obj:
                trades.append(obj)
        except json.JSONDecodeError:
            continue

    return trades


def normalize_trades(raw_trades):
    """将原始交易数据标准化为统一格式"""
    normalized = []
    for t in raw_trades:
        if not isinstance(t, dict) or "_txId" not in t:
            continue

        issuer = t.get("issuer", {}) or {}
        politician = t.get("politician", {}) or {}

        # 解析 ticker（格式通常为 "AAPL:US"）
        raw_ticker = issuer.get("issuerTicker", "")
        ticker = raw_ticker.split(":")[0] if raw_ticker else ""

        record = {
            "tx_id": t.get("_txId"),
            "politician": f"{politician.get('firstName', '')} {politician.get('lastName', '')}".strip(),
            "politician_id": t.get("_politicianId", ""),
            "party": politician.get("party", ""),
            "chamber": t.get("chamber", politician.get("chamber", "")),
            "ticker": ticker,
            "issuer_name": issuer.get("issuerName", ""),
            "sector": issuer.get("sector", ""),
            "country": issuer.get("country", ""),
            "tx_type": t.get("txType", ""),
            "tx_date": t.get("txDate", ""),
            "pub_date": t.get("pubDate", ""),
            "reporting_gap_days": t.get("reportingGap", 0),
            "amount": t.get("value", 0),
            "price": t.get("price"),
            "owner": t.get("owner", ""),
            "comment": t.get("comment", ""),
        }
        normalized.append(record)

    return normalized


def filter_trades(trades, days=90, min_amount=0, politician=None,
                  ticker=None, chamber=None, tx_type=None):
    """根据条件筛选交易记录"""
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    filtered = []

    for trade in trades:
        # 日期筛选
        tx_date = trade.get("tx_date", "")
        if tx_date and tx_date < cutoff_date:
            continue

        # 金额筛选
        if min_amount > 0:
            amount = trade.get("amount", 0) or 0
            if amount < min_amount:
                continue

        # 议员姓名筛选（模糊匹配）
        if politician:
            name = trade.get("politician", "").lower()
            if politician.lower() not in name:
                continue

        # 股票代码筛选
        if ticker:
            if ticker.upper() != trade.get("ticker", "").upper():
                continue

        # 议院筛选
        if chamber:
            if chamber.lower() != trade.get("chamber", "").lower():
                continue

        # 交易类型筛选
        if tx_type:
            if tx_type.lower() != trade.get("tx_type", "").lower():
                continue

        filtered.append(trade)

    return filtered


def analyze_concentration(trades):
    """
    分析重仓标的：找出被多位议员集中买入的股票
    返回按买入议员数降序排列的标的列表
    """
    ticker_stats = {}

    for trade in trades:
        ticker = trade.get("ticker", "").strip()
        tx_type = trade.get("tx_type", "").lower()
        if not ticker or tx_type != "buy":
            continue

        if ticker not in ticker_stats:
            ticker_stats[ticker] = {
                "ticker": ticker,
                "issuer_name": trade.get("issuer_name", ""),
                "sector": trade.get("sector", ""),
                "buy_count": 0,
                "politicians": set(),
                "total_amount": 0,
                "latest_date": "",
                "parties": set(),
                "chambers": set(),
            }

        stats = ticker_stats[ticker]
        stats["buy_count"] += 1
        stats["politicians"].add(trade.get("politician", ""))
        stats["parties"].add(trade.get("party", ""))
        stats["chambers"].add(trade.get("chamber", ""))
        stats["total_amount"] += trade.get("amount", 0) or 0

        tx_date = trade.get("tx_date", "")
        if tx_date > stats["latest_date"]:
            stats["latest_date"] = tx_date

    # 转换 set 为 list
    result = []
    for ticker, stats in ticker_stats.items():
        stats["politicians"] = sorted(list(stats["politicians"]))
        stats["politician_count"] = len(stats["politicians"])
        stats["parties"] = sorted(list(stats["parties"]))
        stats["chambers"] = sorted(list(stats["chambers"]))
        result.append(stats)

    result.sort(key=lambda x: (x["politician_count"], x["buy_count"]), reverse=True)
    return result


def detect_anomalies(trades):
    """
    检测异常交易模式：
    1. 大额交易（>= $500,000）
    2. 密集交易（同一议员短期内多次交易同一标的）
    3. 跨党派共识（两党议员同时买入同一标的）
    4. 超短披露延迟（可能暗示紧迫性）
    """
    anomalies = []

    # 1. 大额交易
    for trade in trades:
        amount = trade.get("amount", 0) or 0
        if amount >= 500000:
            asset = trade["ticker"] or trade.get("issuer_name", "未知标的")
            anomalies.append({
                "type": "大额交易",
                "severity": "high",
                "description": (
                    f"{trade['politician']} ({trade['party']}) "
                    f"{'买入' if trade['tx_type'] == 'buy' else '卖出'} "
                    f"{asset} 金额 ${amount:,.0f}"
                ),
                "trade": trade,
            })

    # 2. 密集交易
    pol_ticker = {}
    for trade in trades:
        key = (trade.get("politician", ""), trade.get("ticker", ""))
        if key[0] and key[1]:
            pol_ticker.setdefault(key, []).append(trade)

    for (politician, ticker), trade_list in pol_ticker.items():
        if len(trade_list) >= 3:
            anomalies.append({
                "type": "密集交易",
                "severity": "medium",
                "description": (
                    f"{politician} 近期对 {ticker} "
                    f"进行了 {len(trade_list)} 次交易"
                ),
                "trade_count": len(trade_list),
            })

    # 3. 跨党派共识
    ticker_parties = {}
    for trade in trades:
        ticker = trade.get("ticker", "")
        if trade.get("tx_type", "").lower() == "buy" and ticker:
            if ticker not in ticker_parties:
                ticker_parties[ticker] = {"parties": set(), "politicians": set()}
            ticker_parties[ticker]["parties"].add(trade.get("party", ""))
            ticker_parties[ticker]["politicians"].add(trade.get("politician", ""))

    for ticker, info in ticker_parties.items():
        if len(info["parties"]) >= 2 and len(info["politicians"]) >= 3:
            anomalies.append({
                "type": "跨党派共识",
                "severity": "high",
                "description": (
                    f"{ticker} 被来自 {', '.join(info['parties'])} "
                    f"的 {len(info['politicians'])} 位议员买入"
                ),
                "politicians": sorted(list(info["politicians"])),
            })

    # 4. 极短披露延迟（<= 3天，可能暗示紧迫性或大额交易）
    for trade in trades:
        gap = trade.get("reporting_gap_days", 99)
        if gap is not None and gap <= 3 and trade.get("amount", 0) and trade["amount"] >= 50000:
            anomalies.append({
                "type": "极短披露延迟",
                "severity": "low",
                "description": (
                    f"{trade['politician']} 交易 {trade['ticker']} 后 "
                    f"仅 {gap} 天即披露（金额 ${trade['amount']:,.0f}）"
                ),
                "trade": trade,
            })

    return anomalies


def output_csv(trades, filepath):
    """将交易数据输出为 CSV"""
    fields = [
        "politician", "party", "chamber", "ticker", "issuer_name",
        "sector", "tx_type", "tx_date", "pub_date",
        "reporting_gap_days", "amount", "price", "owner", "comment",
    ]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for trade in trades:
            writer.writerow(trade)
    print(f"✅ CSV 已保存至 {filepath}", file=sys.stderr)


def output_json(data, filepath=None):
    """将数据输出为 JSON"""
    output = json.dumps(data, ensure_ascii=False, indent=2, default=str)
    if filepath:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ JSON 已保存至 {filepath}", file=sys.stderr)
    else:
        print(output)


def main():
    parser = argparse.ArgumentParser(
        description="国会山股神线索追踪 - 获取美国国会议员股票交易数据"
    )
    parser.add_argument("--days", type=int, default=90,
                        help="获取最近 N 天的交易记录（默认 90）")
    parser.add_argument("--min-amount", type=int, default=0,
                        help="最低交易金额筛选")
    parser.add_argument("--politician", type=str, default=None,
                        help="按议员姓名筛选（模糊匹配）")
    parser.add_argument("--ticker", type=str, default=None,
                        help="按股票代码筛选")
    parser.add_argument("--chamber", type=str, default=None,
                        choices=["senate", "house"],
                        help="筛选议院")
    parser.add_argument("--tx-type", type=str, default=None,
                        choices=["buy", "sell"],
                        help="筛选交易类型")
    parser.add_argument("--output", type=str, default=None,
                        help="输出文件路径（支持 .json / .csv）")
    parser.add_argument("--analyze", action="store_true",
                        help="执行重仓分析和异常检测")
    parser.add_argument("--pages", type=int, default=3,
                        help="抓取页数（默认 3）")

    args = parser.parse_args()

    print("🏛️ 正在获取国会议员交易数据...", file=sys.stderr)

    all_trades = []
    for page in range(1, args.pages + 1):
        print(f"   📄 正在抓取第 {page}/{args.pages} 页...", file=sys.stderr)
        trades = fetch_page(page=page)
        if trades:
            all_trades.extend(trades)
            print(f"      获取 {len(trades)} 条记录", file=sys.stderr)
        else:
            print(f"      第 {page} 页无数据或抓取失败", file=sys.stderr)
            if page == 1:
                print("   ⚠️ 首页即失败，请检查网络连接", file=sys.stderr)
                break

    if not all_trades:
        print("❌ 未能获取到任何交易数据。", file=sys.stderr)
        sys.exit(1)

    print(f"   ✅ 共获取 {len(all_trades)} 条原始记录", file=sys.stderr)

    # 去重（按 tx_id）
    seen_ids = set()
    unique_trades = []
    for t in all_trades:
        tid = t.get("tx_id")
        if tid and tid not in seen_ids:
            seen_ids.add(tid)
            unique_trades.append(t)
    all_trades = unique_trades
    print(f"   🔄 去重后 {len(all_trades)} 条记录", file=sys.stderr)

    # 筛选
    filtered = filter_trades(
        all_trades,
        days=args.days,
        min_amount=args.min_amount,
        politician=args.politician,
        ticker=args.ticker,
        chamber=args.chamber,
        tx_type=args.tx_type,
    )
    print(f"   🔍 筛选后 {len(filtered)} 条记录", file=sys.stderr)

    # 构建输出
    result = {
        "trades": filtered,
        "meta": {
            "fetched_at": datetime.now().isoformat(),
            "total_raw": len(all_trades),
            "total_filtered": len(filtered),
            "filters": {
                "days": args.days,
                "min_amount": args.min_amount,
                "politician": args.politician,
                "ticker": args.ticker,
                "chamber": args.chamber,
                "tx_type": args.tx_type,
            },
        },
    }

    # 分析模式
    if args.analyze:
        print("   📊 正在执行重仓分析...", file=sys.stderr)
        result["concentration"] = analyze_concentration(filtered)
        print("   🔎 正在检测异常交易...", file=sys.stderr)
        result["anomalies"] = detect_anomalies(filtered)
        print(
            f"   ✅ 发现 {len(result['concentration'])} 个被买入标的，"
            f"{len(result['anomalies'])} 条异常信号",
            file=sys.stderr,
        )

    # 输出
    if args.output:
        if args.output.endswith(".csv"):
            output_csv(filtered, args.output)
        else:
            output_json(result, args.output)
    else:
        output_json(result)


if __name__ == "__main__":
    main()
