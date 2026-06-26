#!/usr/bin/env python3
import argparse
import json
import os
import random
import signal
import subprocess
import sys
import time
from pathlib import Path

AUDIO_EXTS = {'.mp3', '.m4a', '.aac', '.wav', '.flac', '.aiff', '.ogg'}
STATE_DIR = Path.home() / '.openclaw' / 'state'
STATE_FILE = STATE_DIR / 'local-audio-jukebox.json'


def scan_audio(root: Path):
    files = []
    for p in root.rglob('*'):
        if p.is_file() and p.suffix.lower() in AUDIO_EXTS:
            files.append(p)
    return sorted(files, key=lambda p: str(p).lower())


def load_state():
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {}


def save_state(state):
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2))


def is_running(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def stop_current():
    state = load_state()
    pid = state.get('pid')
    if not pid:
        print('No active player recorded.')
        return 0
    if not is_running(pid):
        print('Recorded player is not running.')
        return 0
    try:
        os.kill(pid, signal.SIGTERM)
        print(f'Stopped player pid {pid}.')
        return 0
    except Exception as e:
        print(f'error: {e}', file=sys.stderr)
        return 1


def print_status():
    state = load_state()
    if not state:
        print('No player state recorded.')
        return 0
    pid = state.get('pid')
    running = bool(pid and is_running(pid))
    print(json.dumps({
        'running': running,
        'pid': pid,
        'root': state.get('root'),
        'mode': state.get('mode'),
        'query': state.get('query'),
        'tracks': state.get('tracks', []),
        'updatedAt': state.get('updatedAt'),
    }, ensure_ascii=False, indent=2))
    return 0


def play_worker(tracks, player):
    for track in tracks:
        if player == 'afplay':
            cmd = ['afplay', str(track)]
        else:
            cmd = ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'error', str(track)]
        proc = subprocess.Popen(cmd)
        rc = proc.wait()
        if rc != 0:
            print(f'warning: player exited with {rc} for {track}', file=sys.stderr)
            break


def choose_tracks(files, mode, query=None, count=1):
    if mode == 'random':
        if not files:
            return []
        count = max(1, min(count, len(files)))
        return random.sample(files, count)
    if mode == 'match':
        q = (query or '').strip().lower()
        matches = [f for f in files if q in f.name.lower() or q in str(f).lower()]
        return matches
    if mode == 'playlist':
        if not query:
            return files
        terms = [q.strip().lower() for q in query.split(',') if q.strip()]
        selected = []
        for term in terms:
            for f in files:
                hay = (f.name + ' ' + str(f)).lower()
                if term in hay and f not in selected:
                    selected.append(f)
                    break
        return selected
    raise ValueError(f'Unsupported mode: {mode}')


def main():
    parser = argparse.ArgumentParser(description='Scan local audio directories and play matches or random selections.')
    sub = parser.add_subparsers(dest='cmd', required=True)

    scan_p = sub.add_parser('scan')
    scan_p.add_argument('--root', required=True)
    scan_p.add_argument('--limit', type=int, default=100)

    list_p = sub.add_parser('list')
    list_p.add_argument('--root', required=True)
    list_p.add_argument('--query')
    list_p.add_argument('--limit', type=int, default=50)

    play_p = sub.add_parser('play')
    play_p.add_argument('--root', required=True)
    play_p.add_argument('--mode', choices=['random', 'match', 'playlist'], required=True)
    play_p.add_argument('--query')
    play_p.add_argument('--count', type=int, default=1)
    play_p.add_argument('--player', choices=['afplay', 'ffplay'], default='afplay')
    play_p.add_argument('--dry-run', action='store_true')

    sub.add_parser('stop')
    sub.add_parser('status')

    args = parser.parse_args()

    if args.cmd == 'stop':
        return stop_current()
    if args.cmd == 'status':
        return print_status()

    root = Path(os.path.expanduser(args.root)).resolve()
    if not root.exists() or not root.is_dir():
        print(f'error: root directory not found: {root}', file=sys.stderr)
        return 2

    files = scan_audio(root)

    if args.cmd == 'scan':
        print(json.dumps({
            'root': str(root),
            'count': len(files),
            'sample': [str(p) for p in files[:args.limit]],
        }, ensure_ascii=False, indent=2))
        return 0

    if args.cmd == 'list':
        q = (args.query or '').strip().lower()
        if q:
            files = [f for f in files if q in f.name.lower() or q in str(f).lower()]
        print(json.dumps({
            'root': str(root),
            'count': len(files),
            'matches': [str(p) for p in files[:args.limit]],
        }, ensure_ascii=False, indent=2))
        return 0

    tracks = choose_tracks(files, args.mode, args.query, args.count)
    if not tracks:
        print('error: no matching tracks found', file=sys.stderr)
        return 1

    state = {
        'pid': os.getpid(),
        'root': str(root),
        'mode': args.mode,
        'query': args.query,
        'tracks': [str(t) for t in tracks],
        'updatedAt': int(time.time()),
    }
    save_state(state)

    if args.dry_run:
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return 0

    print(json.dumps(state, ensure_ascii=False, indent=2))
    play_worker(tracks, args.player)
    state['updatedAt'] = int(time.time())
    save_state(state)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
