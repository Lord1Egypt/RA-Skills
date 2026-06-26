#!/usr/bin/env python3
import json
import os
import socket
from pathlib import Path
from urllib.parse import urlparse

OPENCLAW_CONFIG = Path('/root/.openclaw/openclaw.json')
COMMON_LOCAL_PORTS = {
    'ollama_11434': ('127.0.0.1', 11434),
    'lmstudio_1234': ('127.0.0.1', 1234),
    'vllm_8000': ('127.0.0.1', 8000),
    'openai_compatible_3000': ('127.0.0.1', 3000),
    'openai_compatible_4000': ('127.0.0.1', 4000),
    'openai_compatible_4010': ('127.0.0.1', 4010),
}


def can_connect(host, port, timeout=0.5):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def env_present(name):
    return bool(os.environ.get(name))


def redact_url(url):
    if not url or not isinstance(url, str):
        return None
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            return url
        return f'{parsed.scheme}://{parsed.netloc}{parsed.path or ""}'
    except Exception:
        return url


def summarize_provider(name, provider):
    if not isinstance(provider, dict):
        return {'name': name, 'type': 'unknown'}

    models = provider.get('models') or []
    model_ids = []
    for item in models[:5]:
        if isinstance(item, dict) and item.get('id'):
            model_ids.append(item['id'])
        elif isinstance(item, str):
            model_ids.append(item)

    return {
        'name': name,
        'api': provider.get('api'),
        'base_url': redact_url(provider.get('baseUrl') or provider.get('base_url')),
        'has_api_key_inline': bool(provider.get('apiKey') or provider.get('api_key')),
        'model_count': len(models) if isinstance(models, list) else 0,
        'sample_models': model_ids,
    }


def main():
    report = {
        'openclaw_config_exists': OPENCLAW_CONFIG.exists(),
        'env': {
            'PRIMARY_API_KEY': env_present('PRIMARY_API_KEY'),
            'OPENAI_API_KEY': env_present('OPENAI_API_KEY'),
            'ANTHROPIC_API_KEY': env_present('ANTHROPIC_API_KEY'),
            'OPENROUTER_API_KEY': env_present('OPENROUTER_API_KEY'),
        },
        'local_candidates': {
            name: can_connect(host, port)
            for name, (host, port) in COMMON_LOCAL_PORTS.items()
        },
        'openclaw_hints': {},
        'recommended_primary': None,
    }

    if OPENCLAW_CONFIG.exists():
        try:
            obj = json.loads(OPENCLAW_CONFIG.read_text(encoding='utf-8'))
            providers = obj.get('models', {}).get('providers', {}) or {}
            provider_summaries = [summarize_provider(name, provider) for name, provider in providers.items()]
            default_model = obj.get('agents', {}).get('defaults', {}).get('model', {}).get('primary')
            matched_provider = None
            matched_model = None
            if isinstance(default_model, str) and '/' in default_model:
                matched_provider, matched_model = default_model.split('/', 1)

            recommended_primary = None
            if matched_provider and matched_provider in providers:
                p = providers[matched_provider]
                recommended_primary = {
                    'provider_name': matched_provider,
                    'type': 'openai-compatible' if (p.get('api') or '').startswith('openai') else p.get('api'),
                    'base_url': redact_url(p.get('baseUrl') or p.get('base_url')),
                    'api_key_source': 'inline-config' if (p.get('apiKey') or p.get('api_key')) else 'env-or-external',
                    'default_model': matched_model,
                }

            report['openclaw_hints'] = {
                'default_model': default_model,
                'default_model_provider': matched_provider,
                'has_gateway': bool(obj.get('gateway')),
                'exec_security': obj.get('tools', {}).get('exec', {}).get('security'),
                'provider_count': len(providers),
                'providers': provider_summaries,
                'gateway_bind': obj.get('gateway', {}).get('bind'),
                'gateway_mode': obj.get('gateway', {}).get('mode'),
            }
            report['recommended_primary'] = recommended_primary
        except Exception as e:
            report['openclaw_hints'] = {'error': str(e)}

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
