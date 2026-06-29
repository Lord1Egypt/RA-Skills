#!/usr/bin/env python3
"""Auto Backup Manager — restic + Docker volumes backup automation."""
import json, subprocess, sys, os
from pathlib import Path

def init_repo(path):
    """Initialize restic repository"""
    password = subprocess.run(['openssl', 'rand', '-hex', '32'], capture_output=True, text=True).stdout.strip()
    os.makedirs(path, exist_ok=True)
    pass_file = Path(path) / '.restic-key'
    pass_file.write_text(password)
    os.chmod(pass_file, 0o600)
    env = os.environ.copy(); env['RESTIC_PASSWORD'] = password
    r = subprocess.run(['restic', '-r', path, 'init'], capture_output=True, text=True, timeout=30, env=env)
    return {'status': 'ok' if r.returncode == 0 else 'error', 'repo': path, 'key_file': str(pass_file)}

def run_backup(repo, paths, docker_volumes=None):
    """Run incremental backup"""
    env = os.environ.copy()
    pass_file = Path(repo) / '.restic-key'
    if pass_file.exists():
        env['RESTIC_PASSWORD_FILE'] = str(pass_file)
    results = []
    for p in paths:
        r = subprocess.run(['restic', '-r', repo, 'backup', p], capture_output=True, text=True, timeout=120, env=env)
        results.append({'path': p, 'ok': r.returncode == 0})
    if docker_volumes:
        for vol in docker_volumes:
            mount = subprocess.run(['docker', 'volume', 'inspect', vol, '--format', '{{.Mountpoint}}'], capture_output=True, text=True, timeout=10).stdout.strip()
            if mount:
                r = subprocess.run(['restic', '-r', repo, 'backup', mount], capture_output=True, text=True, timeout=120, env=env)
                results.append({'docker_volume': vol, 'ok': r.returncode == 0})
    return {'snapshots': len(results), 'results': results}

if __name__ == '__main__':
    args = sys.argv[1:]
    if '--init' in args:
        idx = args.index('--init') + 1
        result = init_repo(args[idx] if idx < len(args) else '/opt/backup-repo')
    elif '--backup' in args:
        result = run_backup('/opt/backup-repo', ['/opt/king/sae'], ['king-qdrant', 'king-redis'])
    else:
        result = {'status': 'idle', 'message': 'Use --init or --backup'}
    print(json.dumps(result, indent=2, ensure_ascii=False))
