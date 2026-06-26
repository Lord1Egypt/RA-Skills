#!/usr/bin/env python3
import json
import shutil
import subprocess
import sys


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def parse_ss() -> list:
    proc = run(['ss', '-lntpH'])
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or 'ss failed')
    listeners = []
    for line in proc.stdout.splitlines():
        parts = line.split()
        if len(parts) < 4:
            continue
        local = parts[3]
        proc_info = parts[-1] if parts else ''
        ip, port = split_host_port(local)
        listeners.append({
            'proto': 'tcp',
            'ip': ip,
            'port': int(port) if str(port).isdigit() else port,
            'process_name': extract_process_name(proc_info),
            'pid': extract_pid(proc_info),
        })
    return listeners


def parse_lsof() -> list:
    proc = run(['lsof', '-nP', '-iTCP', '-sTCP:LISTEN'])
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or 'lsof failed')
    lines = proc.stdout.splitlines()
    if not lines:
        return []
    listeners = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 9:
            continue
        name = parts[0]
        pid = int(parts[1]) if parts[1].isdigit() else None
        endpoint = parts[-2] if '(LISTEN)' in parts[-1] else parts[-1]
        ip, port = split_lsof_endpoint(endpoint)
        listeners.append({
            'proto': 'tcp',
            'ip': ip,
            'port': int(port) if str(port).isdigit() else port,
            'process_name': name,
            'pid': pid,
        })
    return listeners


def split_host_port(value: str):
    if value.startswith('['):
        host, port = value.rsplit(':', 1)
        return host.strip('[]'), port
    if value.count(':') > 1:
        host, port = value.rsplit(':', 1)
        return host, port
    if ':' in value:
        return value.rsplit(':', 1)
    return value, ''


def split_lsof_endpoint(value: str):
    if '->' in value:
        value = value.split('->', 1)[0]
    if value.startswith('*:'):
        return '0.0.0.0', value.split(':', 1)[1]
    return split_host_port(value)


def extract_process_name(proc_info: str):
    marker = 'users:(("'
    if marker in proc_info:
        rest = proc_info.split(marker, 1)[1]
        return rest.split('"', 1)[0]
    return None


def extract_pid(proc_info: str):
    marker = 'pid='
    if marker in proc_info:
        rest = proc_info.split(marker, 1)[1]
        num = ''
        for ch in rest:
            if ch.isdigit():
                num += ch
            else:
                break
        return int(num) if num else None
    return None


def main() -> None:
    try:
        if shutil.which('ss'):
            listeners = parse_ss()
        elif shutil.which('lsof'):
            listeners = parse_lsof()
        else:
            raise RuntimeError('Neither ss nor lsof is available')
    except Exception as exc:
        print(json.dumps({'status': 'error', 'error': str(exc)}))
        sys.exit(1)

    print(json.dumps({'listeners': listeners}, indent=2))


if __name__ == '__main__':
    main()
