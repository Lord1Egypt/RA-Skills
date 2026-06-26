#!/usr/bin/env python3
import json
import os
import socket
import subprocess
import sys
from pathlib import Path

ROOT = Path('/root/.openclaw/workspace/skills/api-failover')
REFS = ROOT / 'references'
CONFIG = REFS / 'config-forced-failover-drill.yaml'
STATE = Path('/tmp/api-failover-activation-drill-state.json')
ENV_FILE = Path('/root/.config/api-failover.env')


def can_connect(host, port, timeout=0.5):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def run(cmd, check=False):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(f'cmd failed: {cmd}\nstdout={p.stdout}\nstderr={p.stderr}')
    return p


def read_env_file(path):
    result = {}
    if not path.exists():
        return result
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        k, v = line.split('=', 1)
        result[k.strip()] = v.strip()
    return result


def main():
    env_file_vars = read_env_file(ENV_FILE)
    env = {**env_file_vars, **os.environ}
    report = {
        'env_file': str(ENV_FILE),
        'env_file_exists': ENV_FILE.exists(),
        'detected': {
            'ANTHROPIC_API_KEY': bool(env.get('ANTHROPIC_API_KEY')),
            'OPENROUTER_API_KEY': bool(env.get('OPENROUTER_API_KEY')),
            'OLLAMA_11434': can_connect('127.0.0.1', 11434),
        },
        'actions': [],
    }

    if not any(report['detected'].values()):
        report['ok'] = False
        report['message'] = 'No secondary resource detected. Add ANTHROPIC_API_KEY, OPENROUTER_API_KEY, or local Ollama first.'
        print(json.dumps(report, ensure_ascii=False, indent=2))
        sys.exit(2)

    run(['systemctl', '--user', 'daemon-reload'])
    report['actions'].append('daemon-reload')
    run(['systemctl', '--user', 'restart', 'api-failover.service'], check=True)
    report['actions'].append('restart-service')

    if not can_connect('127.0.0.1', 4010, timeout=2):
        report['ok'] = False
        report['message'] = 'api-failover service did not come back on port 4010'
        print(json.dumps(report, ensure_ascii=False, indent=2))
        sys.exit(3)

    payload = Path('/tmp/api-failover-activation-payload.json')
    payload.write_text(json.dumps({
        'messages': [{'role': 'user', 'content': 'Reply with exactly: ok'}],
        'max_tokens': 16,
        'temperature': 0,
    }, ensure_ascii=False), encoding='utf-8')

    proc = run([
        'python3', str(ROOT / 'scripts' / 'failover_proxy.py'),
        '--config', str(CONFIG),
        '--state-file', str(STATE),
        '--payload-file', str(payload),
    ])
    report['drill_returncode'] = proc.returncode
    try:
        report['drill_result'] = json.loads(proc.stdout or '{}')
    except Exception:
        report['drill_result_raw'] = proc.stdout
        report['drill_stderr'] = proc.stderr

    drill = report.get('drill_result', {})
    report['ok'] = bool(drill.get('ok'))
    if report['ok']:
        report['message'] = f"Secondary path activated via {drill.get('provider')}"
    else:
        report['message'] = 'Secondary path still not active or drill failed'

    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(0 if report['ok'] else 4)


if __name__ == '__main__':
    main()
