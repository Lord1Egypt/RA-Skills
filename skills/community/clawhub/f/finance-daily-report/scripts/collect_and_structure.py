#!/usr/bin/env python3
"""
Finance Daily Report — Full Collector Pipeline (v2.1)

Supports:
1. 9 modules with optimized data fetching (shared sources)
2. Single module re-collection via --module parameter
3. LLM extraction with precise prompts per module
4. Fallback from kimi to doubao on errors
5. Jin10 API integration for real article URLs

Usage:
    # Full collection
    python3 collect_and_structure.py --date 2026-03-13
    
    # Single module re-collection
    python3 collect_and_structure.py --date 2026-03-13 --module fx_usd

Output: JSON with structured report data to stdout.
"""

import json
import os
import sys
import urllib.request
import urllib.error
import re
import argparse
from datetime import datetime, timedelta

# ── Model configs (keys from environment variables) ──
PRIMARY = {
    "name": "kimi-k2.5",
    "url": "https://coding.dashscope.aliyuncs.com/v1/chat/completions",
    "key": os.environ.get("DASHSCOPE_API_KEY", ""),
    "model": "kimi-k2.5",
}

BACKUP = {
    "name": "doubao-seed-mini",
    "url": "https://ark.cn-beijing.volces.com/api/v3/chat/completions",
    "key": os.environ.get("DOUBAO_API_KEY", ""),
    "model": "doubao-seed-2-0-mini-260215",
}

# ── Data sources ──
SOURCES = {
    "trading_stocks": "https://tradingeconomics.com/stocks",
    "trading_currencies": "https://tradingeconomics.com/currencies",
    "trading_commodities": "https://tradingeconomics.com/commodities",
    "trading_bonds": "https://tradingeconomics.com/bonds",
    # jin10 is fetched via API (fetch_jin10_api), not this URL
    "cls": "https://www.cls.cn/",
    "eastmoney": "https://www.eastmoney.com/",
}

# Jin10 API endpoint — returns structured JSON with article IDs and source_link
JIN10_API_URL = "https://www.jin10.com/flash_newest.js"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "identity",
    "Referer": "https://www.jin10.com/",
}


def fetch_url(url, max_chars=10000, timeout=15):
    """Fetch URL and return structured text from HTML."""
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
            return extract_te_data(raw, max_chars)
    except Exception as e:
        return f"FETCH_ERROR: {e}"


def fetch_jin10_api(max_items=80, timeout=15):
    """Fetch Jin10 news via API. Returns list of structured news items with URLs.
    
    Each item has:
    - id: unique article ID
    - time: publish time
    - content: news text
    - source: source name
    - url: article URL (source_link if available, else jin10 newsflash URL)
    """
    req = urllib.request.Request(JIN10_API_URL, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace").strip()
            # Remove JS variable prefix: "var newest = [...]; "
            raw = re.sub(r'^var\s+newest\s*=\s*', '', raw).rstrip(';').strip()
            data = json.loads(raw)
            
            items = []
            for entry in data[:max_items]:
                article_id = entry.get("id", "")
                time_str = entry.get("time", "")
                d = entry.get("data", {})
                content = d.get("content", "").strip()
                source_name = d.get("source", "")
                source_link = d.get("source_link", "")
                
                # Build URL: prefer original source_link, fallback to jin10 newsflash page
                if source_link and source_link.startswith("http"):
                    article_url = source_link
                elif article_id:
                    article_url = f"https://www.jin10.com/newsflash/{article_id}.html"
                else:
                    article_url = "https://www.jin10.com/"
                
                items.append({
                    "id": article_id,
                    "time": time_str,
                    "content": content,
                    "source": source_name,
                    "url": article_url,
                })
            return items
    except Exception as e:
        print(f"  Jin10 API error: {e}", file=sys.stderr)
        return []


def format_jin10_for_llm(items, max_chars=8000):
    """Format jin10 items as text for LLM prompt. Each line has URL."""
    lines = []
    for item in items:
        if not item.get("content"):
            continue
        line = f"[{item['time']}] {item['content']}"
        if item.get("source"):
            line += f" 【来源：{item['source']}】"
        line += f" | URL: {item['url']}"
        lines.append(line)
    
    result = "\n".join(lines)
    return result[:max_chars]


def extract_te_data(html, max_chars=10000):
    """Extract structured data from Trading Economics HTML tables.
    TE uses <tr data-symbol="..."> rows with <td> cells for price/change."""
    rows = []
    # Find all table rows with data-symbol
    for match in re.finditer(
        r'<tr[^>]*data-symbol="([^"]*)"[^>]*>(.*?)</tr>',
        html, re.DOTALL
    ):
        symbol = match.group(1)
        row_html = match.group(2)
        # Extract all <td> values
        cells = re.findall(r'<td[^>]*>\s*(.*?)\s*</td>', row_html, re.DOTALL)
        # Clean cell values
        clean_cells = []
        for cell in cells:
            val = re.sub(r'<[^>]+>', '', cell).strip()
            if val:
                clean_cells.append(val)
        if clean_cells:
            rows.append(f"{symbol}: {' | '.join(clean_cells)}")
    
    if rows:
        result = "\n".join(rows)
        return result[:max_chars]
    
    # Fallback: basic text extraction
    text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
    text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:max_chars]


