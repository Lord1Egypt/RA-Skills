#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证所有活动的真实截止日期
从文章详情 API 提取 Activity Period / Promotion Period 的截止日期
"""

import json
import requests
import re
import html
from datetime import datetime, timedelta, timezone
import os

# 代理配置（从环境变量读取，可选）
PROXY_URL = os.environ.get("HTTP_PROXY", "")
PROXIES = {
    "http": PROXY_URL,
    "https": PROXY_URL,
} if PROXY_URL else {}

def strip_html_tags(html_text):
    """提取 HTML 或 JSON 结构中的纯文本"""
    try:
        parsed = json.loads(html_text)
        texts = []
        def extract(node):
            if isinstance(node, dict):
                if node.get('node') == 'text':
                    text = node.get('text', '')
                    text = html.unescape(text.replace('&nbsp;', ' '))
                    texts.append(text)
                elif 'child' in node:
                    for child in node['child']:
                        extract(child)
            elif isinstance(node, list):
                for item in node:
                    extract(item)
        extract(parsed)
        text = ' '.join(texts)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    except (json.JSONDecodeError, TypeError):
        text = re.sub(r'<[^>]+>', ' ', html_text)
        text = html.unescape(text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

def get_article_details(code):
    """从文章详情 API 获取活动完整信息"""
    url = "https://www.binance.com/bapi/composite/v1/public/cms/article/detail/query"
    params = {"articleCode": code}
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10, proxies=PROXIES)
        if resp.status_code == 200:
            data = resp.json()
            body = data.get("data", {}).get("body", "")
            title = data.get("data", {}).get("title", "")
            pure_body = strip_html_tags(body)
            return {"title": title, "body": pure_body}
    except Exception as e:
        print(f"获取详情失败 {code}: {e}")
    return {"title": "", "body": ""}

def extract_end_date_from_body(body):
    """从文章正文提取 Activity Period / Promotion Period 的截止日期"""
    
    # 优先级 1: Activity Period: YYYY-MM-DD HH:MM (UTC) to YYYY-MM-DD HH:MM (UTC)
    # 支持多种分隔符：-, –, to
    # 注意：使用 .*? 而非 [^0-9]*? 以支持时间格式（如 10:30）
    period_patterns = [
        r'(?:Activity|Promotion) Period\s*:\s*(\d{4}-\d{2}-\d{2}).*?(?:to|–|-).*?(\d{4}-\d{2}-\d{2})',
        r'Activity Period:\s*(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}\s*\(UTC\)\s*(?:to|–|-)\s*(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}\s*\(UTC\)',
        r'Promotion Period:\s*(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}\s*\(UTC\)\s*(?:to|–|-)\s*(\d{4}-\d{2}-\d{2})\s+\d{2}:\d{2}\s*\(UTC\)',
    ]
    
    for pattern in period_patterns:
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            end_date = match.group(2)
            return end_date, "Activity/Promotion Period"
    
    # 优先级 2: 查找独立的日期（可能是截止日期的其他表述）
    # 格式：YYYY-MM-DD
    date_matches = re.findall(r'\b(\d{4}-\d{2}-\d{2})\b', body)
    if date_matches:
        # 取最后一个日期作为截止日期（通常是结束日期）
        return date_matches[-1], "Date Found"
    
    return "", "Not Found"

def get_binance_activities():
    """从币安 API 实时获取活动"""
    url = "https://www.binance.com/bapi/composite/v1/public/cms/article/list/query"
    params = {"type": "1", "pageNo": "1", "pageSize": "50", "catalogId": "93"}
    headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=15, proxies=PROXIES)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("code") == "000000":
                return data.get("data", {}).get("catalogs", [{}])[0].get("articles", [])
    except Exception as e:
        print(f"API 错误：{e}")
    return []

MONEY_KEYWORDS = [
    "airdrop", "空投", "alpha", "web3", "task", "任务",
    "launchpool", "挖矿", "earn", "质押", "staking", "simple earn", "理财",
    "hodler", "竞赛", "比赛", "competition", "challenge", "trading", "reward", "奖励",
    "share", "瓜分", "super", "sign", "sign protocol", "sbt", "nft 身份"
]

EXCLUDE_KEYWORDS = [
    "perpetual contract", "永续合约", "futures will launch",
    "options", "monitoring tag", "tick size",
    "pakistan", "africa", "balkans", "nigeria", "uganda", "ghana", "kenya",
    "morocco", "cameroon", "turkmenistan", "ramadan",
]

def filter_earning_activities(articles):
    """过滤赚钱相关活动"""
    earning = []
    for article in articles:
        title = article.get("title", "").lower()
        if any(kw in title for kw in EXCLUDE_KEYWORDS):
            continue
        if not any(kw in title for kw in MONEY_KEYWORDS):
            continue
        earning.append(article)
    return earning

def main():
    print("=" * 100)
    print("🔍 币安活动截止日期核实报告")
    print("=" * 100)
    print(f"查询时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 获取活动列表
    articles = get_binance_activities()
    earning_articles = filter_earning_activities(articles)
    
    # 去重
    seen_codes = set()
    unique_articles = []
    for article in earning_articles:
        code = article.get("code", "")
        if code not in seen_codes:
            seen_codes.add(code)
            unique_articles.append(article)
    
    print(f"📊 找到赚钱相关活动：{len(unique_articles)} 个")
    print()
    
    # 逐个获取详情并提取截止日期
    results = []
    for i, article in enumerate(unique_articles, 1):
        title = article.get("title", "")
        code = article.get("code", "")
        release_ts = article.get("releaseDate", 0)
        
        # 获取发布日期
        release_date = ""
        if release_ts:
            if isinstance(release_ts, str):
                release_date = release_ts
            else:
                release_dt = datetime.fromtimestamp(release_ts / 1000, tz=timezone.utc)
                release_dt_utc8 = release_dt.astimezone(timezone(timedelta(hours=8)))
                release_date = release_dt_utc8.strftime('%Y-%m-%d')
        
        print(f"[{i}/{len(unique_articles)}] 获取详情：{title[:60]}...")
        
        # 获取文章详情
        details = get_article_details(code)
        body = details.get("body", "")
        
        # 提取截止日期
        end_date, date_source = extract_end_date_from_body(body)
        
        results.append({
            "index": i,
            "title": title,
            "code": code,
            "release_date": release_date,
            "end_date": end_date,
            "date_source": date_source,
        })
        
        if end_date:
            print(f"  ✅ 截止日期：{end_date} (来源：{date_source})")
        else:
            print(f"  ⚠️ 未找到明确截止日期")
        print()
    
    # 输出完整列表
    print("=" * 100)
    print("📋 活动截止日期完整列表")
    print("=" * 100)
    print()
    
    # 按截止日期排序
    results_with_dates = [r for r in results if r["end_date"]]
    results_without_dates = [r for r in results if not r["end_date"]]
    
    try:
        results_with_dates.sort(key=lambda x: x["end_date"])
    except:
        pass
    
    print(f"✅ 已核实截止日期的活动：{len(results_with_dates)} 个")
    print(f"⚠️ 未找到明确截止日期的活动：{len(results_without_dates)} 个")
    print()
    
    # 表格输出
    print("-" * 120)
    print(f"{'序号':<4} {'截止日期':<12} {'来源':<22} {'活动名称':<80}")
    print("-" * 120)
    
    for r in results_with_dates:
        title_short = r["title"][:77] + "..." if len(r["title"]) > 80 else r["title"]
        print(f"{r['index']:<4} {r['end_date']:<12} {r['date_source']:<22} {title_short:<80}")
    
    if results_without_dates:
        print()
        print("⚠️ 未找到明确截止日期的活动：")
        for r in results_without_dates:
            title_short = r["title"][:90] if len(r["title"]) > 90 else r["title"]
            print(f"  - {title_short}")
    
    print()
    print("=" * 100)
    print("✅ 核实完成")
    print("=" * 100)
    
    # 导出到文件（使用相对路径，兼容不同环境）
    workspace_base = os.environ.get("OPENCLAW_WORKSPACE", os.path.expanduser("~/.openclaw/workspace"))
    output_file = os.path.join(workspace_base, ".binance_earning", "exports", "deadlines_verified.md")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# 币安活动截止日期核实报告\n\n")
        f.write(f"查询时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"- ✅ 已核实截止日期的活动：{len(results_with_dates)} 个\n")
        f.write(f"- ⚠️ 未找到明确截止日期的活动：{len(results_without_dates)} 个\n\n")
        f.write("## 完整列表（按截止日期排序）\n\n")
        f.write("| 序号 | 截止日期 | 来源 | 活动名称 |\n")
        f.write("|------|----------|------|----------|\n")
        for r in results_with_dates:
            f.write(f"| {r['index']} | {r['end_date']} | {r['date_source']} | {r['title']} |\n")
        if results_without_dates:
            f.write("\n## 未找到明确截止日期的活动\n\n")
            for r in results_without_dates:
                f.write(f"- {r['title']}\n")
    
    print(f"\n📁 报告已导出：{output_file}")

if __name__ == "__main__":
    main()
