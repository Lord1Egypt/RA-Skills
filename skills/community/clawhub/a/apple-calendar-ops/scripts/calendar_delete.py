#!/usr/bin/env python3
from __future__ import annotations

import argparse

from calendar_common import CalendarError, delete_event, discover_calendars, fetch_event_resource, load_apple_config, maybe_filter_calendars, print_json


def main() -> int:
    parser = argparse.ArgumentParser(description='Delete an Apple Calendar event')
    parser.add_argument('--event-id', required=True, help='Event resource URL returned by fetch')
    parser.add_argument('--dry-run', action='store_true', help='Show delete target without writing')
    args = parser.parse_args()

    config = load_apple_config()
    calendars = discover_calendars(config['baseUrl'], config['appleId'], config['appSpecificPassword'])
    calendars = maybe_filter_calendars(calendars, config['calendarUrls'])
    _, etag, event = fetch_event_resource(args.event_id, config['appleId'], config['appSpecificPassword'], calendars, config['timezone'])

    if args.dry_run:
        print_json({'ok': True, 'dryRun': True, 'event': event})
        return 0

    delete_event(args.event_id, config['appleId'], config['appSpecificPassword'], etag=etag)
    print_json({'ok': True, 'deleted': True, 'event': event})
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except CalendarError as exc:
        print_json({'ok': False, 'error': str(exc)})
        raise SystemExit(2)