def call_llm(config, prompt, timeout=120):
    """Call LLM API and return content string."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['key']}",
    }
    payload = {
        "model": config["model"],
        "messages": [
            {"role": "system", "content": (
                "你是金融数据采集助手。从原始网页数据中提取结构化信息。"
                "只输出纯 JSON，不要用 ```json 包裹，不要多余文字。"
                "数据缺失用 null，不要编造。"
                "所有来源 URL 必须保留原始链接。"
            )},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.1,
        "max_tokens": 6000,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(config["url"], data=data, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['key']}",
    }, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            content = body.get("choices", [{}])[0].get("message", {}).get("content", "")
            tokens = body.get("usage", {}).get("total_tokens", 0)
            return content, tokens
    except Exception as e:
        return f"LLM_ERROR: {e}", 0


def call_with_fallback(prompt):
    """Try primary, fallback to backup."""
    content, tokens = call_llm(PRIMARY, prompt)
    if not content.startswith("LLM_ERROR"):
        return content, tokens, PRIMARY["name"]
    
    print(f"  Primary failed, trying backup...", file=sys.stderr)
    content, tokens = call_llm(BACKUP, prompt)
    return content, tokens, BACKUP["name"]


def parse_json(text):
    """Extract JSON from text that might have markdown wrapping."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
    
    # Try finding array
    start = text.find("[")
    end = text.rfind("]") + 1
    if start >= 0 and end > start:
        try:
            return json.loads(text[start:end])
        except json.JSONDecodeError:
            pass
    
    return None


# ── Module-specific extraction functions ──

def extract_market_theme(raw_jin10, raw_cls, date):
    """Extract market theme from jin10 + cls data."""
    prompt = f"""从以下金十数据快讯和财联社页面提取 {date} 的市场核心主线叙事。

金十数据每条新闻末尾都有"| URL: ..."，这是该条新闻的具体链接，请在引用时保留。

要求：
1. 只提取 2-3 个核心主线，每个主线 50-80 字
2. 主线必须是当日市场最核心的驱动因素（如：美联储政策预期、地缘冲突、重要经济数据）
3. main_theme 字段是 200-300 字的整体叙事总结
4. 不要混入具体新闻事件或明日前瞻

返回 JSON：
{{"main_theme": "当日市场核心叙事（200-300 字）", "themes": ["主线 1（50-80 字）", "主线 2（50-80 字）"]}}

金十数据快讯（含具体 URL）：
{raw_jin10[:6000]}

财联社原始内容（前 3000 字符）：
{raw_cls[:3000]}"""
    
    content, tokens, model = call_with_fallback(prompt)
    parsed = parse_json(content)
    return parsed, tokens, model


def extract_global_macro(raw_jin10, raw_cls, date):
    """Extract global macro data from jin10 + cls."""
    prompt = f"""从以下金十数据快讯和财联社页面提取 {date} 的全球宏观经济数据和政策事件。

金十数据每条新闻末尾都有"| URL: ..."，这是该条新闻的具体链接，提取新闻时必须把对应 URL 放入 source_url 字段。

要求：
1. 分四个子板块：美国(us)、欧洲(europe)、亚太(asia_pacific)、地缘政治(geopolitics)
2. 每个子板块提取 2-4 条关键数据或事件
3. 每条包含：事件描述、数据值（如有）、来源名称、来源 URL（从"| URL: ..."提取）
4. 宏观数据包括：GDP、CPI、就业、PMI、央行政策声明等

返回 JSON：
{{"us": [...], "europe": [...], "asia_pacific": [...], "geopolitics": [...]}}
每个子数组元素格式：{{"text": "事件描述", "value": "数据值或 null", "source": "来源名称", "source_url": "https://..."}}

金十数据快讯（含具体 URL）：
{raw_jin10[:6000]}

财联社原始内容（前 3000 字符）：
{raw_cls[:3000]}"""
    
    content, tokens, model = call_with_fallback(prompt)
    parsed = parse_json(content)
    return parsed, tokens, model


