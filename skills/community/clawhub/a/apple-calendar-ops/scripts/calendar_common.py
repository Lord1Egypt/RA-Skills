#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import re
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, time, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4
from zoneinfo import ZoneInfo

from icalendar import Calendar, Event

WORKSPACE = Path('/home/agent/.openclaw/workspace')
SECRETS_PATH = WORKSPACE / 'secrets.json'
DAV_NS = 'DAV:'
CALDAV_NS = 'urn:ietf:params:xml:ns:caldav'
NS = {'d': DAV_NS, 'c': CALDAV_NS}


class CalendarError(RuntimeError):
    pass


def get_nested(obj: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    cur: Any = obj
    for key in keys:
        if not isinstance(cur, dict) or key not in cur:
            return default
        cur = cur[key]
    return cur


def load_all_secrets() -> Dict[str, Any]:
    if not SECRETS_PATH.exists():
        raise CalendarError(f'Missing secrets file: {SECRETS_PATH}')
    return json.loads(SECRETS_PATH.read_text(encoding='utf-8'))


def load_apple_config() -> Dict[str, Any]:
    data = load_all_secrets()
    apple = data.get('appleCalendar') or {}
    if not apple.get('appleId') or not apple.get('appSpecificPassword'):
        raise CalendarError('Missing appleCalendar.appleId or appleCalendar.appSpecificPassword in secrets.json')
    return {
        'appleId': apple['appleId'],
        'appSpecificPassword': apple['appSpecificPassword'],
        'baseUrl': apple.get('baseUrl') or 'https://caldav.icloud.com',
        'calendarUrls': apple.get('calendarUrls') or [],
        'timezone': apple.get('timezone') or 'Asia/Shanghai',
    }


def load_secrets() -> Dict[str, Any]:
    return load_apple_config()


def print_json(data: Any) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def not_implemented(operation: str) -> None:
    raise CalendarError(f'{operation} is not implemented yet in apple-calendar-ops v1')


def authenticated_request(
    url: str,
    username: str,
    password: str,
    method: str = 'GET',
    headers: Optional[Dict[str, str]] = None,
    data: Optional[bytes] = None,
) -> Tuple[bytes, Dict[str, str]]:
    token = base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('ascii')
    req = urllib.request.Request(url=url, method=method, data=data)
    req.add_header('Authorization', f'Basic {token}')
    for key, value in (headers or {}).items():
        req.add_header(key, value)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read(), dict(resp.headers.items())
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode('utf-8', errors='replace')
        raise CalendarError(f'{method} {url} failed with HTTP {exc.code}: {body_text[:400]}') from exc
    except urllib.error.URLError as exc:
        raise CalendarError(f'{method} {url} network error: {exc}') from exc


def caldav_request(url: str, username: str, password: str, method: str, body: str, depth: str = '0') -> bytes:
    content, _ = authenticated_request(
        url=url,
        username=username,
        password=password,
        method=method,
        headers={
            'Depth': depth,
            'Content-Type': 'application/xml; charset=utf-8',
        },
        data=body.encode('utf-8'),
    )
    return content


def parse_xml(content: bytes) -> ET.Element:
    try:
        return ET.fromstring(content)
    except ET.ParseError as exc:
        raise CalendarError(f'Failed to parse XML: {exc}') from exc


def first_href(root: ET.Element, xpath: str) -> Optional[str]:
    el = root.find(xpath, NS)
    if el is None or el.text is None:
        return None
    return el.text.strip()


def absolutize(base_url: str, href: str) -> str:
    return urllib.parse.urljoin(base_url, href)


def discover_calendars(base_url: str, username: str, password: str) -> List[Dict[str, str]]:
    principal_body = """<?xml version='1.0' encoding='utf-8'?>
<d:propfind xmlns:d='DAV:'>
  <d:prop>
    <d:current-user-principal />
  </d:prop>
</d:propfind>
"""
    principal_root = parse_xml(caldav_request(base_url, username, password, 'PROPFIND', principal_body, depth='0'))
    principal_href = first_href(principal_root, './/d:current-user-principal/d:href')
    if not principal_href:
        raise CalendarError('Could not discover current-user-principal from CalDAV server')
    principal_url = absolutize(base_url, principal_href)

    home_body = """<?xml version='1.0' encoding='utf-8'?>
<d:propfind xmlns:d='DAV:' xmlns:c='urn:ietf:params:xml:ns:caldav'>
  <d:prop>
    <c:calendar-home-set />
  </d:prop>
</d:propfind>
"""
    home_root = parse_xml(caldav_request(principal_url, username, password, 'PROPFIND', home_body, depth='0'))
    home_href = first_href(home_root, './/c:calendar-home-set/d:href')
    if not home_href:
        raise CalendarError('Could not discover calendar-home-set from CalDAV server')
    home_url = absolutize(principal_url, home_href)

    list_body = """<?xml version='1.0' encoding='utf-8'?>
<d:propfind xmlns:d='DAV:'>
  <d:prop>
    <d:resourcetype />
    <d:displayname />
  </d:prop>
</d:propfind>
"""
    list_root = parse_xml(caldav_request(home_url, username, password, 'PROPFIND', list_body, depth='1'))
    calendars: List[Dict[str, str]] = []
    for response in list_root.findall('.//d:response', NS):
        href = response.find('d:href', NS)
        if href is None or not href.text:
            continue
        is_calendar = response.find('.//d:resourcetype/c:calendar', NS) is not None
        if not is_calendar:
            continue
        url = absolutize(home_url, href.text.strip())
        name = (response.findtext('.//d:displayname', default='', namespaces=NS) or '').strip()
        if not name:
            name = url.rstrip('/').split('/')[-1]
        calendars.append({'id': url, 'name': name, 'url': url})
    if not calendars:
        raise CalendarError('No calendars discovered from CalDAV home set')
    return calendars


def maybe_filter_calendars(calendars: List[Dict[str, str]], allowed_urls: List[str]) -> List[Dict[str, str]]:
    if not allowed_urls:
        return calendars
    allowed = set(allowed_urls)
    filtered = [item for item in calendars if item['url'] in allowed]
    if not filtered:
        raise CalendarError('Configured calendarUrls filtered out all discovered calendars')
    return filtered


def resolve_calendar(calendars: List[Dict[str, str]], calendar_name: Optional[str] = None, calendar_id: Optional[str] = None) -> Dict[str, str]:
    if calendar_id:
        for item in calendars:
            if item['id'] == calendar_id or item['url'] == calendar_id:
                return item
        raise CalendarError(f'Calendar id not found: {calendar_id}')
    if calendar_name:
        matched = [item for item in calendars if item['name'].strip().lower() == calendar_name.strip().lower()]
        if not matched:
            raise CalendarError(f'Calendar name not found: {calendar_name}')
        if len(matched) > 1:
            raise CalendarError(f'Calendar name ambiguous: {calendar_name}')
        return matched[0]
    raise CalendarError('Need calendar name or calendar id')


def infer_calendar_for_event(event_id: str, calendars: List[Dict[str, str]]) -> Optional[Dict[str, str]]:
    for calendar in calendars:
        if event_id.startswith(calendar['url']):
            return calendar
    return None


def parse_cli_datetime(raw: str, tz_name: str, end_of_day: bool = False) -> datetime:
    tz = ZoneInfo(tz_name)
    text = raw.strip()
    if re.fullmatch(r'\d{4}-\d{2}-\d{2}', text):
        day = datetime.fromisoformat(text)
        base = datetime.combine(day.date(), time.max if end_of_day else time.min)
        return base.replace(tzinfo=tz)
    dt = datetime.fromisoformat(text)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz)
    return dt


