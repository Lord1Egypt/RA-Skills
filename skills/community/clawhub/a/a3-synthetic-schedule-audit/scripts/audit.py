"""Offline schedule audit; standard library only; no filesystem writes or network."""
import argparse
from datetime import datetime, timedelta
import json
from pathlib import Path


def timestamp(value):
    result = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if result.tzinfo is None or result.utcoffset() is None:
        raise ValueError('Every timestamp must include a UTC offset')
    return result


def audit(data, minutes=30):
    if not 1 <= minutes <= 480:
        raise ValueError('Task duration must be 1 to 480 minutes')
    start, end = timestamp(data['day_start']), timestamp(data['day_end'])
    if end <= start or end-start > timedelta(days=1):
        raise ValueError('Working window must be positive and at most 24 hours')
    if len(data['events']) > 1000:
        raise ValueError('At most 1000 events are supported')
    busy, identifiers = [], set()
    for event in data['events']:
        key = event['id']
        if not isinstance(key, str) or not 1 <= len(key) <= 200 or key in identifiers:
            raise ValueError('Event IDs must be unique strings of 1 to 200 characters')
        identifiers.add(key)
        left, right = timestamp(event['start']), timestamp(event['end'])
        if right <= left:
            raise ValueError('Event end must follow start')
        if event.get('busy', True) and left < end and right > start:
            busy.append((max(left, start), min(right, end), key))
    busy.sort(key=lambda row: row[0])
    conflicts = []
    for index, first in enumerate(busy):
        for second in busy[index+1:]:
            if second[0] >= first[1]:
                break
            conflicts.append([first[2], second[2]])
    duration, cursor, gaps = timedelta(minutes=minutes), start, []
    for left, right, _ in busy + [(end, end, '')]:
        if left-cursor >= duration:
            gaps.append({'start': cursor.astimezone(start.tzinfo).isoformat(),
                         'end': left.astimezone(start.tzinfo).isoformat()})
        cursor = max(cursor, right)
    suggestion = None
    if gaps:
        left = timestamp(gaps[0]['start'])
        suggestion = {'start': left.isoformat(), 'end': (left+duration).isoformat()}
    return {'conflicts': conflicts, 'free_intervals': gaps,
            'task_minutes': minutes, 'suggested_slot': suggestion,
            'scope': 'Supplied working window and busy timed events only'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=Path)
    parser.add_argument('--minutes', type=int, default=30)
    args = parser.parse_args()
    try:
        print(json.dumps(audit(json.loads(args.input.read_text(encoding='utf-8')), args.minutes), indent=2))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        # Event contents and paths are not needed in an error report.
        parser.exit(1, 'Invalid schedule: ' + type(exc).__name__ + '\n')


if __name__ == '__main__':
    main()
