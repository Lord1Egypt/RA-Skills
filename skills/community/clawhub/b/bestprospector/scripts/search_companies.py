#!/usr/bin/env python3
"""
搜索潜在客户公司
智能多搜索引擎：自动检测可用引擎、失败自动切换、多引擎汇总
支持代理设置
"""

import argparse
import json
import re
import time
import random
import sys
import os
from urllib.parse import quote, urlparse, unquote
import requests
from bs4 import BeautifulSoup

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
]

EXCLUDE_DOMAINS = [
    'google.com', 'bing.com', 'baidu.com', 'youtube.com', 'facebook.com',
    'twitter.com', 'x.com', 'linkedin.com', 'instagram.com', 'tiktok.com', 
    'weibo.com', 'zhihu.com', 'taobao.com', 'jd.com', 'tmall.com', 'amazon.com',
    'github.com', 'gitlab.com', 'gitee.com', 'csdn.net', 'juejin.cn',
    'duckduckgo.com', 'wikipedia.org', 'medium.com', 'reddit.com',
    'pinterest.com', 'tumblr.com', 'quora.com', 'stackoverflow.com',
    'sogou.com', 'so.com', '360.cn', 'baike.baidu.com',
]

PROXIES = None
AVAILABLE_ENGINES = {}

SEARCH_ENGINES = {
    'baidu': {
        'name': '百度',
        'test_url': 'https://www.baidu.com',
        'priority': 1,
        'description': '中国最大搜索引擎，适合搜索中文内容'
    },
    'sogou': {
        'name': '搜狗',
        'test_url': 'https://www.sogou.com',
        'priority': 2,
        'description': '中国搜索引擎，支持微信搜索'
    },
    'so': {
        'name': '360搜索',
        'test_url': 'https://www.so.com',
        'priority': 3,
        'description': '360搜索引擎，中国可用'
    },
    'duckduckgo': {
        'name': 'DuckDuckGo',
        'test_url': 'https://duckduckgo.com',
        'priority': 4,
        'description': '注重隐私的搜索引擎，全球可用'
    },
    'searx': {
        'name': 'Searx',
        'test_url': 'https://searx.be',
        'priority': 5,
        'description': '开源元搜索引擎，聚合多个搜索结果'
    },
    'bing': {
        'name': 'Bing',
        'test_url': 'https://www.bing.com',
        'priority': 6,
        'description': '微软搜索引擎，结果质量较好'
    },
    'google': {
        'name': 'Google',
        'test_url': 'https://www.google.com',
        'priority': 7,
        'description': '全球最大搜索引擎，结果质量最高（部分地区需要代理）'
    },
}


def init_proxies():
    global PROXIES
    http_proxy = os.environ.get('HTTP_PROXY') or os.environ.get('http_proxy')
    https_proxy = os.environ.get('HTTPS_PROXY') or os.environ.get('https_proxy')
    all_proxy = os.environ.get('ALL_PROXY') or os.environ.get('all_proxy')
    
    if https_proxy:
        PROXIES = {'http': https_proxy, 'https': https_proxy}
    elif http_proxy:
        PROXIES = {'http': http_proxy, 'https': http_proxy}
    elif all_proxy:
        PROXIES = {'http': all_proxy, 'https': all_proxy}
    
    if PROXIES:
        print(f"Using proxy: {PROXIES.get('https', 'N/A')}", file=sys.stderr)
    
    return PROXIES


def get_random_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }


def is_valid_domain(domain):
    if not domain or len(domain) < 4:
        return False
    if '.' not in domain:
        return False
    for exclude in EXCLUDE_DOMAINS:
        if exclude in domain:
            return False
    return True


