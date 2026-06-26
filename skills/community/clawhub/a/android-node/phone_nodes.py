#!/usr/bin/env python3
"""
albion_phone_nodes.py — Android phone compute node registry.

Phones run Ollama via Termux. This module discovers, health-checks,
and exposes them to the router as inference endpoints.

Node registry: ~/albion_memory/phone_nodes.json
Format:
  [
    {"name": "pixel6", "url": "http://192.168.1.42:11434", "model": "qwen2.5:0.5b", "enabled": true},
    ...
  ]
"""

import json, time, threading, requests
from pathlib import Path

NODES_FILE     = Path.home() / 'albion_memory' / 'phone_nodes.json'
CHECK_INTERVAL = 60   # seconds between health checks
CALL_TIMEOUT   = 45   # inference timeout per phone

_nodes: list     = []
_healthy: dict   = {}   # url -> bool
_lock            = threading.Lock()


def _load_nodes() -> list:
    try:
        return json.loads(NODES_FILE.read_text())
    except Exception:
        return []


def _check(node: dict) -> bool:
    try:
        r = requests.get(node['url'] + '/api/tags', timeout=5)
        return r.ok
    except Exception:
        return False


def _health_loop():
    while True:
        nodes = _load_nodes()
        with _lock:
            _nodes.clear()
            _nodes.extend(nodes)
        for node in nodes:
            if not node.get('enabled', True):
                continue
            ok = _check(node)
            with _lock:
                _healthy[node['url']] = ok
        time.sleep(CHECK_INTERVAL)


_thread = threading.Thread(target=_health_loop, daemon=True)
_thread.start()


def get_healthy() -> list:
    """Return list of currently healthy, enabled nodes."""
    with _lock:
        return [n for n in _nodes if n.get('enabled', True) and _healthy.get(n['url'], False)]


def call(messages: list, system_override: str = None) -> str:
    """
    Try each healthy phone node in order. Returns first successful response.
    Raises RuntimeError if all fail or none available.
    """
    nodes = get_healthy()
    if not nodes:
        raise RuntimeError('no healthy phone nodes')

    for node in nodes:
        url   = node['url'] + '/api/chat'
        model = node.get('model', 'qwen2.5:0.5b')
        msgs  = list(messages)
        if system_override:
            msgs = [{'role': 'system', 'content': system_override}] + [m for m in msgs if m.get('role') != 'system']
        try:
            r = requests.post(url, json={
                'model': model, 'messages': msgs, 'stream': False,
                'options': {'temperature': 0.7, 'num_predict': 1024},
            }, timeout=CALL_TIMEOUT)
            r.raise_for_status()
            return r.json()['message']['content'].strip()
        except Exception as e:
            with _lock:
                _healthy[node['url']] = False
            continue

    raise RuntimeError('all phone nodes failed')


def register(name: str, ip: str, model: str = 'qwen2.5:0.5b', port: int = 11434):
    """Add or update a phone node in the registry."""
    nodes = _load_nodes()
    url   = f'http://{ip}:{port}'
    existing = next((n for n in nodes if n['url'] == url), None)
    if existing:
        existing.update({'name': name, 'model': model, 'enabled': True})
    else:
        nodes.append({'name': name, 'url': url, 'model': model, 'enabled': True})
    NODES_FILE.write_text(json.dumps(nodes, indent=2))
    print(f'registered {name} at {url}')


def status() -> list:
    """Print current node health."""
    nodes = _load_nodes()
    out   = []
    for n in nodes:
        ok = _healthy.get(n['url'], None)
        state = 'up' if ok else ('down' if ok is False else 'unchecked')
        out.append({'name': n['name'], 'url': n['url'], 'model': n.get('model'), 'state': state})
    return out


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 4 and sys.argv[1] == 'register':
        register(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else 'qwen2.5:0.5b')
    elif len(sys.argv) == 2 and sys.argv[1] == 'status':
        time.sleep(2)
        for n in status():
            print(f"{n['name']:20} {n['url']:30} {n['model']:20} {n['state']}")
    else:
        print('usage:')
        print('  python3 albion_phone_nodes.py register <name> <ip> [model]')
        print('  python3 albion_phone_nodes.py status')
