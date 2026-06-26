#!/usr/bin/env python3
# Copyright (c) 2026 李卓伦 (Zhuolun Li) — MIT License
"""
ClawSwarm Swarm Runner v1.0

Orchestrates multi-agent predictions:
1. Reads a swarm config (YAML/JSON)
2. Spawns N agents with different roles/temperatures
3. Each agent calls an LLM API to produce a prediction
4. Collects results and pipes them to consensus.py

Usage:
  python3 swarm_runner.py --config swarm.yaml
  python3 swarm_runner.py --config swarm.json --dry-run

Config format (YAML):
  target:
    name: "Gold"
    current_price: 5023.1
    unit: "USD/troy oz"
    context: "RSI: 40.8, MA5: 5084, MA10: 5120, recent 5d: -2.1%"

  agents:
    - role: "Macro analyst focusing on geopolitical risk"
      count: 10
      temperature_range: [0.4, 0.7]
    - role: "Technical RSI/MACD momentum trader"
      count: 5
      temperature_range: [0.45, 0.6]

  api:
    provider: groq          # groq | openai | ollama
    model: llama-3.3-70b-versatile
    api_key_env: GROQ_API_KEY   # env var name
    base_url: https://api.groq.com/openai/v1/chat/completions  # optional override
    max_tokens: 150
    delay_ms: 1200          # delay between requests

  consensus:
    max_deviation: 0.15
    bias: 0.0
"""

import json
import os
import sys
import time
import argparse
import subprocess
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


def load_config(path):
    """Load YAML or JSON config."""
    text = Path(path).read_text()
    if path.endswith(('.yaml', '.yml')):
        if not HAS_YAML:
            print("Error: PyYAML required for .yaml configs. Install: pip install pyyaml", file=sys.stderr)
            sys.exit(1)
        return yaml.safe_load(text)
    return json.loads(text)


def build_agents(config):
    """Expand agent groups into individual agent specs."""
    agents = []
    for group in config.get('agents', []):
        count = group.get('count', 1)
        t_range = group.get('temperature_range', [0.5, 0.5])
        t_min, t_max = t_range[0], t_range[-1]
        for i in range(count):
            t = t_min + (t_max - t_min) * (i / max(1, count - 1)) if count > 1 else t_min
            agents.append({
                'role': group['role'],
                'model': group.get('model'),  # per-group override
                'temperature': round(t, 3),
                'index': len(agents)
            })
    return agents


def call_llm(agent, target, api_config):
    """Call LLM API for a single agent prediction."""
    provider = api_config.get('provider', 'groq')
    model = agent.get('model') or api_config.get('model', 'llama-3.3-70b-versatile')
    api_key = os.environ.get(api_config.get('api_key_env', 'GROQ_API_KEY'), api_config.get('api_key', ''))
    max_tokens = api_config.get('max_tokens', 150)

    base_urls = {
        'groq': 'https://api.groq.com/openai/v1/chat/completions',
        'openai': 'https://api.openai.com/v1/chat/completions',
        'ollama': 'http://localhost:11434/v1/chat/completions',
    }
    url = api_config.get('base_url') or base_urls.get(provider, base_urls['groq'])

    system_prompt = f"""{agent['role']}

=== {target['name']} Data ===
Current price: {target['current_price']} {target.get('unit', '')}
{target.get('context', '')}

=== Task ===
Predict next-day close price for {target['name']}.
Return JSON only: {{"price": number, "confidence": 0-100, "reasoning": "brief"}}"""

    user_msg = f"Predict {target['name']} next-day close. Return JSON only."

    headers = {'Content-Type': 'application/json'}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'

    payload = {
        'model': model,
        'messages': [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_msg}
        ],
        'max_tokens': max_tokens,
        'temperature': agent['temperature']
    }

    try:
        if HAS_REQUESTS:
            r = requests.post(url, json=payload, headers=headers, timeout=30)
            r.raise_for_status()
            data = r.json()
        else:
            import urllib.request
            req = urllib.request.Request(
                url, data=json.dumps(payload).encode(),
                headers=headers, method='POST'
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())

        text = data['choices'][0]['message']['content'].strip()

        import re
        m = re.search(r'\{[\s\S]*\}', text)
        if not m:
            return None

        try:
            result = json.loads(m.group())
        except json.JSONDecodeError:
            return None

        if 'price' not in result:
            return None

        price = float(result['price'])
        if price <= 0:
            return None

        return {
            'price': price,
            'confidence': min(100, max(0, int(result.get('confidence', 50)))),
            'reasoning': str(result.get('reasoning', ''))[:120],
            'agent_role': agent['role'][:60],
            'temperature': agent['temperature']
        }

    except Exception as e:
        if '429' in str(e):
            print(f"  Rate limited, waiting 5s...", file=sys.stderr)
            time.sleep(5)
        return None


