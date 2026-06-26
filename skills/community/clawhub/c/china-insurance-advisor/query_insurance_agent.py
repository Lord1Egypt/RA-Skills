#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path
from urllib import request, error

API_URL = 'https://whylingxi.cn/chat'
DEFAULT_SESSION_DIR = Path.home() / '.openclaw' / 'workspace-xiaoma' / '.skill-sessions' / 'china-insurance-advisor'


def load_session_map(path):
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {}


def save_session_map(path, mapping):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(mapping, ensure_ascii=False, indent=2), encoding='utf-8')


def call_agent(message, upstream_session_id=None, timeout=40):
    payload = {'message': message}
    if upstream_session_id:
        payload['session_id'] = upstream_session_id
    data = json.dumps(payload).encode('utf-8')
    req = request.Request(
        API_URL,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode('utf-8')
    parsed = json.loads(body)
    session_id = parsed.get('session_id') or upstream_session_id
    content = parsed.get('reply') or parsed.get('message') or parsed.get('content')
    if not content:
        raise ValueError('Empty reply returned from insurance agent')
    return {
        'session_id': session_id,
        'content': content,
        'raw': parsed,
    }


def main():
    parser = argparse.ArgumentParser(description='Proxy to remote insurance advisor web chat')
    parser.add_argument('--message', required=True, help='User request to send to insurance agent')
    parser.add_argument('--timeout', type=int, default=40, help='HTTP timeout in seconds')
    parser.add_argument('--session-id', help='Local conversation session id for multi-turn continuity')
    parser.add_argument('--reset-session', action='store_true', help='Reset stored upstream session mapping for the given local session id before sending')
    parser.add_argument('--print-history-path', action='store_true', help='Print the local mapping file path to stderr when using session mode')
    args = parser.parse_args()

    try:
        map_dir = Path(os.environ.get('CHINA_INSURANCE_ADVISOR_SESSION_DIR', str(DEFAULT_SESSION_DIR)))
        map_file = map_dir / 'session_map.json'
        session_map = {} if args.reset_session else load_session_map(map_file)
        upstream_session_id = None
        if args.session_id:
            upstream_session_id = session_map.get(args.session_id)
        result = call_agent(args.message, upstream_session_id=upstream_session_id, timeout=args.timeout)
        if args.session_id and result.get('session_id'):
            session_map[args.session_id] = result['session_id']
            save_session_map(map_file, session_map)
            if args.print_history_path:
                print(str(map_file), file=sys.stderr)
        print(result['content'])
    except error.HTTPError as e:
        detail = e.read().decode('utf-8', errors='replace') if hasattr(e, 'read') else str(e)
        print(json.dumps({'error': 'http_error', 'status': e.code, 'detail': detail}, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(json.dumps({'error': 'request_failed', 'detail': str(e)}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
