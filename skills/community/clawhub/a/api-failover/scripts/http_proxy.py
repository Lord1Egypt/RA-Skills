#!/usr/bin/env python3
import argparse
import json
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from failover_proxy import load_yaml, load_state, save_state, call_with_failover, prune_state_for_config

CODE_HINTS = [
    'python', 'javascript', 'typescript', 'java', 'golang', 'go ', 'rust', 'bash', 'shell',
    'regex', 'sql', 'html', 'css', 'json', 'yaml', 'docker', 'dockerfile', 'kubernetes',
    'debug', 'bug', 'stack trace', 'traceback', 'exception', 'error', 'function', 'class',
    'script', '代码', '报错', '调试', '函数', '脚本', '修复', '编程'
]
CRITICAL_HINTS = [
    'important', 'critical', 'production', 'incident', 'postmortem', 'root cause', 'security',
    'audit', '法律', '合同', '财务', '安全', '上线', '事故', '根因', '正式', '高风险', '严肃'
]
CHEAP_HINTS = [
    'summarize', 'rewrite', 'translate', 'quick', 'simple', 'brief', 'short', 'brainstorm',
    '总结', '翻译', '简短', '简单', '快速', '润色', '改写'
]

TASK_TYPE_TO_PROFILE = {
    'code': 'code',
    'coding': 'code',
    'programming': 'code',
    'chat': 'default',
    'general': 'default',
    'analysis': 'critical',
    'critical': 'critical',
    'security': 'critical',
}
QUALITY_TO_PROFILE = {
    'cheap': 'cheap',
    'fast': 'cheap',
    'balanced': 'default',
    'default': 'default',
    'best': 'critical',
    'high': 'critical',
}


class App:
    def __init__(self, config_path, state_file, default_profile):
        self.config_path = config_path
        self.state_file = state_file
        self.default_profile = default_profile

    def load(self):
        config = load_yaml(self.config_path)
        state = prune_state_for_config(load_state(self.state_file), config)
        return config, state

    def save(self, state):
        save_state(self.state_file, state)


def flatten_messages(payload):
    messages = payload.get('messages') or []
    parts = []
    for msg in messages:
        content = msg.get('content')
        if isinstance(content, str):
            parts.append(content)
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get('type') == 'text' and item.get('text'):
                    parts.append(item['text'])
    return '\n'.join(parts)


def infer_profile(payload, fallback='default'):
    text = flatten_messages(payload).lower().strip()
    if not text:
        return fallback, 'empty-input'

    if '```' in text or re.search(r'\b(def |class |function |import |SELECT |FROM |console\.log|Traceback|Exception)\b', text, re.I):
        return 'code', 'code-block-or-syntax'
    if any(h in text for h in CODE_HINTS):
        return 'code', 'code-keywords'
    if any(h in text for h in CRITICAL_HINTS):
        return 'critical', 'critical-keywords'

    text_len = len(text)
    if text_len < 80 or any(h in text for h in CHEAP_HINTS):
        return 'cheap', 'short-or-cheap-keywords'

    return fallback, 'default-fallback'


def extract_body_hints(payload):
    candidates = [
        payload.get('failover'),
        payload.get('meta'),
        payload.get('metadata'),
    ]
    for candidate in candidates:
        if isinstance(candidate, dict):
            profile = (candidate.get('profile') or '').strip().lower()
            task_type = (candidate.get('task_type') or candidate.get('taskType') or '').strip().lower()
            quality = (candidate.get('quality') or '').strip().lower()
            if profile or task_type or quality:
                return {
                    'profile': profile,
                    'task_type': task_type,
                    'quality': quality,
                }
    return {'profile': '', 'task_type': '', 'quality': ''}


def resolve_hint_to_profile(task_type, quality):
    if task_type and task_type in TASK_TYPE_TO_PROFILE:
        task_profile = TASK_TYPE_TO_PROFILE[task_type]
        if quality and quality in QUALITY_TO_PROFILE:
            quality_profile = QUALITY_TO_PROFILE[quality]
            if task_profile == 'code':
                if quality_profile == 'cheap':
                    return 'cheap', f'task-type={task_type} + quality={quality}'
                return 'code', f'task-type={task_type} + quality={quality}'
            if task_profile == 'critical':
                return 'critical', f'task-type={task_type} + quality={quality}'
            return quality_profile, f'task-type={task_type} + quality={quality}'
        return task_profile, f'task-type={task_type}'

    if quality and quality in QUALITY_TO_PROFILE:
        return QUALITY_TO_PROFILE[quality], f'quality={quality}'

    return None, None


