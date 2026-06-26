#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

STATE_FILE = Path.home() / '.local' / 'state' / 'icloud-findmy-cli' / 'account.env'

def load_username():
    if not STATE_FILE.exists():
        raise SystemExit('No stored Apple ID username. Run ./scripts/account-set.sh <apple-id-email> first.')
    for line in STATE_FILE.read_text().splitlines():
        if line.startswith('ICLOUD_FINDMY_USERNAME='):
            return line.split('=', 1)[1].strip().strip('"')
    raise SystemExit('Stored username missing in state file.')

def normalize(value: str) -> str:
    return value.casefold().replace("’", "'")

def main():
    if len(sys.argv) < 2:
        raise SystemExit('Usage: device-find.py <device name substring>')
    needle = normalize(' '.join(sys.argv[1:]))
    username = load_username()
    result = subprocess.run(
        ['icloud', 'devices', 'list', '--username', username, '--with-family', '--locate', '--format', 'json'],
        check=True,
        capture_output=True,
        text=True,
    )
    devices = json.loads(result.stdout)
    matches = []
    for device in devices:
        hay = normalize(str(device.get('name', '')))
        if needle in hay:
            matches.append(device)
    print(json.dumps(matches, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
