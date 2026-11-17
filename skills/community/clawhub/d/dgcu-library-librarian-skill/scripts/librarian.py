#!/usr/bin/env python3
"""Call the public DGCU library assistant; Python standard library only."""
import argparse
import json
import sys
import urllib.error
import urllib.request

ENDPOINT = 'https://lib.dgcu.edu.cn/libai/api/public'


def main():
    parser = argparse.ArgumentParser(description='东莞城市学院图书馆公开 AI 馆员')
    parser.add_argument('query', help='问题或检索词；不要填写敏感个人信息')
    parser.add_argument('--action', choices=['ask', 'catalog', 'ebooks', 'dongguan'], default='ask')
    parser.add_argument('--limit', type=int, choices=range(1, 11), default=5)
    args = parser.parse_args()
    max_length = 1000 if args.action == 'ask' else 100
    if not args.query.strip() or len(args.query) > max_length:
        parser.error(f'query 须为 1—{max_length} 字的文本')
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps({'action': args.action, 'query': args.query.strip(), 'limit': args.limit}).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'User-Agent': 'dgcu-library-librarian-skill/1.0.2'},
        method='POST',
    )
    try:
        with urllib.request.urlopen(request, timeout=115) as response:
            data = json.load(response)
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0
    except urllib.error.HTTPError as exc:
        try:
            message = json.loads(exc.read(8192)).get('error', exc.reason)
        except (ValueError, AttributeError):
            message = exc.reason
        print(f'AI 馆员 HTTP {exc.code}: {message}', file=sys.stderr)
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        print(f'无法获取 AI 馆员结果：{exc}', file=sys.stderr)
    return 1


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    sys.exit(main())
