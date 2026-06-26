#!/usr/bin/env python3
import argparse, json, sys, urllib.request, urllib.parse

FAIL_MARKERS = [
    'Just a moment...',
    'Performing security verification',
    'Enable JavaScript and cookies',
    'captcha',
    'security service to protect against malicious bots',
]

METHODS = [
    ('r.jina.ai', lambda u: f'https://r.jina.ai/http://{u.removeprefix("https://").removeprefix("http://")}'),
    ('markdown.new', lambda u: f'https://markdown.new/{u}'),
    ('defuddle', lambda u: f'https://defuddle.md/{u}'),
]

def fetch(url: str, timeout: int = 30):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode('utf-8', errors='replace')

def classify(text: str):
    low = text.lower()
    for marker in FAIL_MARKERS:
        if marker.lower() in low:
            return 'blocked'
    if len(text.strip()) < 200:
        return 'thin'
    return 'ok'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('url')
    ap.add_argument('--timeout', type=int, default=30)
    args = ap.parse_args()

    attempts = []
    for name, builder in METHODS:
        target = builder(args.url)
        try:
            text = fetch(target, args.timeout)
            status = classify(text)
            attempts.append({'method': name, 'url': target, 'status': status, 'chars': len(text)})
            if status == 'ok':
                print(json.dumps({
                    'ok': True,
                    'method': name,
                    'sourceUrl': args.url,
                    'fetchedUrl': target,
                    'status': status,
                    'attempts': attempts,
                    'content': text,
                }, ensure_ascii=False))
                return
        except Exception as e:
            attempts.append({'method': name, 'url': target, 'status': 'error', 'error': str(e)})

    print(json.dumps({
        'ok': False,
        'sourceUrl': args.url,
        'attempts': attempts,
        'note': 'All direct fetch methods failed or returned challenge/thin content. Fall back to browser or search-based retrieval.'
    }, ensure_ascii=False))
    sys.exit(1)

if __name__ == '__main__':
    main()
