#!/usr/bin/env python3
import argparse
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path('/root/.openclaw/workspace/skills/api-failover')
SCRIPTS = ROOT / 'scripts'
REFS = ROOT / 'references'


def run_json(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        return {'ok': False, 'cmd': cmd, 'stdout': p.stdout, 'stderr': p.stderr, 'code': p.returncode}
    try:
        data = json.loads(p.stdout.strip() or '{}')
        return {'ok': True, 'data': data, 'stdout': p.stdout, 'stderr': p.stderr}
    except Exception:
        return {'ok': False, 'cmd': cmd, 'stdout': p.stdout, 'stderr': p.stderr, 'code': 0}


def wait_port(host, port, timeout=8):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except Exception:
            time.sleep(0.4)
    return False


def main():
    ap = argparse.ArgumentParser(description='Bootstrap api-failover semi-automatically')
    ap.add_argument('--default-model', default='custom-ai-td-ee/gpt-5.4')
    ap.add_argument('--host', default='127.0.0.1')
    ap.add_argument('--port', type=int, default=4010)
    ap.add_argument('--config-out', default=str(REFS / 'config-production.yaml'))
    ap.add_argument('--state-file', default='/tmp/api-failover-state.json')
    ap.add_argument('--start-proxy', action='store_true')
    args = ap.parse_args()

    report = {'steps': []}
    discovery_tmp = f'/tmp/api-failover-discovery-{os.getpid()}.json'

    discover = run_json([sys.executable, str(SCRIPTS / 'discover_env.py')])
    report['steps'].append({'discover_env': discover})
    if discover.get('ok'):
        Path(discovery_tmp).write_text(
            json.dumps(discover.get('data', {}), ensure_ascii=False, indent=2),
            encoding='utf-8'
        )

    gen = run_json([
        sys.executable, str(SCRIPTS / 'generate_config.py'),
        '--default-model', args.default_model,
        '--output', args.config_out,
        '--discovery-json', discovery_tmp,
    ])
    report['steps'].append({'generate_config': gen})

    proxy_started = False
    proxy_pid = None
    if args.start_proxy:
        log_path = '/tmp/api-failover-http.log'
        with open(log_path, 'a', encoding='utf-8') as logf:
            proc = subprocess.Popen([
                sys.executable, str(SCRIPTS / 'http_proxy.py'),
                '--config', args.config_out,
                '--host', args.host,
                '--port', str(args.port),
                '--state-file', args.state_file,
            ], stdout=logf, stderr=logf)
        proxy_pid = proc.pid
        proxy_started = wait_port(args.host, args.port, timeout=8)
        report['steps'].append({'start_proxy': {'ok': proxy_started, 'pid': proxy_pid, 'log': log_path}})

    if proxy_started:
        selfcheck = run_json([
            sys.executable, str(SCRIPTS / 'selfcheck.py'),
            '--base-url', f'http://{args.host}:{args.port}',
        ])
        report['steps'].append({'selfcheck': selfcheck})
    else:
        report['steps'].append({'selfcheck': {'ok': False, 'reason': 'proxy not started'}})

    report['summary'] = {
        'config_out': args.config_out,
        'proxy_started': proxy_started,
        'proxy_pid': proxy_pid,
        'discovery_file': discovery_tmp if discover.get('ok') else None,
        'next_actions': [
            'Verify generated primary base_url matches the real upstream you want to protect',
            'Set matching credentials for the generated providers in environment variables',
            'If desired, install references/api-failover.service as a user systemd unit',
            'Point OpenAI-compatible clients at the local proxy endpoint',
        ],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
