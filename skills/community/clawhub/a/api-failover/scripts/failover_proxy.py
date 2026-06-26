#!/usr/bin/env python3
import argparse
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

try:
    import yaml
except Exception:
    print('PyYAML is required: pip install pyyaml', file=sys.stderr)
    raise

OPENCLAW_CONFIG = Path('/root/.openclaw/openclaw.json')
TRANSIENT = {
    'RATE_LIMIT', 'TIMEOUT', 'SERVER_ERROR', 'NETWORK_ERROR', 'MODEL_UNAVAILABLE', 'UNKNOWN_TRANSIENT'
}
PROVIDER_WIDE_FATAL = {'AUTH_ERROR', 'QUOTA_EXCEEDED'}
CONTROL_FIELDS = {'failover', 'meta', 'metadata'}
_OPENCLAW_CACHE = None


def load_yaml(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_state(path):
    p = Path(path)
    if not p.exists():
        return {'providers': {}}
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception:
        return {'providers': {}}


def prune_state_for_config(state, config):
    valid = set((config.get('providers') or {}).keys())
    current = ((state or {}).get('providers') or {})
    pruned = {name: data for name, data in current.items() if name in valid}
    return {'providers': pruned}


def save_state(path, state):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')


def load_openclaw_config():
    global _OPENCLAW_CACHE
    if _OPENCLAW_CACHE is not None:
        return _OPENCLAW_CACHE
    if not OPENCLAW_CONFIG.exists():
        _OPENCLAW_CACHE = {}
        return _OPENCLAW_CACHE
    try:
        _OPENCLAW_CACHE = json.loads(OPENCLAW_CONFIG.read_text(encoding='utf-8'))
    except Exception:
        _OPENCLAW_CACHE = {}
    return _OPENCLAW_CACHE


def provider_state(state, name):
    return state.setdefault('providers', {}).setdefault(name, {
        'consecutive_failures': 0,
        'cooldown_until': 0,
        'last_error': None,
        'last_success': 0,
    })


def now():
    return int(time.time())


def classify_error(exc=None, status=None, body=''):
    body_l = (body or '').lower()
    if isinstance(exc, urllib.error.HTTPError):
        status = exc.code
    if isinstance(exc, urllib.error.URLError):
        return 'NETWORK_ERROR'
    if isinstance(exc, TimeoutError):
        return 'TIMEOUT'
    if status == 400:
        if 'model' in body_l and any(term in body_l for term in ['not found', 'unavailable', 'overloaded', 'does not exist', 'disabled']):
            return 'MODEL_UNAVAILABLE'
        return 'BAD_REQUEST'
    if status in (401, 403):
        return 'AUTH_ERROR'
    if status == 402:
        return 'QUOTA_EXCEEDED'
    if status == 404 and 'model' in body_l:
        return 'MODEL_UNAVAILABLE'
    if status == 429:
        return 'RATE_LIMIT'
    if status and status >= 500:
        return 'SERVER_ERROR'
    if 'quota' in body_l or 'insufficient_quota' in body_l:
        return 'QUOTA_EXCEEDED'
    if 'model' in body_l and any(term in body_l for term in ['unavailable', 'overloaded', 'not found', 'does not exist', 'disabled']):
        return 'MODEL_UNAVAILABLE'
    return 'UNKNOWN_TRANSIENT'


def choose_routes(config, profile, state):
    routes = config['task_profiles'][profile]['routes']
    selected = []
    ts = now()
    for route in routes:
        ps = provider_state(state, route['provider'])
        if ps.get('cooldown_until', 0) > ts:
            continue
        selected.append(route)
    return selected or routes


def resolve_model(provider_cfg, model_key):
    return provider_cfg.get('models', {}).get(model_key, model_key)


def resolve_provider_cfg(provider_name, provider_cfg):
    resolved = dict(provider_cfg)
    inherit_name = provider_cfg.get('inherit_from_openclaw')
    if not inherit_name:
        return resolved

    openclaw = load_openclaw_config()
    upstream = (((openclaw.get('models') or {}).get('providers') or {}).get(inherit_name) or {})
    if not upstream:
        return resolved

    if upstream.get('baseUrl') and not resolved.get('base_url'):
        resolved['base_url'] = upstream.get('baseUrl')
    else:
        resolved['base_url'] = resolved.get('base_url') or upstream.get('baseUrl')

    if upstream.get('apiKey'):
        resolved['api_key_value'] = upstream.get('apiKey')

    if upstream.get('api') == 'anthropic' and not resolved.get('type'):
        resolved['type'] = 'anthropic'

    return resolved


def sanitize_payload(payload):
    if not isinstance(payload, dict):
        return payload
    return {k: v for k, v in payload.items() if k not in CONTROL_FIELDS}


def build_request(provider_name, provider_cfg, model, payload):
    provider_cfg = resolve_provider_cfg(provider_name, provider_cfg)
    provider_type = provider_cfg.get('type', 'openai-compatible')
    base = provider_cfg['base_url'].rstrip('/')
    api_key = provider_cfg.get('api_key_value') or os.environ.get(provider_cfg.get('api_key_env', ''), '')
    clean_payload = sanitize_payload(payload)

    headers = {'Content-Type': 'application/json'}
    if provider_type == 'anthropic':
        url = f'{base}/v1/messages'
        headers['x-api-key'] = api_key
        headers['anthropic-version'] = '2023-06-01'
        body = {
            'model': model,
            'max_tokens': clean_payload.get('max_tokens', 512),
            'messages': clean_payload['messages'],
        }
    else:
        url = f'{base}/chat/completions'
        headers['Authorization'] = f'Bearer {api_key}'
        body = dict(clean_payload)
        body['model'] = model
    return url, headers, json.dumps(body).encode('utf-8')


def do_call(url, headers, data, timeout_s):
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            text = resp.read().decode('utf-8', 'ignore')
            return resp.status, text
    except urllib.error.HTTPError as e:
        text = e.read().decode('utf-8', 'ignore') if hasattr(e, 'read') else ''
        raise RuntimeError(json.dumps({'http_status': e.code, 'body': text}))
    except Exception as e:
        raise e


def maybe_sleep(backoff_ms, attempt_idx):
    if not backoff_ms:
        return
    idx = min(attempt_idx, len(backoff_ms) - 1)
    base = backoff_ms[idx]
    time.sleep((base + random.randint(0, 250)) / 1000.0)


def mark_failure(config, state, provider_name, err_class):
    ps = provider_state(state, provider_name)
    ps['consecutive_failures'] += 1
    ps['last_error'] = err_class
    cb = config.get('circuit_breaker', {})
    threshold = cb.get('open_after_failures', 3)
    cooldown = cb.get('cooldown_seconds', 90)
    override = config.get('provider_overrides', {}).get(provider_name, {})
    threshold = override.get('open_after_failures', threshold)
    cooldown = override.get('cooldown_seconds', cooldown)
    if err_class == 'QUOTA_EXCEEDED':
        cooldown = max(cooldown, 600)
    if ps['consecutive_failures'] >= threshold:
        ps['cooldown_until'] = now() + cooldown


def mark_success(state, provider_name):
    ps = provider_state(state, provider_name)
    ps['consecutive_failures'] = 0
    ps['cooldown_until'] = 0
    ps['last_error'] = None
    ps['last_success'] = now()


def infer_requested_model(config, profile, payload):
    if payload.get('model'):
        return payload['model']
    routes = (((config.get('task_profiles') or {}).get(profile) or {}).get('routes') or [])
    if not routes:
        return None
    first = routes[0]
    provider_cfg = (config.get('providers') or {}).get(first.get('provider'), {})
    return resolve_model(provider_cfg, first.get('model'))


def summarize_failure(attempts_log):
    providers_tried = []
    error_counts = {}
    last_errors_by_provider = {}
    for item in attempts_log:
        provider = item.get('provider')
        err = item.get('error') or 'UNKNOWN'
        if provider and provider not in providers_tried:
            providers_tried.append(provider)
        error_counts[err] = error_counts.get(err, 0) + 1
        if provider:
            last_errors_by_provider[provider] = err

    unique_errors = list(error_counts.keys())
    if not attempts_log:
        user_message = '当前没有可用的模型路由，请检查配置后重试。'
    elif all(err == 'AUTH_ERROR' for err in unique_errors):
        user_message = '当前已配置的模型凭据不可用，请检查 provider 凭据配置。'
    elif 'NETWORK_ERROR' in unique_errors and len(unique_errors) == 1:
        user_message = '当前模型路由网络不可达，请稍后重试或检查上游连接。'
    elif 'QUOTA_EXCEEDED' in unique_errors:
        user_message = '当前模型额度不足或已耗尽，请切换可用 provider 或稍后重试。'
    else:
        user_message = '当前已配置的模型路由暂时都不可用，请稍后再试或检查 provider 配置。'

    return {
        'providers_tried': providers_tried,
        'error_counts': error_counts,
        'last_errors_by_provider': last_errors_by_provider,
        'user_message': user_message,
    }


def call_with_failover(config, state, profile, payload):
    retry_cfg = config.get('retry', {})
    retry_on = set(retry_cfg.get('retry_on', []))
    max_attempts = int(retry_cfg.get('max_attempts_per_route', 2))
    backoff_ms = retry_cfg.get('backoff_ms', [500, 1500])

    attempts_log = []
    requested_model = infer_requested_model(config, profile, payload)
    routes = choose_routes(config, profile, state)
    blocked_providers = set()

    for route in routes:
        provider_name = route['provider']
        if provider_name in blocked_providers:
            continue
        provider_cfg = config['providers'][provider_name]
        model = resolve_model(provider_cfg, route['model'])
        timeout_s = max(1, int(provider_cfg.get('timeout_ms', 30000) / 1000))
        for attempt in range(max_attempts):
            try:
                url, headers, data = build_request(provider_name, provider_cfg, model, payload)
                status, text = do_call(url, headers, data, timeout_s)
                mark_success(state, provider_name)
                final_model = model
                downgrade = bool(requested_model and final_model and requested_model != final_model)
                downgrade_reason = attempts_log[-1]['error'] if downgrade and attempts_log else None
                return {
                    'ok': True,
                    'provider': provider_name,
                    'model': final_model,
                    'requested_model': requested_model,
                    'final_model': final_model,
                    'downgraded': downgrade,
                    'downgrade_reason': downgrade_reason,
                    'response': json.loads(text),
                    'attempts': attempts_log,
                }
            except Exception as e:
                status = None
                body = ''
                if isinstance(e, RuntimeError):
                    try:
                        parsed = json.loads(str(e))
                        status = parsed.get('http_status')
                        body = parsed.get('body', '')
                    except Exception:
                        body = str(e)
                err_class = classify_error(e, status=status, body=body)
                attempts_log.append({
                    'provider': provider_name,
                    'model': model,
                    'attempt': attempt + 1,
                    'error': err_class,
                    'status': status,
                })
                if err_class in PROVIDER_WIDE_FATAL:
                    blocked_providers.add(provider_name)
                if err_class not in TRANSIENT:
                    mark_failure(config, state, provider_name, err_class)
                    break
                if err_class in retry_on and attempt + 1 < max_attempts:
                    maybe_sleep(backoff_ms, attempt)
                    continue
                mark_failure(config, state, provider_name, err_class)
                break

    summary = summarize_failure(attempts_log)
    return {
        'ok': False,
        'error': 'ALL_ROUTES_FAILED',
        'requested_model': requested_model,
        'user_message': summary['user_message'],
        'summary': {
            'providers_tried': summary['providers_tried'],
            'error_counts': summary['error_counts'],
            'last_errors_by_provider': summary['last_errors_by_provider'],
        },
        'attempts': attempts_log,
    }


def main():
    ap = argparse.ArgumentParser(description='Minimal AI API failover proxy runner')
    ap.add_argument('--config', required=True)
    ap.add_argument('--profile', default='default')
    ap.add_argument('--state-file', default='/tmp/api-failover-state.json')
    ap.add_argument('--payload-file', required=True, help='JSON file containing chat payload/messages')
    ap.add_argument('--prune-state', action='store_true', help='Remove provider state entries not present in config and exit')
    args = ap.parse_args()

    config = load_yaml(args.config)
    state = load_state(args.state_file)
    state = prune_state_for_config(state, config)

    if args.prune_state:
        save_state(args.state_file, state)
        print(json.dumps({'ok': True, 'pruned': True, 'providers': sorted(state.get('providers', {}).keys())}, ensure_ascii=False, indent=2))
        sys.exit(0)

    payload = json.loads(Path(args.payload_file).read_text(encoding='utf-8'))
    result = call_with_failover(config, state, args.profile, payload)
    save_state(args.state_file, state)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result.get('ok') else 2)


if __name__ == '__main__':
    main()