def unfold_ics_lines(text: str) -> List[str]:
    raw_lines = text.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    lines: List[str] = []
    for line in raw_lines:
        if not line:
            continue
        if line.startswith((' ', '\t')) and lines:
            lines[-1] += line[1:]
        else:
            lines.append(line)
    return lines


def parse_ical_value(line: str) -> Tuple[str, Dict[str, str], str]:
    key_part, value = line.split(':', 1)
    parts = key_part.split(';')
    name = parts[0].upper()
    params: Dict[str, str] = {}
    for part in parts[1:]:
        if '=' in part:
            k, v = part.split('=', 1)
            params[k.upper()] = v
    return name, params, value


def unescape_ical_text(value: str) -> str:
    return value.replace('\\n', '\n').replace('\\,', ',').replace('\\;', ';').replace('\\\\', '\\').strip()


def parse_ics_datetime(value: str, params: Dict[str, str], default_tz: ZoneInfo) -> Tuple[datetime, bool]:
    if params.get('VALUE') == 'DATE' or re.fullmatch(r'\d{8}', value):
        dt = datetime.strptime(value[:8], '%Y%m%d').replace(tzinfo=default_tz)
        return dt, True
    if value.endswith('Z'):
        dt = datetime.strptime(value, '%Y%m%dT%H%M%SZ').replace(tzinfo=timezone.utc).astimezone(default_tz)
        return dt, False
    dt = datetime.strptime(value, '%Y%m%dT%H%M%S')
    return dt.replace(tzinfo=default_tz), False


