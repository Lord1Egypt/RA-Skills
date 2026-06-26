#!/usr/bin/env python3
from __future__ import annotations

import argparse

from calendar_common import CalendarError, discover_calendars, load_apple_config, parse_cli_datetime, print_json, query_events


def main() -> int:
    parser = argparse.ArgumentParser(description='List Apple calendars or fetch events by time range')
    parser.add_argument('--list-calendars', action='store_true', help='List available calendars')
    parser.add_argument('--calendar', action='append', help='Filter by calendar name; may be repeated')
    parser.add_argument('--start', help='ISO start datetime or YYYY-MM-DD')
    parser.add_argument('--end', help='ISO end datetime or YYYY-MM-DD')
    args = parser.parse_args()

    config = load_apple_config()
    calendars = discover_calendars(config['baseUrl'], config['appleId'], config['appSpecificPassword'])
    if config.get('calendarUrls'):
        allowed = {item for item in config['calendarUrls']}
        calendars = [item for item in calendars if item['url'] in allowed]

    if args.list_calendars:
        print_json({'ok': True, 'calendars': calendars})
        return 0

    if not args.start or not args.end:
        raise CalendarError('fetch events requires --start and --end unless --list-calendars is used')

    selected = calendars
    if args.calendar:
        wanted = {item.strip().lower() for item in args.calendar if item.strip()}
        selected = [item for item in calendars if item['name'].strip().lower() in wanted]
        if not selected:
            raise CalendarError('No calendars matched the requested --calendar filter')

    start = parse_cli_datetime(args.start, config['timezone'])
    end = parse_cli_datetime(args.end, config['timezone'], end_of_day=True)
    if end <= start:
        raise CalendarError('--end must be later than --start')

    events = query_events(selected, config['appleId'], config['appSpecificPassword'], start, end)
    print_json({
        'ok': True,
        'range': {'start': start.isoformat(), 'end': end.isoformat()},
        'calendarCount': len(selected),
        'eventCount': len(events),
        'events': events,
    })
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except CalendarError as exc:
        print_json({'ok': False, 'error': str(exc)})
        raise SystemExit(2)