def extract_fx_usd(raw_te_currencies, date):
    """Extract FX data from Trading Economics."""
    prompt = f"""从以下 Trading Economics 汇率页面数据中提取 {date} 的汇率信息：
DXY 美元指数、EUR/USD、GBP/USD、USD/JPY、USD/CNY、AUD/USD、USD/BRL、USD/KRW

返回 JSON：
{{"fx": [{{"name": "DXY 美元指数", "price": "100.495", "change_pct": "+0.76%", "monthly_pct": "+3.69%", "source_url": "https://tradingeconomics.com/united-states/currency"}}]}}

每个货币对的 source_url 必须是 Trading Economics 上对应页面的具体 URL。

原始数据（前 5000 字符）：
{raw_te_currencies[:5000]}"""
    
    content, tokens, model = call_with_fallback(prompt)
    parsed = parse_json(content)
    return parsed, tokens, model


def extract_rates_bonds(raw_te_bonds, date):
    """Extract bond yields from Trading Economics."""
    prompt = f"""从以下 Trading Economics 国债页面数据中提取 {date} 的全球主要国家 10Y 国债收益率：
美国、英国、德国、日本、法国、意大利、加拿大、中国

返回 JSON：
{{"bonds": [{{"country": "美国", "yield_10y": "4.282%", "day_change": "+0.013", "monthly_change": "+0.23%", "source_url": "https://tradingeconomics.com/united-states/government-bond-yield"}}]}}

每个国家的 source_url 必须是 Trading Economics 上该国国债的具体页面 URL。

原始数据（前 4000 字符）：
{raw_te_bonds[:4000]}"""
    
    content, tokens, model = call_with_fallback(prompt)
    parsed = parse_json(content)
    return parsed, tokens, model


def extract_equities(raw_te_stocks, date):
    """Extract stock indices from Trading Economics."""
    prompt = f"""从以下 Trading Economics 股市页面原始数据中提取 {date} 的股指信息：
标普 500(US500)、道琼斯 (US30)、纳斯达克 100(US100)、上证综指 (SHANGHAI)、沪深 300(CSI 300)、
恒生指数 (HK50)、日经 225(JP225)、印度 SENSEX、DAX(DE40)、富时 100(GB100)、法国 CAC40(FR40)、台湾加权 (TSI)

返回 JSON：
{{"stocks": [{{"name": "标普 500", "code": "US500", "price": "6632.19", "change_pct": "-0.61%", "monthly_pct": "-3.08%", "source_url": "https://tradingeconomics.com/united-states/stock-market"}}]}}

每个股指的 source_url 必须是 Trading Economics 上该国家股市的具体页面 URL。

原始数据（前 6000 字符）：
{raw_te_stocks[:6000]}"""
    
    content, tokens, model = call_with_fallback(prompt)
    parsed = parse_json(content)
    return parsed, tokens, model


def extract_commodities(raw_te_commodities, date):
    """Extract commodity prices from Trading Economics."""
    prompt = f"""从以下 Trading Economics 商品页面数据中提取 {date} 的商品价格：
WTI 原油 (Crude Oil)、布伦特原油 (Brent)、黄金 (Gold)、白银 (Silver)、铜 (Copper)、
铁矿石 (Iron Ore)、天然气 (Natural gas)、小麦 (Wheat)、铂金 (Platinum)

返回 JSON：
{{"commodities": [{{"name": "WTI 原油", "price": "98.71", "unit": "USD/Bbl", "change_pct": "+3.11%", "monthly_pct": "+58.37%", "source_url": "https://tradingeconomics.com/commodity/crude-oil"}}]}}

每个商品的 source_url 必须是 Trading Economics 上该商品的具体页面 URL。

原始数据（前 5000 字符）：
{raw_te_commodities[:5000]}"""
    
    content, tokens, model = call_with_fallback(prompt)
    parsed = parse_json(content)
    return parsed, tokens, model