def clean_company_name(title):
    title = re.sub(r'\s*[-|]\s*.*$', '', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title


def test_engine_availability(engine_key):
    """测试单个搜索引擎是否可用"""
    engine = SEARCH_ENGINES.get(engine_key)
    if not engine:
        return False
    
    try:
        response = requests.get(
            engine['test_url'],
            headers=get_random_headers(),
            timeout=5,
            proxies=PROXIES
        )
        return response.status_code == 200
    except:
        return False


def detect_available_engines():
    """检测所有可用的搜索引擎"""
    global AVAILABLE_ENGINES
    print("正在检测可用的搜索引擎...", file=sys.stderr)
    
    available = {}
    for engine_key, engine_info in SEARCH_ENGINES.items():
        is_available = test_engine_availability(engine_key)
        engine_info['available'] = is_available
        available[engine_key] = engine_info
        status = "✓ 可用" if is_available else "✗ 不可用"
        print(f"  {engine_info['name']}: {status}", file=sys.stderr)
    
    AVAILABLE_ENGINES = available
    return available


def get_sorted_engines():
    """获取按优先级排序的可用引擎列表"""
    available = [k for k, v in AVAILABLE_ENGINES.items() if v.get('available', False)]
    return sorted(available, key=lambda x: SEARCH_ENGINES[x]['priority'])


def google_search(query, limit=50):
    """Google搜索"""
    results = []
    url = f"https://www.google.com/search?q={quote(query)}&num={min(limit, 100)}&hl=zh-CN"
    
    try:
        headers = get_random_headers()
        headers['Accept-Language'] = 'en-US,en;q=0.9'
        
        response = requests.get(url, headers=headers, timeout=15, proxies=PROXIES)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for div in soup.select('div.g'):
            title_elem = div.select_one('h3')
            link_elem = div.select_one('a')
            snippet_elem = div.select_one('div.VwiC3b') or div.select_one('div[data-sncf]')
            
            if title_elem and link_elem:
                link = link_elem.get('href', '')
                domain = urlparse(link).netloc.replace('www.', '')
                
                if is_valid_domain(domain):
                    results.append({
                        'name': clean_company_name(title_elem.text),
                        'domain': domain,
                        'url': link,
                        'description': snippet_elem.text if snippet_elem else '',
                        'source': 'google'
                    })
                
                if len(results) >= limit:
                    break
                    
    except Exception as e:
        print(f"Google search error: {e}", file=sys.stderr)
    
    return results


def duckduckgo_search(query, limit=50):
    """DuckDuckGo搜索"""
    results = []
    url = f"https://html.duckduckgo.com/html/?q={quote(query)}"
    
    try:
        headers = get_random_headers()
        headers['Referer'] = 'https://duckduckgo.com/'
        
        response = requests.get(url, headers=headers, timeout=15, proxies=PROXIES)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for result in soup.select('.result'):
            title_elem = result.select_one('.result__a')
            snippet_elem = result.select_one('.result__snippet')
            
            if title_elem:
                href = title_elem.get('href', '')
                
                if 'uddg=' in href:
                    actual_url = unquote(href.split('uddg=')[1].split('&')[0])
                else:
                    actual_url = href
                
                domain = urlparse(actual_url).netloc.replace('www.', '')
                
                if is_valid_domain(domain):
                    results.append({
                        'name': clean_company_name(title_elem.text),
                        'domain': domain,
                        'url': actual_url,
                        'description': snippet_elem.text if snippet_elem else '',
                        'source': 'duckduckgo'
                    })
                
                if len(results) >= limit:
                    break
                    
    except Exception as e:
        print(f"DuckDuckGo search error: {e}", file=sys.stderr)
    
    return results


def bing_search(query, limit=50):
    """Bing搜索"""
    results = []
    url = f"https://www.bing.com/search?q={quote(query)}&count={min(limit, 50)}&setlang=en&cc=us"
    
    try:
        headers = get_random_headers()
        headers['Accept-Language'] = 'en-US,en;q=0.9'
        headers['Cookie'] = 'SRCHHPGUSR=SRCHLANG=en; _EDGE_S=ui=en-us; _EDGE_V=1;'
        
        response = requests.get(url, headers=headers, timeout=15, proxies=PROXIES)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for li in soup.select('li.b_algo'):
            title_elem = li.select_one('h2')
            link_elem = li.select_one('a')
            snippet_elem = li.select_one('p') or li.select_one('.b_caption p')
            
            if title_elem and link_elem:
                href = link_elem.get('href', '')
                
                if href.startswith('/ck/a?'):
                    continue
                
                domain = urlparse(href).netloc.replace('www.', '')
                
                if is_valid_domain(domain):
                    results.append({
                        'name': clean_company_name(title_elem.text),
                        'domain': domain,
                        'url': href,
                        'description': snippet_elem.text if snippet_elem else '',
                        'source': 'bing'
                    })
                    
    except Exception as e:
        print(f"Bing search error: {e}", file=sys.stderr)
    
    return results


def baidu_search(query, limit=50):
    """百度搜索"""
    results = []
    url = f"https://www.baidu.com/s?wd={quote(query)}&rn={min(limit, 50)}"
    
    try:
        headers = get_random_headers()
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        headers['Cache-Control'] = 'max-age=0'
        
        response = requests.get(url, headers=headers, timeout=15, proxies=PROXIES)
        
        if '安全验证' in response.text or len(response.text) < 2000:
            return results
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for div in soup.select('div.result'):
            title_elem = div.select_one('h3')
            link_elem = div.select_one('a')
            
            if title_elem and link_elem:
                link = link_elem.get('href', '')
                domain = urlparse(link).netloc.replace('www.', '')
                
                if is_valid_domain(domain):
                    results.append({
                        'name': clean_company_name(title_elem.text),
                        'domain': domain,
                        'url': link,
                        'description': '',
                        'source': 'baidu'
                    })
                
                if len(results) >= limit:
                    break
                    
    except Exception as e:
        print(f"Baidu search error: {e}", file=sys.stderr)
    
    return results


def sogou_search(query, limit=50):
    """搜狗搜索"""
    results = []
    url = f"https://www.sogou.com/web?query={quote(query)}&num={min(limit, 50)}"
    
    try:
        headers = get_random_headers()
        
        response = requests.get(url, headers=headers, timeout=15, proxies=PROXIES)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for div in soup.select('div.vrwrap'):
            title_elem = div.select_one('h3 a') or div.select_one('a')
            snippet_elem = div.select_one('p.str-text-info') or div.select_one('p')
            
            if title_elem:
                href = title_elem.get('href', '')
                
                if href.startswith('/link?'):
                    actual_url = unquote(href.split('url=')[-1].split('&')[0]) if 'url=' in href else href
                else:
                    actual_url = href
                
                domain = urlparse(actual_url).netloc.replace('www.', '')
                
                if is_valid_domain(domain):
                    results.append({
                        'name': clean_company_name(title_elem.text),
                        'domain': domain,
                        'url': actual_url,
                        'description': snippet_elem.text if snippet_elem else '',
                        'source': 'sogou'
                    })
                
                if len(results) >= limit:
                    break
                    
    except Exception as e:
        print(f"Sogou search error: {e}", file=sys.stderr)
    
    return results


def so_search(query, limit=50):
    """360搜索"""
    results = []
    url = f"https://www.so.com/s?q={quote(query)}&pn=1"
    
    try:
        headers = get_random_headers()
        
        response = requests.get(url, headers=headers, timeout=15, proxies=PROXIES)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for li in soup.select('li.res-list'):
            title_elem = li.select_one('h3 a')
            snippet_elem = li.select_one('p.res-desc') or li.select_one('p')
            
            if title_elem:
                href = title_elem.get('href', '')
                domain = urlparse(href).netloc.replace('www.', '')
                
                if is_valid_domain(domain):
                    results.append({
                        'name': clean_company_name(title_elem.text),
                        'domain': domain,
                        'url': href,
                        'description': snippet_elem.text if snippet_elem else '',
                        'source': 'so'
                    })
                
                if len(results) >= limit:
                    break
                    
    except Exception as e:
        print(f"360 search error: {e}", file=sys.stderr)
    
    return results


def searx_search(query, limit=50):
    """Searx搜索 - 开源元搜索引擎"""
    results = []
    searx_instances = [
        'https://searx.be',
        'https://search.sapti.me',
        'https://search.bus-hit.me',
        'https://search.rowie.at',
        'https://searx.fmac.xyz',
    ]
    
    for instance in searx_instances:
        try:
            url = f"{instance}/search?q={quote(query)}&format=json"
            headers = get_random_headers()
            
            response = requests.get(url, headers=headers, timeout=15, proxies=PROXIES)
            data = response.json()
            
            for result in data.get('results', []):
                result_url = result.get('url', '')
                domain = urlparse(result_url).netloc.replace('www.', '')
                
                if is_valid_domain(domain):
                    results.append({
                        'name': clean_company_name(result.get('title', '')),
                        'domain': domain,
                        'url': result_url,
                        'description': result.get('content', ''),
                        'source': 'searx'
                    })
                
                if len(results) >= limit:
                    break
            
            if results:
                break
                    
        except Exception as e:
            print(f"Searx ({instance}) search error: {e}", file=sys.stderr)
            continue
    
    return results


def search_companies(keyword, region=None, limit=50, engines=None):
    init_proxies()
    detect_available_engines()
    
    query = keyword
    if region:
        query = f"{region} {keyword}"
    
    all_results = []
    seen_domains = set()
    engine_stats = {}
    
    print(f"\n搜索关键词: {query}", file=sys.stderr)
    print(f"目标数量: {limit}", file=sys.stderr)
    
    if engines is None:
        engines = get_sorted_engines()
    else:
        engines = [e for e in engines if e in SEARCH_ENGINES]
    
    search_functions = {
        'google': google_search,
        'duckduckgo': duckduckgo_search,
        'bing': bing_search,
        'baidu': baidu_search,
        'sogou': sogou_search,
        'so': so_search,
        'searx': searx_search,
    }
    
    print(f"\n开始搜索...", file=sys.stderr)
    
    for engine in engines:
        if len(all_results) >= limit:
            break
        
        if engine not in search_functions:
            continue
        
        if not AVAILABLE_ENGINES.get(engine, {}).get('available', False):
            print(f"  {SEARCH_ENGINES[engine]['name']}: 跳过（不可用）", file=sys.stderr)
            continue
        
        search_func = search_functions[engine]
        engine_info = SEARCH_ENGINES.get(engine, {})
        
        try:
            results = search_func(query, limit)
            new_results = 0
            
            for r in results:
                domain = r['domain']
                if domain not in seen_domains:
                    seen_domains.add(domain)
                    all_results.append(r)
                    new_results += 1
            
            engine_stats[engine] = {
                'total': len(results),
                'new': new_results
            }
            
            print(f"  {engine_info.get('name', engine)}: 找到 {len(results)} 条，新增 {new_results} 条", file=sys.stderr)
            
            if len(all_results) >= limit:
                break
                
        except Exception as e:
            print(f"  {engine_info.get('name', engine)}: 搜索失败 - {e}", file=sys.stderr)
            engine_stats[engine] = {'total': 0, 'new': 0, 'error': str(e)}
            continue
    
    print(f"\n汇总结果: {len(all_results)} 家公司", file=sys.stderr)
    
    return {
        'results': all_results[:limit],
        'engine_stats': engine_stats,
        'available_engines': [SEARCH_ENGINES[e]['name'] for e in get_sorted_engines()]
    }


def list_engines():
    """列出所有支持的搜索引擎"""
    init_proxies()
    detect_available_engines()
    
    print("\n支持的搜索引擎：")
    print("=" * 70)
    for key, info in SEARCH_ENGINES.items():
        status = "✓ 可用" if info.get('available', False) else "✗ 不可用"
        print(f"\n{info['name']} ({key}):")
        print(f"  状态: {status}")
        print(f"  优先级: {info['priority']}")
        print(f"  说明: {info['description']}")
    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(description='Search for potential customer companies')
    parser.add_argument('keyword', nargs='?', help='Search keyword')
    parser.add_argument('--region', '-r', help='Region filter (e.g., 上海, 北京)')
    parser.add_argument('--limit', '-l', type=int, default=50, help='Maximum number of results')
    parser.add_argument('--output', '-o', help='Output file path (JSON)')
    parser.add_argument('--proxy', '-p', help='Proxy URL (e.g., http://127.0.0.1:7890)')
    parser.add_argument('--engines', '-e', help='Comma-separated list of search engines (e.g., google,duckduckgo,baidu)')
    parser.add_argument('--list-engines', action='store_true', help='List all supported search engines')
    
    args = parser.parse_args()
    
    if args.list_engines:
        list_engines()
        return
    
    if not args.keyword:
        parser.print_help()
        return
    
    if args.proxy:
        os.environ['HTTPS_PROXY'] = args.proxy
        os.environ['HTTP_PROXY'] = args.proxy
    
    engines = args.engines.split(',') if args.engines else None
    
    search_result = search_companies(args.keyword, args.region, args.limit, engines)
    
    output = {
        'query': args.keyword,
        'region': args.region,
        'total': len(search_result['results']),
        'engine_stats': search_result['engine_stats'],
        'available_engines': search_result['available_engines'],
        'results': search_result['results']
    }
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"Results saved to {args.output}", file=sys.stderr)
    else:
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