def normalize_event(event_id: str, calendar: Dict[str, str], title: str, start: datetime, end: datetime, all_day: bool, location: str, notes: str, raw: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'id': event_id,
        'calendar': {'id': calendar['id'], 'name': calendar['name']},
        'title': title,
        'start': start.isoformat(),
        'end': end.isoformat(),
        'allDay': all_day,
        'location': location,
        'notes': notes,
        'raw': raw,
    }


def parse_ics_events(ics_text: str, range_start: datetime, range_end: datetime, calendar: Dict[str, str], resource_url: str, etag: Optional[str]) -> List[Dict[str, Any]]:
    lines = unfold_ics_lines(ics_text)
    events: List[Dict[str, Any]] = []
    in_event = False
    props: List[Tuple[str, Dict[str, str], str]] = []
    for line in lines:
        if line == 'BEGIN:VEVENT':
            in_event = True
            props = []
            continue
        if line == 'END:VEVENT':
            in_event = False
            item = {name: (params, value) for name, params, value in props}
            try:
                dtstart_raw = item.get('DTSTART')
                if not dtstart_raw:
                    continue
                start, all_day = parse_ics_datetime(dtstart_raw[1], dtstart_raw[0], range_start.tzinfo)  # type: ignore[arg-type]
                if 'DTEND' in item:
                    end, _ = parse_ics_datetime(item['DTEND'][1], item['DTEND'][0], range_start.tzinfo)  # type: ignore[arg-type]
                else:
                    end = start + (timedelta(days=1) if all_day else timedelta(hours=1))
                if end <= range_start or start >= range_end:
                    continue
                uid = item.get('UID', ({}, ''))[1] or resource_url
                event = normalize_event(
                    event_id=resource_url,
                    calendar=calendar,
                    title=unescape_ical_text(item.get('SUMMARY', ({}, 'Untitled event'))[1]),
                    start=start,
                    end=end,
                    all_day=all_day,
                    location=unescape_ical_text(item.get('LOCATION', ({}, ''))[1]),
                    notes=unescape_ical_text(item.get('DESCRIPTION', ({}, ''))[1]),
                    raw={'uid': uid, 'etag': etag, 'resourceUrl': resource_url},
                )
                events.append(event)
            except Exception:
                pass
            continue
        if in_event and ':' in line:
            props.append(parse_ical_value(line))
    events.sort(key=lambda e: (e['start'], e['end'], e['title'].lower()))
    return events