def extract_china_market(raw_jin10, raw_cls, raw_eastmoney, date):
    """Extract China market and liquidity data."""
    prompt = f"""从以下金十数据快讯和财联社页面提取 {date} 的中国市场与流动性数据。

金十数据每条新闻末尾都有"| URL: ..."，这是该条新闻的具体链接，提取政策新闻时必须把对应 URL 放入 source_url 字段。

要求提取以下内容：
1. liquidity（流动性）：央行 OMO（逆回购/MLF 操作）、Shibor、DR007、北向资金净流入、两融余额、A 股成交额
2. policy（政策）：当日发布的金融/经济政策、监管动态，每条必须带 source_url
3. a_shares（A 股概览）：上证/深证/创业板涨跌幅、涨跌家数、涨停/跌停家数

返回 JSON：
{{
  "liquidity": [{{"item": "央行逆回购", "value": "净投放 500 亿元", "note": "7 天期"}}],
  "policy": [{{"text": "政策内容", "source": "来源名称", "source_url": "https://..."}}],
  "a_shares": {{"shanghai": {{"change_pct": "+0.5%"}}, "shenzhen": {{}}, "chinext": {{}}, "advancers": 2500, "decliners": 1800, "limit_up": 45, "limit_down": 3}}
}}

金十数据快讯（含具体 URL）：
{raw_jin10[:5000]}

财联社原始内容（前 3000 字符）：
{raw_cls[:3000]}

东方财富原始内容（前 3000 字符）：
{raw_eastmoney[:3000]}"""
    
    content, tokens, model = call_with_fallback(prompt)
    parsed = parse_json(content)
    return parsed, tokens, model


def extract_sector_news(raw_jin10, raw_cls, date):
    """Extract sector/industry news from jin10 + cls."""
    prompt = f"""从以下金十数据快讯和财联社页面提取 {date} 的行业热点新闻。

金十数据每条新闻末尾都有"| URL: ..."，这是该条新闻的具体链接，每条新闻的 source_url 必须从这里提取。

要求：
1. 只提取具体行业事件：监管政策/处罚、新产品发布、公司重大事件（并购/重组/业绩）、行业数据发布
2. 每条必须标注所属行业（如：科技、医药、金融、地产、消费、新能源等）
3. 每条必须包含具体 source_url（从"| URL: ..."提取，不要填写域名首页）
4. 返回 8-15 条重要新闻

返回 JSON：
{{"news": [{{"text": "新闻内容（20-40 字）", "sector": "行业名称", "source_url": "https://www.jin10.com/newsflash/..."}}]}}

金十数据快讯（含具体 URL）：
{raw_jin10[:5000]}

财联社原始内容（前 4000 字符）：
{raw_cls[:4000]}"""
    
    content, tokens, model = call_with_fallback(prompt)
    parsed = parse_json(content)
    return parsed, tokens, model


def extract_tomorrow_preview(raw_cls, raw_jin10, date, tomorrow_date):
    """Extract tomorrow's preview events from cls + jin10."""
    prompt = f"""从以下金十数据快讯和财联社页面提取 {tomorrow_date} 的财经日历事件（明日前瞻）。

金十数据每条新闻末尾都有"| URL: ..."，这是该条新闻的具体链接，提取事件时把对应 URL 放入 source_url 字段。

要求：
1. 只提取已确认的官方日历事件（数据发布、央行会议、重要公司财报等）
2. 禁止推测或编写未确认的事件
3. 每条包含具体时间、事件描述、来源 URL
4. 返回 5-10 条重要事件

返回 JSON：
{{"events": [{{"time": "09:30", "event": "中国 CPI 同比数据发布", "source_url": "https://www.jin10.com/newsflash/..."}}]}}

金十数据快讯（含具体 URL）：
{raw_jin10[:4000]}

财联社原始内容（前 5000 字符）：
{raw_cls[:5000]}"""
    
    content, tokens, model = call_with_fallback(prompt)
    parsed = parse_json(content)
    return parsed, tokens, model


