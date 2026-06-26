#!/usr/bin/env python3
import sys, json, urllib.parse

def parse(url):
    try:
        parsed = urllib.parse.urlparse(url)
        return {
            'scheme': parsed.scheme,
            'netloc': parsed.netloc,
            'path': parsed.path,
            'params': dict(urllib.parse.parse_qsl(parsed.query))
        }
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    print(json.dumps(parse(sys.argv[1] if len(sys.argv)>1 else ''), ensure_ascii=False, indent=2))
