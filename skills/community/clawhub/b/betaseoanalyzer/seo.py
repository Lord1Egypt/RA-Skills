#!/usr/bin/env python3
"""SEO Analyzer"""
import argparse, urllib.request, re

META_KEYS = ['title','description','keywords','author','og:title','og:description']

def analyze(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            html = r.read().decode(errors='ignore')
    except: return {'error': 'Could not fetch URL'}
    
    title = re.search(r'<title>(.*?)</title>', html, re.I)
    desc = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'](.*?)["\']', html, re.I)
    h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.I)
    word_count = len(html.split())
    
    return {
        'url': url,
        'title': title.group(1) if title else 'MISSING',
        'description': desc.group(1)[:100] if desc else 'MISSING',
        'h1_count': len(h1s),
        'word_count': word_count,
        'mobile_friendly': 'viewport' in html
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--url', required=True)
    p.add_argument('--keyword', default='main keyword')
    args = p.parse_args()
    r = analyze(args.url)
    if 'error' in r:
        print(f"❌ {r['error']}")
    else:
        print(f"""
🔍 SEO ANALYSIS: {args.url}
═══════════════════════════════════════
TITLE:       {r['title'][:60]}
DESCRIPTION: {r['description']}
H1 TAGS:     {r['h1_count']} (ideal: 1)
WORD COUNT:  {r['word_count']}
MOBILE:      {'✅' if r['mobile_friendly'] else '❌'}
KEYWORD:     {args.keyword}
""")

if __name__ == '__main__':
    main()
