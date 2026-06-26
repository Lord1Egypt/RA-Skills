#!/usr/bin/env python3
"""
Claw Search - 自研全网搜索工具
通过爬取多个免费搜索引擎结果进行聚合
"""

import json
import re
import urllib.parse
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

app = Flask(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def search_bing(query, count=10):
    """搜索 Bing"""
    results = []
    try:
        url = f'https://www.bing.com/search?q={urllib.parse.quote(query)}&count={count}'
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        for item in soup.select('li.b_algo')[:count]:
            try:
                title_elem = item.select_one('h2 a')
                desc_elem = item.select_one('p')
                if title_elem:
                    results.append({
                        'title': title_elem.get_text().strip(),
                        'url': title_elem.get('href', ''),
                        'description': desc_elem.get_text().strip() if desc_elem else '',
                        'source': 'Bing'
                    })
            except:
                continue
    except Exception as e:
        print(f"Bing error: {e}")
    return results

def search_duckduckgo(query, count=10):
    """搜索 DuckDuckGo"""
    results = []
    try:
        url = f'https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}'
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        for item in soup.select('div.result')[:count]:
            try:
                title_elem = item.select_one('a.result__a')
                desc_elem = item.select_one('a.result__snippet')
                if title_elem:
                    results.append({
                        'title': title_elem.get_text().strip(),
                        'url': title_elem.get('href', ''),
                        'description': desc_elem.get_text().strip() if desc_elem else '',
                        'source': 'DuckDuckGo'
                    })
            except:
                continue
    except Exception as e:
        print(f"DuckDuckGo error: {e}")
    return results

def search_yahoo(query, count=10):
    """搜索 Yahoo"""
    results = []
    try:
        url = f'https://search.yahoo.com/search?p={urllib.parse.quote(query)}&n={count}'
        resp = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        for item in soup.select('div.algo')[:count]:
            try:
                title_elem = item.select_one('h3 a')
                desc_elem = item.select_one('div.compText')
                if title_elem:
                    results.append({
                        'title': title_elem.get_text().strip(),
                        'url': title_elem.get('href', ''),
                        'description': desc_elem.get_text().strip() if desc_elem else '',
                        'source': 'Yahoo'
                    })
            except:
                continue
    except Exception as e:
        print(f"Yahoo error: {e}")
    return results

def deduplicate(results):
    """去重"""
    seen = set()
    unique = []
    for r in results:
        url = r.get('url', '')
        if url and url not in seen:
            seen.add(url)
            unique.append(r)
    return unique

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'service': 'Claw Search', 'version': '2.0.0'})

@app.route('/api/search', methods=['POST'])
def search():
    data = request.get_json() or {}
    query = data.get('query', '')
    count = min(int(data.get('count', 10)), 20)
    
    if not query:
        return jsonify({'error': 'query is required'}), 400
    
    # 并行搜索多个引擎
    all_results = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(search_bing, query, count): 'bing',
            executor.submit(search_duckduckgo, query, count): 'ddg',
            executor.submit(search_yahoo, query, count): 'yahoo'
        }
        for future in as_completed(futures, timeout=15):
            try:
                results = future.result()
                all_results.extend(results)
            except:
                pass
    
    # 去重
    unique_results = deduplicate(all_results)
    
    return jsonify({
        'query': query,
        'count': len(unique_results),
        'results': unique_results[:count]
    })

@app.route('/search', methods=['GET'])
def search_get():
    query = request.args.get('q') or request.args.get('query', '')
    count = min(int(request.args.get('count', 10)), 20)
    
    if not query:
        return jsonify({'error': 'query parameter is required'}), 400
    
    data = {'query': query, 'count': count}
    return search()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8093, debug=False)
