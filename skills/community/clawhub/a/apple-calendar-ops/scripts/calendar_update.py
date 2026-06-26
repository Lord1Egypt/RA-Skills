#!/usr/bin/env python3
from __future__ import annotations

import argparse

from calendar_common import CalendarError, build_event_ics, delete_event, discover_calendars, fetch_event_resource, infer_calendar_for_event, load_apple_config, maybe_filter_calendars, parse_cli_datetime, print_json, put_event


def main() -> int:
    parser = argparse.ArgumentParser(description='Update an Apple Calendar event')
    parser.add_argument('--event-id', required=True, help='Event resource URL returned by fetch')
    parser.add_argument('--title', help='New title')
    parser.add_argument('--start', help='New ISO start datetime or YYYY-MM-DD')
    parser.add_argument('--end', help='New ISO end datetime or YYYY-MM-DD')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--all-day', action='store_true', help='Set all-day true')
    mode.add_argument('--timed', action='store_true', help='Set all-day false')
    parser.add_argument('--location', help='New location')
    parser.add_argument('--notes', help='New notes')
    parser.add_argument('--dry-run', action='store_true', help='Show normalized update without writing')
    args = parser.parse_args()

    config = load_apple_config()
    calendars = discover_calendars(config['baseUrl'], config['appleId'], config['appSpecificPassword'])
    calendars = maybe_filter_calendars(calendars, config['calendarUrls'])
    _, etag, current = fetch_event_resource(args.event_id, config['appleId'], config['appSpecificPassword'], calendars, config['timezone'])

    all_day = current['allDay']
    if args.all_day:
        all_day = True
    elif args.timed:
        all_day = False

    start = parse_cli_datetime(args.start, config['timezone']) if args.start else parse_cli_datetime(current['start'], config['timezone'])
    end = parse_cli_datetime(args.end, config['timezone'], end_of_day=all_day) if args.end else parse_cli_datetime(current['end'], config['timezone'], end_of_day=all_day)
    title = args.title if args.title is not None else current['title']
    location = args.location if args.location is not None else current['location']
    notes = args.notes if args.notes is not None else current['notes']
    calendar = infer_calendar_for_event(args.event_id, calendars) or current['calendar']

    event = {
        'id': args.event_id,
        'calendar': {'id': calendar['id'], 'name': calendar['name']},
        'title': title,
        'start': start.isoformat(),
        'end': end.isoformat(),
        'allDay': all_day,
        'location': location or '',
        'notes': notes or '',
        'raw': current['raw'],
    }
    if args.dry_run:
        print_json({'ok': True, 'dryRun': True, 'event': event})
        return 0

    body = build_event_ics(
        title=title,
        start=start,
        end=end,
        all_day=all_day,
        location=location,
        notes=notes,
        uid=current['raw'].get('uid'),
    )
    new_etag = put_event(args.event_id, body, config['appleId'], config['appSpecificPassword'], etag=etag)
    event['raw']['etag'] = new_etag or etag
    print_json({'ok': True, 'updated': True, 'event': event})
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except CalendarError as exc:
        print_json({'ok': False, 'error': str(exc)})
        raise SystemExit(2)