def query_events(calendars: List[Dict[str, str]], username: str, password: str, start: datetime, end: datetime) -> List[Dict[str, Any]]:
    start_utc = start.astimezone(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    end_utc = end.astimezone(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    query_body = f"""<?xml version='1.0' encoding='utf-8'?>
<c:calendar-query xmlns:d='DAV:' xmlns:c='urn:ietf:params:xml:ns:caldav'>
  <d:prop>
    <d:getetag />
    <c:calendar-data>
      <c:expand start='{start_utc}' end='{end_utc}' />
    </c:calendar-data>
  </d:prop>
  <c:filter>
    <c:comp-filter name='VCALENDAR'>
      <c:comp-filter name='VEVENT'>
        <c:time-range start='{start_utc}' end='{end_utc}' />
      </c:comp-filter>
    </c:comp-filter>
  </c:filter>
</c:calendar-query>
"""
    events: List[Dict[str, Any]] = []
    for calendar in calendars:
        root = parse_xml(caldav_request(calendar['url'], username, password, 'REPORT', query_body, depth='1'))
        for response in root.findall('.//d:response', NS):
            href = response.find('d:href', NS)
            if href is None or not href.text:
                continue
            resource_url = absolutize(calendar['url'], href.text.strip())
            etag = response.findtext('.//d:getetag', default='', namespaces=NS) or None
            for data_el in response.findall('.//c:calendar-data', NS):
                if data_el.text:
                    events.extend(parse_ics_events(data_el.text, start, end, calendar, resource_url, etag))
    events.sort(key=lambda e: (e['start'], e['end'], e['title'].lower()))
    return events


def coerce_component_datetime(value: Any, tz_name: str) -> Tuple[datetime, bool]:
    tz = ZoneInfo(tz_name)
    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=tz)
        return value, False
    if isinstance(value, date):
        return datetime.combine(value, time.min, tz), True
    raise CalendarError(f'Unsupported calendar datetime value: {value!r}')


def parse_existing_event(content: bytes, event_id: str, calendars: List[Dict[str, str]], tz_name: str, etag: Optional[str] = None) -> Dict[str, Any]:
    cal = Calendar.from_ical(content)
    component = next((item for item in cal.walk() if item.name == 'VEVENT'), None)
    if component is None:
        raise CalendarError(f'No VEVENT found in resource: {event_id}')
    calendar = infer_calendar_for_event(event_id, calendars) or {'id': '', 'name': '', 'url': ''}
    start, all_day = coerce_component_datetime(component.decoded('dtstart'), tz_name)
    if component.get('dtend'):
        end, _ = coerce_component_datetime(component.decoded('dtend'), tz_name)
    else:
        end = start + (timedelta(days=1) if all_day else timedelta(hours=1))
    uid = str(component.get('uid', event_id))
    title = str(component.get('summary', 'Untitled event'))
    location = str(component.get('location', '')) if component.get('location') is not None else ''
    notes = str(component.get('description', '')) if component.get('description') is not None else ''
    return normalize_event(
        event_id=event_id,
        calendar=calendar,
        title=title,
        start=start,
        end=end,
        all_day=all_day,
        location=location,
        notes=notes,
        raw={'uid': uid, 'etag': etag, 'resourceUrl': event_id},
    )


def fetch_event_resource(event_id: str, username: str, password: str, calendars: List[Dict[str, str]], tz_name: str) -> Tuple[bytes, Optional[str], Dict[str, Any]]:
    content, headers = authenticated_request(event_id, username, password, method='GET')
    etag = headers.get('ETag') or headers.get('Etag')
    event = parse_existing_event(content, event_id, calendars, tz_name, etag=etag)
    return content, etag, event


def build_event_ics(title: str, start: datetime, end: datetime, all_day: bool, location: Optional[str], notes: Optional[str], uid: Optional[str] = None) -> bytes:
    cal = Calendar()
    cal.add('prodid', '-//Jarvis//apple-calendar-ops//EN')
    cal.add('version', '2.0')

    event = Event()
    event.add('uid', uid or str(uuid4()).upper())
    event.add('summary', title)
    event.add('dtstamp', datetime.now(timezone.utc))

    if all_day:
        start_date = start.date()
        end_date = end.date()
        if end_date <= start_date:
            end_date = start_date + timedelta(days=1)
        event.add('dtstart', start_date)
        event.add('dtend', end_date)
    else:
        if end <= start:
            raise CalendarError('Event end must be later than start')
        event.add('dtstart', start)
        event.add('dtend', end)

    if location:
        event.add('location', location)
    if notes:
        event.add('description', notes)

    cal.add_component(event)
    return cal.to_ical()


def create_event_payload(calendar: Dict[str, str], title: str, start: datetime, end: datetime, all_day: bool, location: Optional[str], notes: Optional[str], uid: Optional[str] = None) -> Tuple[str, bytes, str]:
    event_uid = uid or str(uuid4()).upper()
    event_url = urllib.parse.urljoin(calendar['url'], f'{event_uid}.ics')
    body = build_event_ics(title=title, start=start, end=end, all_day=all_day, location=location, notes=notes, uid=event_uid)
    return event_url, body, event_uid


def put_event(event_url: str, body: bytes, username: str, password: str, etag: Optional[str] = None) -> Optional[str]:
    headers = {'Content-Type': 'text/calendar; charset=utf-8'}
    if etag:
        headers['If-Match'] = etag
    _, resp_headers = authenticated_request(event_url, username, password, method='PUT', headers=headers, data=body)
    return resp_headers.get('ETag') or resp_headers.get('Etag')


def delete_event(event_url: str, username: str, password: str, etag: Optional[str] = None) -> None:
    headers: Dict[str, str] = {}
    if etag:
        headers['If-Match'] = etag
    authenticated_request(event_url, username, password, method='DELETE', headers=headers)
