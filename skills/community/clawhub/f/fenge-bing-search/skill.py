#!/usr/bin/env python3
"""
Bing Web Search - 高精准版
- 质量标签（官方/优质/普通/低质量）
- 提取描述摘要
- 高质量来源优先
- 广告过滤
"""

import os
import re
import sys
import requests
from urllib.parse import urlparse, quote
from html import unescape

# 高质量来源权重
HIGH_QUALITY = {
    'github.com': 3.0,
    'docs.openclaw.ai': 3.0,
    'docs': 2.5,
    'official': 2.5,
    'zhihu.com': 2.0,
    'juejin.cn': 2.0,
    'cnblogs.com': 2.0,
    'segmentfault.com': 2.0,
    'runoob.com': 2.0,
    'baike.baidu.com': 1.5,
}

LOW_QUALITY = ['baidu.com', '360.cn', 'sogou.com']

def get_quality_label(score):
    if score >= 2.5: return "⭐⭐⭐【官方】"
    elif score >= 2.0: return "⭐⭐【优质】"
    elif score >= 1.0: return "⭐【普通】"
    else: return "⚠️【低质量】"

def calc_domain_score(url):
    domain = urlparse(url).netloc.lower()
    for good, score in HIGH_QUALITY.items():
        if good in domain: return score
    for bad in LOW_QUALITY:
        if bad in domain and 'baike' not in domain: return 0.3
    return 1.0

def is_ad(match):
    ad_patterns = [r'class="b_ad"', r'class="ads"', r'sponsored', r'广告', r'推广']
    return any(re.search(p, match, re.I) for p in ad_patterns)

def extract_desc(match):
    for p in [r'<p[^>]*class="[^"]*b_desc[^"]*"[^>]*>(.*?)</p>',
                r'<p class="[^"]*b_caption[^"]*"[^>]*>(.*?)</p>',
                r'<p[^>]*>(.*?)</p>']:
        m = re.search(p, match, re.DOTALL)
        if m:
            desc = re.sub(r'<[^>]+>', '', m.group(1))
            desc = unescape(desc).strip()
            if len(desc) > 20:
                return desc[:200]
    return ""

def search(query, num=10):
    url = f"https://cn.bing.com/search?q={quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        
        results, seen = [], set()
        for m in re.findall(r'<li class="b_algo"[^>]*>(.*?)</li>', r.text, re.DOTALL):
            if is_ad(m): continue
            try:
                title = unescape(re.sub(r'<[^>]+>', '', re.search(r'<h2[^>]*><a[^>]*>(.*?)</a></h2>', m).group(1))).strip()
                link = re.search(r'<a[^>]*href="([^"]+)"', m).group(1)
                if link in seen: continue
                seen.add(link)
                desc = extract_desc(m)
                score = calc_domain_score(link)
                if len(title) > 5:
                    results.append({'title': title, 'url': link, 'desc': desc, 'score': score})
            except: continue
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:num]
    except Exception as e:
        print(f"搜索失败: {e}")
        return []

def print_res(results, query):
    if not results:
        print(f"未找到: {query}")
        return
    print(f"\n🔍 搜索: {query}")
    print(f"📊 结果: {len(results)} 条\n")
    for i, r in enumerate(results, 1):
        q = get_quality_label(r['score'])
        print(f"{i}. {q}")
        print(f"   {r['title']}")
        print(f"   {r['url'][:70]}...")
        if r['desc']:
            print(f"   📝 {r['desc'][:100]}...")
        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 bing_search.py <搜索词> [数量]")
        sys.exit(1)
    q = " ".join(sys.argv[1:])
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    print_res(search(q, n), q)
