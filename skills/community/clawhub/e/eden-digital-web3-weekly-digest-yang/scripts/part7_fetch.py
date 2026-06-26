#!/usr/bin/env python3
"""
Part.7 RWA 重要新闻抓取脚本
数据源：https://cryptorank.io/news/rwa
API：  https://api.cryptorank.io/v0/news?lang=en&coinKeys=rwa&withFullContent=true

特点：
  · 纯 curl + Python 标准库，无需 Playwright、无需 API Key
  · 分页拉取，覆盖过去 7 天内所有新闻
  · 按重要性评分排序，过滤稳定币噪音

运行：
  python3 scripts/part7_fetch.py
  python3 scripts/part7_fetch.py --days 7      # 最近 N 天（默认 7）
  python3 scripts/part7_fetch.py --top 12      # 最多展示 N 条（默认 12）
"""

import subprocess, sys, json, re, argparse
from datetime import datetime, timedelta, timezone

API_BASE   = 'https://api.cryptorank.io/v0/news'
SOURCE_URL = 'https://cryptorank.io/news/rwa'
PAGE_SIZE  = 20   # 每次请求条数

# ── 重要性关键词（命中越多，评分越高）─────────────────────────────────────
PRIORITY_KW = [
    'tokeniz', 'tokenise', 'real-world asset', 'rwa', 'on-chain',
    'launch', 'partner', 'integrat', 'billion', 'million',
    'regulat', 'approve', 'fund', 'bond', 'treasur', 'securit',
    'blackrock', 'franklin', 'ondo', 'centrifuge', 'maple',
    'real estate', 'backed', 'protocol', 'expand', 'pilot',
    'institution', 'defi', 'yield', 'custody', 'complian',
]
NOISE_KW = ['meme', 'airdrop', 'nft drop', 'presale', 'giveaway', 'lottery']
STABLECOIN_KW = [
    'stablecoin', 'usdt', 'usdc', 'usde', 'fdusd',
    'usd1', 'pyusd', 'dai ', ' dai', 'frax',
]

# ── 中文月份 ───────────────────────────────────────────────────────────────
def ts_to_zh(ts_ms: int) -> str:
    dt = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc)
    return f'{dt.year}年{dt.month}月{dt.day}日'

# ── 评分 ───────────────────────────────────────────────────────────────────
def score(title: str, desc: str) -> int:
    text = (title + ' ' + desc).lower()
    s = sum(1 for kw in PRIORITY_KW if kw in text)
    s -= sum(2 for kw in NOISE_KW if kw in text)
    return s

# ── curl 拉取 API ──────────────────────────────────────────────────────────
def fetch_page(offset: int, limit: int) -> list:
    url = (f'{API_BASE}?lang=en&coinKeys=rwa'
           f'&withFullContent=true&limit={limit}&offset={offset}')
    r = subprocess.run(
        ['curl', '-s', '-L', '--max-time', '15',
         '-H', 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
         '-H', 'Accept: application/json',
         '-H', 'Referer: https://cryptorank.io/',
         url],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        print(f'[WARN] curl 失败 offset={offset}: {r.stderr[:80]}', file=sys.stderr)
        return []
    try:
        data = json.loads(r.stdout)
        items = data.get('data') if isinstance(data, dict) else data
        return items if isinstance(items, list) else []
    except json.JSONDecodeError as e:
        print(f'[WARN] JSON 解析失败 offset={offset}: {e}', file=sys.stderr)
        return []

# ── 主抓取流程 ─────────────────────────────────────────────────────────────
def fetch_news(days: int = 7) -> list:
    cutoff_ms = (datetime.now(tz=timezone.utc) - timedelta(days=days)).timestamp() * 1000
    results, offset = [], 0

    while True:
        items = fetch_page(offset, PAGE_SIZE)
        print(f'[INFO] offset={offset} 拿到 {len(items)} 条', file=sys.stderr)
        if not items:
            break

        hit_old = False
        for item in items:
            ts = item.get('date', 0)
            if ts < cutoff_ms:
                hit_old = True
                break

            title = item.get('title', '')
            desc  = item.get('description', '') or ''
            url   = item.get('url', '')
            src   = item.get('source', '')
            if isinstance(src, dict):
                src = src.get('name', '')

            # 过滤稳定币
            combined = (title + ' ' + desc).lower()
            if any(kw in combined for kw in STABLECOIN_KW):
                continue

            results.append({
                'ts':    ts,
                'date':  ts_to_zh(ts),
                'title': title,
                'desc':  desc[:200].strip(),
                'url':   url,
                'source': src,
                'score': score(title, desc),
            })

        if hit_old or len(items) < PAGE_SIZE:
            break
        offset += PAGE_SIZE

    # 按评分降序，同分按时间降序
    results.sort(key=lambda x: (x['score'], x['ts']), reverse=True)
    return results

# ── 输出 ───────────────────────────────────────────────────────────────────
def print_report(news: list, days: int, top: int) -> None:
    today = datetime.now(tz=timezone.utc)
    date_str = f'{today.year}年{today.month}月{today.day}日'

    print('=' * 60)
    print('  Part.7  RWA 重要新闻')
    print(f'  数据来源：{SOURCE_URL}')
    print(f'  覆盖范围：近 {days} 天  /  抓取时间：{date_str}')
    print('=' * 60)

    if not news:
        print('\n[⚠️] 未抓取到符合条件的 RWA 新闻。')
        print('可能原因：网络限制 / API 参数变更 / 本周 RWA 新闻较少')
        return

    shown = news[:top]
    for i, item in enumerate(shown, 1):
        src_str = f'  来源：{item["source"]}' if item['source'] else ''
        print(f'\n【{i}】{item["title"]}')
        print(f'  日期：{item["date"]}{src_str}')
        if item['desc']:
            # 清理 description 中的重复标题前缀
            desc = re.sub(r'^.*?\n\n', '', item['desc']).strip()
            if not desc:
                desc = item['desc']
            print(f'  摘要：{desc[:180]}')
        print(f'  链接：{item["url"]}')
        print(f'  点评：⚠️（AI 根据标题与摘要生成背景解读）')

    print(f'\n共展示 {len(shown)} 条重要 RWA 新闻（已过滤稳定币相关，按重要性排序）')
    if len(news) > top:
        print(f'（另有 {len(news) - top} 条次要新闻未展示）')

# ── 入口 ───────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description='抓取 Cryptorank RWA 新闻')
    parser.add_argument('--days', type=int, default=7,  help='最近几天（默认 7）')
    parser.add_argument('--top',  type=int, default=12, help='最多展示几条（默认 12）')
    args = parser.parse_args()

    print(f'[INFO] 抓取近 {args.days} 天 RWA 新闻...', file=sys.stderr)
    news = fetch_news(days=args.days)
    print(f'[INFO] 过滤后共 {len(news)} 条', file=sys.stderr)
    print_report(news, args.days, args.top)

if __name__ == '__main__':
    main()
