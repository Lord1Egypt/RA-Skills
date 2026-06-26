# -*- coding: utf-8 -*-
import sys, io, subprocess, re, urllib.parse
from collections import OrderedDict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

def curl_get(url, timeout=12):
    try:
        r = subprocess.run(
            ['curl.exe', '-s', '-L', '--max-time', str(timeout),
             '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
             '-H', 'Accept-Language: zh-CN,zh;q=0.9', url],
            capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout+3
        )
        return r.stdout
    except:
        return ''

def extract_bing(text):
    results = []
    for m in re.finditer(r'<li[^>]*class="b_algo[^"]*"[^>]*>.*?<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>(.*?)</a>.*?<p[^>]*>(.*?)</p>', text, re.DOTALL|re.IGNORECASE):
        url = m.group(1).strip()
        title = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        snippet = re.sub(r'<[^>]+>', '', m.group(3)).strip()
        if url and title:
            results.append({'title': title, 'url': url, 'snippet': snippet[:200], 'source': 'Bing'})
    return results

def extract_360(text):
    results = []
    for m in re.finditer(r'<h3[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', text, re.DOTALL|re.IGNORECASE):
        url = m.group(1).strip()
        title = re.sub(r'<[^>]+>', '', m.group(2)).strip()
        if url and title:
            results.append({'title': title, 'url': url, 'snippet': '', 'source': '360'})
    return results

def extract_zhihu(text):
    results = []
    for m in re.finditer(r'"title":"([^"]+)".*?"link":"([^"]+)".*?"excerpt":"([^"]+)"', text, re.DOTALL|re.IGNORECASE):
        title = m.group(1).strip()
        url = m.group(2).replace('\\/', '/').strip()
        snippet = m.group(3).strip()
        if title and url:
            results.append({'title': title, 'url': url, 'snippet': snippet[:200], 'source': 'Zhihu'})
    return results

def search_bing(query, count=10):
    url = 'https://cn.bing.com/search?q=' + urllib.parse.quote(query) + '&count=' + str(count)
    return extract_bing(curl_get(url))

def search_360(query, count=10):
    url = 'https://www.so.com/s?q=' + urllib.parse.quote(query) + '&pn=1&rn=' + str(count)
    return extract_360(curl_get(url))

def search_zhihu(query, count=10):
    url = 'https://www.zhihu.com/search?type=content&q=' + urllib.parse.quote(query)
    return extract_zhihu(curl_get(url))

def main():
    if len(sys.argv) < 2:
        print('Usage: run.py <keyword> [freshness] [count] [vertical]')
        return

    query = sys.argv[1]
    count = int(sys.argv[3]) if len(sys.argv) > 3 else 10
    vertical = sys.argv[4] if len(sys.argv) > 4 and sys.argv[4] != 'None' else None

    print('')
    print('== [Search] ' + query + ' ==')
    print('')

    if vertical == 'news':
        engines = [('Bing', search_bing), ('360', search_360), ('Zhihu', search_zhihu)]
    elif vertical == 'tech':
        engines = [('Bing', search_bing), ('360', search_360), ('Zhihu', search_zhihu)]
    elif vertical == 'shop':
        engines = [('Bing', search_bing), ('360', search_360)]
    else:
        engines = [('Bing', search_bing), ('360', search_360), ('Zhihu', search_zhihu)]

    all_results = OrderedDict()
    for name, func in engines:
        if len(all_results) >= count:
            break
        try:
            results = func(query, count)
            print('[' + name + '] +' + str(len(results)))
            for r in results:
                url = r.get('url', '')
                if url and url not in all_results:
                    all_results[url] = r
        except:
            print('[' + name + '] 0')
            continue

    results = list(all_results.values())
    if not results:
        print('[Failed] No results.')
        return

    snippets = [r['snippet'] for r in results if r['snippet']]
    if snippets:
        print('')
        print('== [Core Answer] ==')
        seen = []
        for s in snippets:
            core = s[:200].strip().replace('&nbsp;', ' ').replace('&#183;', '·').replace('&ensp;', ' ')
            if core and core not in seen:
                print('  ' + core)
                seen.append(core)
                if len(seen) >= 3:
                    break
        print('')

    print('')
    print('== [Results: ' + str(len(results)) + ' | Bing + 360 + Zhihu] ==')
    for idx, r in enumerate(results, 1):
        print('')
        print(str(idx) + '. [' + r['source'] + '] ' + r['title'])
        if r['snippet']:
            print('   ' + r['snippet'][:150])
        print('   ' + r['url'])

if __name__ == '__main__':
    main()
