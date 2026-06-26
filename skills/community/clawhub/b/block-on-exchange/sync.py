"""Core sync logic: ICS calendar source -> Microsoft Exchange (Graph API)."""

import json
import re
from datetime import datetime, timedelta, timezone, date

import recurring_ical_events

import config
import ics_source
import ms_auth

# Pattern for validating Graph API IDs (alphanumeric, hyphens, underscores, equals)
_SAFE_ID_PATTERN = re.compile(r'^[A-Za-z0-9\-_=+/]+$')


def _validate_id(value: str, label: str) -> str:
    """Validate that an ID is safe for use in API paths."""
    if not value or not _SAFE_ID_PATTERN.match(value):
        raise ValueError(f"Invalid {label}: contains unexpected characters")
    return value


def load_event_map() -> dict:
    """Load the source->Exchange event ID mapping."""
    if config.EVENT_MAP_FILE.exists():
        return json.loads(config.EVENT_MAP_FILE.read_text())
    return {}


def save_event_map(mapping: dict):
    """Save the source->Exchange event ID mapping."""
    config.write_restricted(config.EVENT_MAP_FILE, json.dumps(mapping, indent=2))


def fetch_source_events() -> list:
    """Fetch upcoming events from ICS feed, expanding recurring events."""
    cal = ics_source.fetch_ics()

    now = datetime.now(timezone.utc)
    cutoff = now + timedelta(days=config.SYNC_DAYS_AHEAD)

    # Expand all events (including recurring) in the date range
    occurrences = recurring_ical_events.of(cal).between(now, cutoff)

    events = []
    for component in occurrences:
        try:
            uid = str(component.get("UID", ""))
            if not uid:
                continue

            # Check transparency
            transp = str(component.get("TRANSP", "OPAQUE")).upper()
            if transp == "TRANSPARENT":
                continue

            dtstart = component.get("DTSTART").dt
            dtend_prop = component.get("DTEND")
            dtend = dtend_prop.dt if dtend_prop else None

            is_all_day = isinstance(dtstart, date) and not isinstance(dtstart, datetime)

            if is_all_day:
                start_str = dtstart.isoformat()
                end_str = dtend.isoformat() if dtend else (dtstart + timedelta(days=1)).isoformat()
            else:
                if dtstart.tzinfo is None:
                    dtstart = dtstart.replace(tzinfo=timezone.utc)
                if dtend and dtend.tzinfo is None:
                    dtend = dtend.replace(tzinfo=timezone.utc)
                start_str = dtstart.isoformat()
                end_str = dtend.isoformat() if dtend else (dtstart + timedelta(hours=1)).isoformat()

            # Use UID + start time as key so each occurrence is unique
            occurrence_id = f"{uid}_{start_str}"

            events.append({
                "uid": occurrence_id,
                "start": start_str,
                "end": end_str,
                "is_all_day": is_all_day,
            })
        except (ValueError, KeyError, AttributeError) as e:
            print(f"  Warning: skipping event due to parse error: {type(e).__name__}")
            continue

    return events


def source_event_to_exchange(event: dict) -> dict:
    """Convert a parsed ICS event to an Exchange event payload."""
    exchange_event = {
        "subject": config.BLOCKED_EVENT_TITLE,
        "showAs": "busy",
        "isReminderOn": False,
        "body": {"contentType": "text", "content": ""},
    }

    if event["is_all_day"]:
        exchange_event["isAllDay"] = True
        exchange_event["start"] = {
            "dateTime": f"{event['start']}T00:00:00",
            "timeZone": "UTC",
        }
        exchange_event["end"] = {
            "dateTime": f"{event['end']}T00:00:00",
            "timeZone": "UTC",
        }
    else:
        exchange_event["start"] = {
            "dateTime": event["start"],
            "timeZone": "UTC",
        }
        exchange_event["end"] = {
            "dateTime": event["end"],
            "timeZone": "UTC",
        }

    return exchange_event


def create_exchange_event(event_data: dict) -> str:
    """Create an event on Exchange and return its ID."""
    endpoint = "/me/calendar/events"
    if config.MS_CALENDAR_ID:
        cal_id = _validate_id(config.MS_CALENDAR_ID, "calendar ID")
        endpoint = f"/me/calendars/{cal_id}/events"

    resp = ms_auth.graph_request("POST", endpoint, json=event_data)
    if resp.status_code == 201:
        return resp.json()["id"]
    else:
        print(f"  ERROR creating event: HTTP {resp.status_code}")
        return None


def update_exchange_event(exchange_id: str, event_data: dict) -> bool:
    """Update an existing Exchange event."""
    eid = _validate_id(exchange_id, "event ID")
    resp = ms_auth.graph_request("PATCH", f"/me/events/{eid}", json=event_data)
    if resp.status_code == 200:
        return True
    elif resp.status_code == 404:
        return False
    else:
        print(f"  ERROR updating event: HTTP {resp.status_code}")
        return False


def delete_exchange_event(exchange_id: str) -> bool:
    """Delete an event from Exchange."""
    eid = _validate_id(exchange_id, "event ID")
    resp = ms_auth.graph_request("DELETE", f"/me/events/{eid}")
    if resp.status_code in (204, 404):
        return True
    else:
        print(f"  ERROR deleting event: HTTP {resp.status_code}")
        return False


def build_event_hash(event: dict) -> str:
    """Create a hash string to detect changes in an event."""
    return f"{event['start']}|{event['end']}|{event['is_all_day']}"


def run_sync():
    """Run a full sync cycle."""
    print(f"Syncing ICS calendar -> Exchange ({config.SYNC_DAYS_AHEAD} days ahead)...")

    source_events = fetch_source_events()
    print(f"  Found {len(source_events)} events to sync")

    event_map = load_event_map()

    synced_uids = set()
    created = 0
    updated = 0
    deleted = 0

    for event in source_events:
        uid = event["uid"]
        synced_uids.add(uid)

        exchange_payload = source_event_to_exchange(event)
        event_hash = build_event_hash(event)

        if uid in event_map:
            existing = event_map[uid]
            if existing.get("hash") == event_hash:
                continue

            success = update_exchange_event(existing["exchange_id"], exchange_payload)
            if success:
                event_map[uid]["hash"] = event_hash
                updated += 1
            else:
                exchange_id = create_exchange_event(exchange_payload)
                if exchange_id:
                    event_map[uid] = {"exchange_id": exchange_id, "hash": event_hash}
                    created += 1
        else:
            exchange_id = create_exchange_event(exchange_payload)
            if exchange_id:
                event_map[uid] = {"exchange_id": exchange_id, "hash": event_hash}
                created += 1

    for uid in list(event_map.keys()):
        if uid not in synced_uids:
            delete_exchange_event(event_map[uid]["exchange_id"])
            del event_map[uid]
            deleted += 1

    save_event_map(event_map)

    last_sync_file = config.DATA_DIR / "last_sync"
    config.write_restricted(last_sync_file, datetime.now(timezone.utc).isoformat())

    print(f"  Done: {created} created, {updated} updated, {deleted} deleted")
