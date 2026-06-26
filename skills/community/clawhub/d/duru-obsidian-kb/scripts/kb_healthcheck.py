#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

from kb_env import KB_CONFIG_PATH

SCRIPT_DIR = Path(__file__).resolve().parent
KB_LINT = SCRIPT_DIR / 'kb_lint.py'
DEFAULT_CONFIG = KB_CONFIG_PATH

def run_lint(root: str):
    proc = subprocess.run([
        'python3', str(KB_LINT), '--root', root
    ], capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return {'ok': False, 'root': root, 'error': proc.stderr or proc.stdout}
    try:
        data = json.loads(proc.stdout)
    except Exception:
        data = {'ok': False, 'root': root, 'error': 'invalid_json', 'raw': proc.stdout}
    data['root'] = root
    return data


def main():
    parser = argparse.ArgumentParser(description='Run KB lint checks across configured repos')
    parser.add_argument('--config', default=str(DEFAULT_CONFIG))
    parser.add_argument('--repo', default=None, help='Optional repo name filter')
    args = parser.parse_args()

    cfg_path = Path(args.config).expanduser().resolve()
    if not cfg_path.exists():
        raise SystemExit(f'config not found: {cfg_path}')

    cfg = json.loads(cfg_path.read_text(encoding='utf-8'))
    repos = cfg.get('repos', [])
    if args.repo:
        repos = [r for r in repos if r.get('name') == args.repo]
        if not repos:
            raise SystemExit(f'repo not found in config: {args.repo}')

    results = []
    for repo in repos:
        root = repo.get('root')
        if not root:
            results.append({'ok': False, 'repo': repo.get('name'), 'error': 'missing_root'})
            continue
        lint = run_lint(root)
        lint['repo'] = repo.get('name')
        results.append(lint)

    overall_ok = all(r.get('ok') for r in results)
    print(json.dumps({
        'ok': overall_ok,
        'checked': len(results),
        'results': results,
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
