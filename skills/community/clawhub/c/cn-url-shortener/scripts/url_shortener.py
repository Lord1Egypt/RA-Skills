#!/usr/bin/env python3
import sys, json, urllib.parse

def shorten(url, custom=None):
    # 简化实现：使用is.gd API
    import requests
    api = "https://is.gd/create.php"
    params = {'format': 'simple', 'url': url}
    if custom:
        params['shorturl'] = custom
    try:
        r = requests.get(api, params=params, timeout=10)
        if r.status_code == 200 and r.text.startswith('http'):
            return {'success': True, 'short_url': r.text.strip()}
        return {'success': False, 'error': r.text[:100]}
    except Exception as e:
        return {'success': False, 'error': str(e)}

if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else ''
    print(json.dumps(shorten(url), ensure_ascii=False))