def resolve_profile(headers, payload, fallback='default'):
    explicit_profile = headers.get('X-Failover-Profile')
    if explicit_profile:
        return explicit_profile, 'explicit', 'header-override'

    header_task_type = (headers.get('X-Task-Type') or '').strip().lower()
    header_quality = (headers.get('X-Quality') or '').strip().lower()
    profile, reason = resolve_hint_to_profile(header_task_type, header_quality)
    if profile:
        return profile, 'hint', reason

    body_hints = extract_body_hints(payload)
    if body_hints.get('profile'):
        return body_hints['profile'], 'body-hint', 'body-profile'
    profile, reason = resolve_hint_to_profile(body_hints.get('task_type'), body_hints.get('quality'))
    if profile:
        return profile, 'body-hint', reason

    inferred, reason = infer_profile(payload, fallback=fallback)
    return inferred, 'auto', reason


class Handler(BaseHTTPRequestHandler):
    app = None

    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/health':
            config, state = self.app.load()
            return self._json(200, {
                'ok': True,
                'profiles': list(config.get('task_profiles', {}).keys()),
                'providers': list(config.get('providers', {}).keys()),
                'state_file': self.app.state_file,
                'state': state,
            })
        return self._json(404, {'error': 'NOT_FOUND'})

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path not in ('/v1/chat/completions', '/chat/completions'):
            return self._json(404, {'error': 'NOT_FOUND'})
        length = int(self.headers.get('Content-Length', '0'))
        raw = self.rfile.read(length)
        try:
            payload = json.loads(raw.decode('utf-8')) if raw else {}
        except Exception:
            return self._json(400, {'error': 'INVALID_JSON'})

        profile, profile_source, profile_reason = resolve_profile(self.headers, payload, fallback=self.app.default_profile)

        try:
            config, state = self.app.load()
            result = call_with_failover(config, state, profile, payload)
            self.app.save(state)
        except KeyError as e:
            return self._json(400, {'error': 'UNKNOWN_PROFILE_OR_PROVIDER', 'detail': str(e)})
        except Exception as e:
            return self._json(500, {'error': 'PROXY_ERROR', 'detail': str(e)})

        if result.get('ok'):
            response = result['response']
            if isinstance(response, dict):
                response.setdefault('_failover', {
                    'profile': profile,
                    'profile_source': profile_source,
                    'profile_reason': profile_reason,
                    'provider': result.get('provider'),
                    'requested_model': result.get('requested_model'),
                    'final_model': result.get('final_model') or result.get('model'),
                    'downgraded': result.get('downgraded', False),
                    'downgrade_reason': result.get('downgrade_reason'),
                    'attempts': result.get('attempts', []),
                })
            return self._json(200, response)

        failure_body = {
            'error': result.get('error', 'ALL_ROUTES_FAILED'),
            'user_message': result.get('user_message', '当前模型路由暂时不可用，请稍后重试。'),
            'summary': result.get('summary', {}),
            '_failover': {
                'profile': profile,
                'profile_source': profile_source,
                'profile_reason': profile_reason,
                'requested_model': result.get('requested_model'),
                'attempts': result.get('attempts', []),
            }
        }
        return self._json(503, failure_body)

    def log_message(self, fmt, *args):
        return


def main():
    ap = argparse.ArgumentParser(description='Minimal HTTP wrapper for api-failover MVP')
    ap.add_argument('--config', required=True)
    ap.add_argument('--state-file', default='/tmp/api-failover-state.json')
    ap.add_argument('--profile', default='default')
    ap.add_argument('--host', default='127.0.0.1')
    ap.add_argument('--port', type=int, default=4010)
    args = ap.parse_args()

    app = App(args.config, args.state_file, args.profile)
    Handler.app = app
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(json.dumps({
        'ok': True,
        'listen': f'http://{args.host}:{args.port}',
        'default_profile': args.profile,
        'config': str(Path(args.config)),
        'state_file': args.state_file,
    }, ensure_ascii=False))
    server.serve_forever()


if __name__ == '__main__':
    main()
