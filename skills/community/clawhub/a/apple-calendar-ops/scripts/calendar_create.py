#!/usr/bin/env python3
from __future__ import annotations

import argparse

from calendar_common import CalendarError, create_event_payload, discover_calendars, load_apple_config, maybe_filter_calendars, parse_cli_datetime, print_json, put_event, resolve_calendar


def main() -> int:
    parser = argparse.ArgumentParser(description='Create an Apple Calendar event')
    parser.add_argument('--calendar', help='Calendar name')
    parser.add_argument('--calendar-id', help='Calendar id/url')
    parser.add_argument('--title', required=True, help='Event title')
    parser.add_argument('--start', required=True, help='ISO start datetime or YYYY-MM-DD')
    parser.add_argument('--end', required=True, help='ISO end datetime or YYYY-MM-DD')
    parser.add_argument('--all-day', action='store_true', help='Create as all-day event')
    parser.add_argument('--location', help='Optional location')
    parser.add_argument('--notes', help='Optional notes')
    parser.add_argument('--dry-run', action='store_true', help='Show normalized payload without writing')
    args = parser.parse_args()

    config = load_apple_config()
    calendars = discover_calendars(config['baseUrl'], config['appleId'], config['appSpecificPassword'])
    calendars = maybe_filter_calendars(calendars, config['calendarUrls'])
    calendar = resolve_calendar(calendars, calendar_name=args.calendar, calendar_id=args.calendar_id)

    start = parse_cli_datetime(args.start, config['timezone'])
    end = parse_cli_datetime(args.end, config['timezone'], end_of_day=args.all_day)
    event_url, body, uid = create_event_payload(
        calendar=calendar,
        title=args.title,
        start=start,
        end=end,
        all_day=args.all_day,
        location=args.location,
        notes=args.notes,
    )

    payload = {
        'id': event_url,
        'calendar': {'id': calendar['id'], 'name': calendar['name']},
        'title': args.title,
        'start': start.isoformat(),
        'end': end.isoformat(),
        'allDay': args.all_day,
        'location': args.location or '',
        'notes': args.notes or '',
        'raw': {'uid': uid, 'resourceUrl': event_url},
    }
    if args.dry_run:
        print_json({'ok': True, 'dryRun': True, 'event': payload})
        return 0

    etag = put_event(event_url, body, config['appleId'], config['appSpecificPassword'])
    payload['raw']['etag'] = etag
    print_json({'ok': True, 'created': True, 'event': payload})
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except CalendarError as exc:
        print_json({'ok': False, 'error': str(exc)})
        raise SystemExit(2)