def main():
    parser = argparse.ArgumentParser(description="Finance Daily Report Collector")
    parser.add_argument("--date", default=None, help="T-1 trading day date YYYY-MM-DD")
    parser.add_argument("--module", default=None, 
                        choices=["market_theme", "global_macro", "fx_usd", "rates_bonds", 
                                 "equities", "commodities", "china_market", "sector_news", 
                                 "tomorrow_preview"],
                        help="Single module to re-collect (optional)")
    args = parser.parse_args()

    if not args.date:
        # Auto-determine T-1 trading day
        today = datetime.now()
        d = today - timedelta(days=1)
        while d.weekday() >= 5:  # Saturday=5, Sunday=6
            d -= timedelta(days=1)
        args.date = d.strftime("%Y-%m-%d")

    tomorrow = (datetime.strptime(args.date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"Report date: {args.date}", file=sys.stderr)
    if args.module:
        print(f"Single module mode: {args.module}", file=sys.stderr)
    
    total_tokens = 0
    last_model = "kimi-k2.5"
    
    # ── Step 1: Fetch raw data (optimized: shared sources) ──
    print("Step 1: Fetching raw data...", file=sys.stderr)
    raw_data = {}
    
    # Determine which sources to fetch based on module filter
    needs_jin10 = args.module is None or args.module in [
        "market_theme", "global_macro", "china_market", "sector_news", "tomorrow_preview"
    ]
    needs_cls = args.module is None or args.module in [
        "market_theme", "global_macro", "china_market", "sector_news", "tomorrow_preview"
    ]
    needs_eastmoney = args.module is None or args.module == "china_market"
    
    te_sources_needed = set()
    if args.module is None:
        te_sources_needed = {"trading_stocks", "trading_currencies", "trading_commodities", "trading_bonds"}
    else:
        mapping = {
            "fx_usd": "trading_currencies",
            "rates_bonds": "trading_bonds",
            "equities": "trading_stocks",
            "commodities": "trading_commodities",
        }
        if args.module in mapping:
            te_sources_needed.add(mapping[args.module])
    
    # Fetch Jin10 via API (structured JSON with URLs)
    if needs_jin10:
        print("  Fetching jin10 API...", file=sys.stderr)
        jin10_items = fetch_jin10_api(max_items=100)
        raw_data["jin10"] = format_jin10_for_llm(jin10_items)
        print(f"  jin10: OK ({len(jin10_items)} items, {len(raw_data['jin10'])} chars)", file=sys.stderr)
    
    # Fetch CLS homepage HTML
    if needs_cls:
        print("  Fetching cls...", file=sys.stderr)
        raw_data["cls"] = fetch_url(SOURCES["cls"])
        status = "OK" if not raw_data["cls"].startswith("FETCH_ERROR") else "FAILED"
        print(f"  cls: {status} ({len(raw_data['cls'])} chars)", file=sys.stderr)
    
    # Fetch Eastmoney
    if needs_eastmoney:
        print("  Fetching eastmoney...", file=sys.stderr)
        raw_data["eastmoney"] = fetch_url(SOURCES["eastmoney"])
        status = "OK" if not raw_data["eastmoney"].startswith("FETCH_ERROR") else "FAILED"
        print(f"  eastmoney: {status} ({len(raw_data['eastmoney'])} chars)", file=sys.stderr)
    
    # Fetch Trading Economics pages
    for key in te_sources_needed:
        url = SOURCES[key]
        print(f"  Fetching {key}...", file=sys.stderr)
        raw_data[key] = fetch_url(url)
        status = "OK" if not raw_data[key].startswith("FETCH_ERROR") else "FAILED"
        print(f"  {key}: {status} ({len(raw_data[key])} chars)", file=sys.stderr)

    # ── Step 2: Extract modules ──
    modules = {}
    
    # Define module extraction order and dependencies
    module_extractors = {
        "market_theme": lambda: extract_market_theme(
            raw_data.get("jin10", ""), raw_data.get("cls", ""), args.date),
        "global_macro": lambda: extract_global_macro(
            raw_data.get("jin10", ""), raw_data.get("cls", ""), args.date),
        "fx_usd": lambda: extract_fx_usd(
            raw_data.get("trading_currencies", ""), args.date),
        "rates_bonds": lambda: extract_rates_bonds(
            raw_data.get("trading_bonds", ""), args.date),
        "equities": lambda: extract_equities(
            raw_data.get("trading_stocks", ""), args.date),
        "commodities": lambda: extract_commodities(
            raw_data.get("trading_commodities", ""), args.date),
        "china_market": lambda: extract_china_market(
            raw_data.get("jin10", ""), raw_data.get("cls", ""),
            raw_data.get("eastmoney", ""), args.date),
        "sector_news": lambda: extract_sector_news(
            raw_data.get("jin10", ""), raw_data.get("cls", ""), args.date),
        "tomorrow_preview": lambda: extract_tomorrow_preview(
            raw_data.get("cls", ""), raw_data.get("jin10", ""), args.date, tomorrow),
    }
    
    modules_to_run = [args.module] if args.module else list(module_extractors.keys())
    
    print(f"\nStep 2: Extracting modules...", file=sys.stderr)
    for module_id in modules_to_run:
        print(f"  Extracting {module_id}...", file=sys.stderr)
        extractor = module_extractors[module_id]
        parsed, tokens, model = extractor()
        total_tokens += tokens
        last_model = model
        print(f"    Model: {model}, Tokens: {tokens}", file=sys.stderr)
        
        if parsed:
            modules[module_id] = parsed
        else:
            # Return error structure
            modules[module_id] = {"error": "parse_failed"}

    # ── Build output ──
    report = {
        "date": args.date,
        "generated_at": datetime.now().isoformat(),
        "total_tokens": total_tokens,
        "collector_model": last_model,
        "modules": modules,
    }

    # ── Output ──
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"\nDone! Total tokens: {total_tokens}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)
