#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path

from kb_env import KB_CONFIG_PATH

SCRIPT_DIR = Path(__file__).resolve().parent
ROUTE = SCRIPT_DIR / 'kb_route.py'
INGEST = SCRIPT_DIR / 'kb_ingest.py'
BUILD = SCRIPT_DIR / 'kb_build.py'
SUMMARIZE = SCRIPT_DIR / 'kb_summarize_concepts.py'
INIT = SCRIPT_DIR / 'kb_init.py'
CONFIG = KB_CONFIG_PATH


def run_json(cmd):
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise SystemExit(proc.stderr or proc.stdout or f'Command failed: {cmd}')
    return json.loads(proc.stdout)


def main():
    parser = argparse.ArgumentParser(description='Unified KB add flow with routing + ingest + optional build')
    parser.add_argument('--source', required=True)
    parser.add_argument('--type', default=None)
    parser.add_argument('--title', default='')
    parser.add_argument('--preview', default='')
    parser.add_argument('--tags', default='')
    parser.add_argument('--notes', default='')
    parser.add_argument('--repo', default=None, help='Explicit repo override')
    parser.add_argument('--config', default=str(CONFIG))
    parser.add_argument('--dry-run-route', action='store_true')
    parser.add_argument('--show-route', action='store_true')
    parser.add_argument('--no-build', action='store_true')
    parser.add_argument('--no-summarize', action='store_true')
    args = parser.parse_args()

    route_cmd = [
        'python3', str(ROUTE),
        '--source', args.source,
        '--config', args.config,
        '--title', args.title,
        '--preview', args.preview,
        '--tags', args.tags,
    ]
    if args.type:
        route_cmd += ['--type', args.type]
    if args.repo:
        route_cmd += ['--repo', args.repo]

    route = run_json(route_cmd)
    if args.dry_run_route:
        print(json.dumps({'ok': True, 'route': route}, ensure_ascii=False, indent=2))
        return

    root_path = Path(route['root']).expanduser().resolve()
    if not (root_path / 'manifest.json').exists():
        run_json(['python3', str(INIT), '--root', str(root_path), '--name', route['repo']])

    ingest_cmd = [
        'python3', str(INGEST),
        '--root', str(root_path),
        '--source', args.source,
        '--tags', args.tags,
        '--notes', args.notes,
    ]
    if args.type:
        ingest_cmd += ['--type', args.type]
    if args.title:
        ingest_cmd += ['--title', args.title]

    ingest = run_json(ingest_cmd)
    build = None
    summarize = None
    if not args.no_build:
        build = run_json(['python3', str(BUILD), '--root', str(root_path)])
    if not args.no_summarize:
        summarize = run_json(['python3', str(SUMMARIZE), '--root', str(root_path)])

    result = {
        'ok': True,
        'route': route,
        'ingest': ingest,
        'build': build,
        'summarize': summarize,
    }
    if args.show_route:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(json.dumps({
            'ok': True,
            'repo': route['repo'],
            'root': route['root'],
            'slug': ingest['entry']['slug'],
            'source_type': ingest['entry']['source_type'],
            'confidence': route['confidence'],
        }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
