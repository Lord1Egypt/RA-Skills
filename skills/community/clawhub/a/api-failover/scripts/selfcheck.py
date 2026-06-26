#!/usr/bin/env python3
import argparse
import json
import urllib.request


def get(url):
    with urllib.request.urlopen(url, timeout=3) as resp:
        return json.loads(resp.read().decode('utf-8'))


def post(url, payload):
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'}, method='POST')
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.status, json.loads(resp.read().decode('utf-8'))


def main():
    ap = argparse.ArgumentParser(description='Self-check for api-failover HTTP proxy')
    ap.add_argument('--base-url', default='http://127.0.0.1:4010')
    args = ap.parse_args()

    health = get(args.base_url.rstrip('/') + '/health')
    payload = {
        'messages': [
            {'role': 'user', 'content': 'Reply with exactly: ok'}
        ],
        'max_tokens': 16,
        'temperature': 0,
    }
    try:
        status, body = post(args.base_url.rstrip('/') + '/v1/chat/completions', payload)
        result = {'ok': True, 'health': health, 'chat_status': status, 'chat_body': body}
    except Exception as e:
        result = {'ok': False, 'health': health, 'chat_error': str(e)}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