def run_swarm(config, dry_run=False):
    """Run the full swarm prediction pipeline."""
    target = config['target']
    api_config = config.get('api', {})
    consensus_config = config.get('consensus', {})
    delay_ms = api_config.get('delay_ms', 1200)

    agents = build_agents(config)
    total = len(agents)

    print(f"\n🦞 ClawSwarm | {target['name']} | {total} agents", file=sys.stderr)
    print(f"   Price: {target['current_price']} {target.get('unit', '')}", file=sys.stderr)

    if dry_run:
        print(f"\n[DRY RUN] Would run {total} agents:", file=sys.stderr)
        for a in agents[:5]:
            print(f"  - {a['role'][:50]} (t={a['temperature']})", file=sys.stderr)
        if total > 5:
            print(f"  ... and {total - 5} more", file=sys.stderr)
        return

    predictions = []
    ok, fail = 0, 0

    for i, agent in enumerate(agents):
        result = call_llm(agent, target, api_config)
        if result:
            # Range check
            anchor = target['current_price']
            max_dev = consensus_config.get('max_deviation', 0.15)
            if abs(result['price'] - anchor) / anchor <= max_dev:
                predictions.append(result)
                ok += 1
                if ok <= 5 or ok % 50 == 0:
                    print(f"  🦞 [{ok}] t={result['temperature']}: {result['price']} ({result['confidence']}%)", file=sys.stderr)
            else:
                fail += 1
        else:
            fail += 1

        if i < total - 1:
            time.sleep(delay_ms / 1000.0)

    print(f"\n📈 {ok}✅ / {fail}❌ ({total} total)", file=sys.stderr)

    if not predictions:
        print(json.dumps({'status': 'error', 'message': 'All agents failed'}))
        return

    # Feed to consensus engine
    consensus_input = {
        'predictions': [{'price': p['price'], 'confidence': p['confidence'], 'weight': 1.0} for p in predictions],
        'anchor_price': target['current_price'],
        'max_deviation': consensus_config.get('max_deviation', 0.15),
        'bias': consensus_config.get('bias', 0.0)
    }

    # Try running consensus.py from same directory
    consensus_script = Path(__file__).parent / 'consensus.py'
    if consensus_script.exists():
        try:
            proc = subprocess.run(
                [sys.executable, str(consensus_script)],
                input=json.dumps(consensus_input),
                capture_output=True, text=True, timeout=10
            )
            if proc.returncode == 0:
                result = json.loads(proc.stdout)
                result['predictions'] = predictions
                print(json.dumps(result, indent=2))
                return
        except Exception:
            pass

    # Fallback: output raw predictions
    output = {
        'status': 'success',
        'predictions': predictions,
        'consensus_input': consensus_input,
        'message': 'Consensus engine not available, raw predictions returned'
    }
    print(json.dumps(output, indent=2))


def main():
    parser = argparse.ArgumentParser(description='ClawSwarm Swarm Runner')
    parser.add_argument('--config', '-c', required=True, help='Swarm config file (YAML/JSON)')
    parser.add_argument('--dry-run', action='store_true', help='Show plan without running')
    args = parser.parse_args()

    config = load_config(args.config)
    run_swarm(config, dry_run=args.dry_run)


if __name__ == '__main__':
    main()
