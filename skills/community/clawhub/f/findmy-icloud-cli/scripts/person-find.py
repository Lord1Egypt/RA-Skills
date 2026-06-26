#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

STATE_FILE = Path.home() / '.local' / 'state' / 'icloud-findmy-cli' / 'account.env'
ALIASES_FILE = Path.home() / '.local' / 'state' / 'icloud-findmy-cli' / 'people-aliases.json'
PREFERRED_DEVICE_CLASSES = ['iPhone', 'Watch']


def load_username():
    if not STATE_FILE.exists():
        raise SystemExit('No stored Apple ID username. Run ./scripts/findmy.sh set-username <apple-id-email> first.')
    for line in STATE_FILE.read_text().splitlines():
        if line.startswith('ICLOUD_FINDMY_USERNAME='):
            return line.split('=', 1)[1].strip().strip('"')
    raise SystemExit('Stored username missing in state file.')


def normalize(value: str) -> str:
    return value.casefold().replace('’', "'")


def load_aliases():
    if not ALIASES_FILE.exists():
        return {}
    try:
        data = json.loads(ALIASES_FILE.read_text())
    except Exception:
        return {}
    result = {}
    if isinstance(data, dict):
        for key, values in data.items():
            if isinstance(key, str) and isinstance(values, list):
                result[normalize(key)] = [normalize(str(v)) for v in values if str(v).strip()]
    return result


def aliases_for(person: str):
    n = normalize(person)
    aliases = load_aliases()
    return aliases.get(n, [n])


def has_location(device: dict) -> bool:
    return isinstance(device.get('location'), dict) and device.get('location') is not None


def match_score(device: dict, aliases: list[str]) -> tuple[int, int]:
    name = normalize(str(device.get('name', '')))
    device_class = str(device.get('device_class', ''))
    alias_match = any(alias in name for alias in aliases)
    if not alias_match:
        return (-1, -1)
    try:
        class_rank = PREFERRED_DEVICE_CLASSES.index(device_class)
    except ValueError:
        class_rank = len(PREFERRED_DEVICE_CLASSES)
    location_rank = 0 if has_location(device) else 1
    return (location_rank, class_rank)


def main():
    if len(sys.argv) < 2:
        raise SystemExit('Usage: person-find.py <person name>')
    person = ' '.join(sys.argv[1:])
    username = load_username()
    result = subprocess.run(
        ['icloud', 'devices', 'list', '--username', username, '--with-family', '--locate', '--format', 'json'],
        check=True,
        capture_output=True,
        text=True,
    )
    devices = json.loads(result.stdout)
    aliases = aliases_for(person)
    scored = []
    for device in devices:
        score = match_score(device, aliases)
        if score[0] >= 0:
            scored.append((score, device))
    scored.sort(key=lambda item: item[0])
    if not scored:
        print(json.dumps({'query': person, 'match': None, 'reason': 'no matching person/device found'}, ensure_ascii=False))
        return
    chosen = scored[0][1]
    print(json.dumps({'query': person, 'matched_device': chosen}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
