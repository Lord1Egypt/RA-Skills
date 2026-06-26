#!/usr/bin/env python3
import argparse
import json
import os
from pathlib import Path

try:
    import yaml
except Exception:
    print('PyYAML is required: pip install pyyaml')
    raise

OPENCLAW_CONFIG = Path('/root/.openclaw/openclaw.json')


def detect_local_provider():
    if os.path.exists('/usr/bin/ollama') or os.path.exists('/usr/local/bin/ollama'):
        return ('local', 'http://127.0.0.1:11434/v1', 'qwen2.5:latest')
    return ('local', 'http://127.0.0.1:11434/v1', 'qwen2.5:latest')


def load_json(path):
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding='utf-8'))


def load_discovery(path):
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding='utf-8'))


def choose_primary(discovery, default_model):
    recommended = discovery.get('recommended_primary') or {}
    openclaw_hints = discovery.get('openclaw_hints') or {}
    provider_name = recommended.get('provider_name') or 'primary'
    base_url = recommended.get('base_url') or 'https://your-primary-openai-compatible.example/v1'
    model = recommended.get('default_model') or default_model or openclaw_hints.get('default_model') or 'gpt-5.4'

    return {
        'provider_name': provider_name,
        'base_url': base_url,
        'default_model': model,
        'api_key_env': 'PRIMARY_API_KEY',
        'source': 'discovery' if recommended else 'fallback',
        'inherit_from_openclaw': provider_name if recommended else None,
    }


def build_provider_entry(name, base_url, default_model, cheap_model, api_key_env, inherit_from_openclaw=None):
    entry = {
        'type': 'openai-compatible',
        'base_url': base_url,
        'api_key_env': api_key_env,
        'timeout_ms': 30000,
        'models': {'default': default_model, 'cheap': cheap_model},
    }
    if inherit_from_openclaw:
        entry['inherit_from_openclaw'] = inherit_from_openclaw
    return entry


def build_config(default_model, discovery, include_anthropic=True, include_openrouter=True):
    local_name, local_url, local_model = detect_local_provider()
    primary = choose_primary(discovery, default_model)
    primary_model = primary['default_model'] or 'gpt-5.4'
    cheap_model = 'gpt-4o' if '/' not in primary_model else primary_model

    providers = {
        primary['provider_name']: build_provider_entry(
            primary['provider_name'],
            primary['base_url'],
            primary_model,
            cheap_model,
            primary['api_key_env'],
            inherit_from_openclaw=primary.get('inherit_from_openclaw'),
        ),
        local_name: {
            'type': 'openai-compatible',
            'base_url': local_url,
            'api_key_env': 'OLLAMA_DUMMY_KEY',
            'timeout_ms': 45000,
            'models': {'default': local_model, 'cheap': local_model},
        },
    }

    default_routes = [
        {'provider': primary['provider_name'], 'model': 'default'},
    ]
    cheap_routes = [
        {'provider': primary['provider_name'], 'model': 'cheap'},
    ]
    critical_routes = [
        {'provider': primary['provider_name'], 'model': 'default'},
    ]

    if include_anthropic:
        providers['anthropic'] = {
            'type': 'anthropic',
            'base_url': 'https://api.anthropic.com',
            'api_key_env': 'ANTHROPIC_API_KEY',
            'timeout_ms': 30000,
            'models': {'default': 'claude-opus-4-6', 'cheap': 'claude-sonnet-4-5'},
        }
        default_routes.append({'provider': 'anthropic', 'model': 'default'})
        critical_routes.insert(0, {'provider': 'anthropic', 'model': 'default'})

    if include_openrouter:
        providers['openrouter'] = {
            'type': 'openai-compatible',
            'base_url': 'https://openrouter.ai/api/v1',
            'api_key_env': 'OPENROUTER_API_KEY',
            'timeout_ms': 35000,
            'models': {'default': 'anthropic/claude-sonnet-4', 'cheap': 'openai/gpt-4o-mini'},
        }
        default_routes.append({'provider': 'openrouter', 'model': 'default'})
        cheap_routes.append({'provider': 'openrouter', 'model': 'cheap'})
        critical_routes.append({'provider': 'openrouter', 'model': 'default'})

    default_routes.extend([
        {'provider': primary['provider_name'], 'model': 'cheap'},
        {'provider': local_name, 'model': 'default'},
    ])
    cheap_routes.append({'provider': local_name, 'model': 'default'})
    critical_routes.append({'provider': local_name, 'model': 'default'})

    cfg = {
        'providers': providers,
        'task_profiles': {
            'default': {'routes': default_routes},
            'cheap': {'routes': cheap_routes},
            'critical': {'routes': critical_routes},
        },
        'retry': {
            'max_attempts_per_route': 2,
            'backoff_ms': [500, 1500],
            'retry_on': [
                'RATE_LIMIT', 'TIMEOUT', 'SERVER_ERROR', 'NETWORK_ERROR', 'MODEL_UNAVAILABLE', 'UNKNOWN_TRANSIENT'
            ],
        },
        'circuit_breaker': {
            'open_after_failures': 3,
            'cooldown_seconds': 90,
            'half_open_max_probes': 1,
            'close_after_successes': 1,
        },
        'provider_overrides': {
            local_name: {'open_after_failures': 5, 'cooldown_seconds': 20},
            'openrouter': {'cooldown_seconds': 60},
        },
        'generated_from': {
            'default_model_input': default_model,
            'primary_provider': primary['provider_name'],
            'primary_source': primary['source'],
            'discovery_used': bool(discovery),
            'openclaw_config_present': OPENCLAW_CONFIG.exists(),
        }
    }
    return cfg


def main():
    ap = argparse.ArgumentParser(description='Generate a production-ish api-failover config')
    ap.add_argument('--default-model', default='gpt-5.4')
    ap.add_argument('--output', required=True)
    ap.add_argument('--discovery-json')
    ap.add_argument('--no-anthropic', action='store_true')
    ap.add_argument('--no-openrouter', action='store_true')
    args = ap.parse_args()

    discovery = load_discovery(args.discovery_json)
    cfg = build_config(
        args.default_model,
        discovery,
        include_anthropic=not args.no_anthropic,
        include_openrouter=not args.no_openrouter,
    )
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(cfg, sort_keys=False, allow_unicode=True), encoding='utf-8')
    print(json.dumps({
        'ok': True,
        'output': str(out),
        'default_model': args.default_model,
        'primary_provider': cfg['generated_from']['primary_provider'],
        'primary_source': cfg['generated_from']['primary_source'],
        'discovery_used': cfg['generated_from']['discovery_used'],
    }, ensure_ascii=False))


if __name__ == '__main__':
    main()
