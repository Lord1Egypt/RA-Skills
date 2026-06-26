#!/usr/bin/env python3
"""
智能搜索 - Smart Search
自动选择最佳搜索引擎：
- 中文搜索 → Bing（中文结果更精准）
- 英文搜索 → DuckDuckGo（无反爬，更稳定）
- 也支持手动指定搜索引擎

用法:
    python3 smart_search.py <搜索词> [引擎] [数量]
    
    引擎: bing (默认中文), ddg (默认英文), auto (自动选择)
"""

import os
import re
import sys
import requests
from urllib.parse import urlparse, quote
from html import unescape

# ============ 共享配置 ============
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
    'wiki': 2.0,
    'wikipedia.org': 2.5,
    'stackoverflow.com': 2.5,
    'medium.com': 1.8,
    'dev.to': 1.8,
    'csdn.net': 1.8,
    'reddit.com': 1.8,
    'youtube.com': 1.5,
    'bilibili.com': 1.5,
}

LOW_QUALITY_BING = ['baidu.com', '360.cn', 'sogou.com']
LOW_QUALITY_DDG = ['baidu.com', '360.cn', 'sogou.com', 'click.baidu.com']

def get_quality_label(score):
    if score >= 2.5: return "⭐⭐⭐【官方】"
    elif score >= 2.0: return "⭐⭐【优质】"
    elif score >= 1.0: return "⭐【普通】"
    else: return "⚠️【低质量】"

def calc_domain_score(url, engine='bing'):
    if not url:
        return 0.5
    domain = urlparse(url).netloc.lower()
    for good, score in HIGH_QUALITY.items():
        if good in domain:
            return score
    low = LOW_QUALITY_BING if engine == 'bing' else LOW_QUALITY_DDG
    for bad in low:
        if bad in domain and 'baike' not in domain:
            return 0.3
    return 1.2

def is_ad_bing(match):
    ad_patterns = [r'class="b_ad"', r'class="ads"', r'sponsored', r'广告', r'推广']
    return any(re.search(p, match, re.I) for p in ad_patterns)

def extract_desc_bing(match):
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

def extract_desc_ddg(text):
    patterns = [
        r'class="[^"]*result__snippet[^"]*"[^>]*>([^<]+)<',
        r'class="[^"]*snippet[^"]*"[^>]*>([^<]+)<',
    ]
    for p in patterns:
        m = re.search(p, text, re.I)
        if m:
            desc = unescape(m.group(1)).strip()
            if len(desc) > 15:
                return desc[:200]
    return ""

# ============ Bing 搜索 ============
def search_bing(query, num=10):
    url = f"https://cn.bing.com/search?q={quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        
        results, seen = [], []
        for m in re.findall(r'<li class="b_algo"[^>]*>(.*?)</li>', r.text, re.DOTALL):
            if is_ad_bing(m): continue
            try:
                title = unescape(re.sub(r'<[^>]+>', '', re.search(r'<h2[^>]*><a[^>]*>(.*?)</a></h2>', m).group(1))).strip()
                link = re.search(r'<a[^>]*href="([^"]+)"', m).group(1)
                if link in seen: continue
                seen.append(link)
                desc = extract_desc_bing(m)
                score = calc_domain_score(link, 'bing')
                if len(title) > 5:
                    results.append({'title': title, 'url': link, 'desc': desc, 'score': score})
            except: continue
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:num]
    except Exception as e:
        print(f"Bing搜索失败: {e}")
        return []

# ============ DuckDuckGo 搜索 ============
def search_ddg(query, num=10):
    url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.encoding = 'utf-8'
        r.raise_for_status()
        
        results, seen = [], []
        for m in re.findall(r'class="result[^"]*"[^>]*>(.*?)</div>\s*</div>', r.text, re.DOTALL):
            try:
                title_match = re.search(r'<a[^>]*class="[^"]*result__a[^"]*"[^>]*>(.*?)</a>', m, re.I)
                if not title_match: continue
                title = unescape(title_match.group(1)).strip()
                
                link_match = re.search(r'<a[^>]*href="([^"]+)"', m)
                if not link_match: continue
                link = link_match.group(1)
                
                if 'uddg=' in link:
                    import urllib.parse
                    parsed = urllib.parse.parse_qs(urllib.parse.urlparse(link).query)
                    link = parsed.get('uddg', [link])[0]
                
                if not link.startswith('http') or link in seen: continue
                seen.append(link)
                
                desc = extract_desc_ddg(m)
                score = calc_domain_score(link, 'ddg')
                
                if len(title) > 5:
                    results.append({'title': title, 'url': link, 'desc': desc, 'score': score})
            except: continue
        
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:num]
    except Exception as e:
        print(f"DuckDuckGo搜索失败: {e}")
        return []

# ============ 自动选择引擎 ============
def detect_language(query):
    """检测查询语言"""
    # 简单检测：是否包含中文字符
    if re.search(r'[\u4e00-\u9fff]', query):
        return 'zh'
    return 'en'

def smart_search(query, engine='auto', num=10):
    """智能搜索主函数"""
    if engine == 'auto':
        lang = detect_language(query)
        engine = 'bing' if lang == 'zh' else 'ddg'
        print(f"🔍 自动选择引擎: {engine.upper()} (检测语言: {'中文' if lang == 'zh' else '英文'})")
    
    if engine == 'bing':
        return search_bing(query, num), 'Bing'
    elif engine == 'ddg':
        return search_ddg(query, num), 'DuckDuckGo'
    else:
        return [], 'Unknown'

def print_res(results, query, engine):
    if not results:
        print(f"未找到: {query}")
        return
    print(f"\n🔍 {engine}搜索: {query}")
    print(f"📊 结果: {len(results)} 条\n")
    for i, r in enumerate(results, 1):
        q = get_quality_label(r['score'])
        print(f"{i}. {q}")
        print(f"   {r['title']}")
        url_display = r['url'][:70] + "..." if len(r['url']) > 70 else r['url']
        print(f"   {url_display}")
        if r['desc']:
            desc_display = r['desc'][:100] + "..." if len(r['desc']) > 100 else r['desc']
            print(f"   📝 {desc_display}")
        print()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python3 smart_search.py <搜索词> [引擎] [数量]")
        print("  引擎: bing (中文), ddg (英文), auto (自动选择，默认)")
        sys.exit(1)
    
    # 解析参数
    args = sys.argv[1:]
    query = args[0]
    engine = 'auto'
    num = 10
    
    for arg in args[1:]:
        if arg in ['bing', 'ddg', 'auto']:
            engine = arg
        elif arg.isdigit():
            num = int(arg)
    
    results, engine_name = smart_search(query, engine, num)
    print_res(results, query, engine_name)
