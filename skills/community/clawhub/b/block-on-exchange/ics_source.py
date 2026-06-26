"""ICS calendar source — works with any calendar that provides an ICS/iCal feed."""

from urllib.parse import urlparse

import requests
from icalendar import Calendar

import config

MAX_ICS_SIZE = 10 * 1024 * 1024  # 10 MB


def _validate_ics_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError(f"ICS URL must use HTTPS, got: {parsed.scheme}")
    return url


def fetch_ics() -> Calendar:
    """Fetch and parse an ICS calendar feed."""
    if not config.ICS_URL:
        print("ERROR: ICS calendar URL not configured.")
        print("Add to ~/.calintegration/.env:")
        print("  CALINT_ICS_URL=<your-ics-url>")
        print()
        print("Where to find your ICS URL:")
        print("  Google Calendar:  Settings > your calendar > Integrate > Secret address in iCal format")
        print("  iCloud:           Calendar app > right-click calendar > Share > Public Calendar > copy URL")
        print("  Outlook.com:      Settings > Calendar > Shared calendars > Publish > ICS link")
        print("  Nextcloud:        Calendar > three-dot menu > Copy subscription link")
        print("  Fastmail:         Settings > Calendars > Share/export > ICS URL")
        print("  Any CalDAV:       Check your provider's docs for ICS feed URL")
        raise SystemExit(1)

    url = _validate_ics_url(config.ICS_URL)
    resp = requests.get(url, timeout=30, verify=True)
    resp.raise_for_status()

    if len(resp.content) > MAX_ICS_SIZE:
        print(f"ERROR: ICS feed too large ({len(resp.content)} bytes, max {MAX_ICS_SIZE})")
        raise SystemExit(1)

    return Calendar.from_ical(resp.content)


def setup():
    """Verify ICS calendar access."""
    print("=== ICS Calendar Setup ===")
    cal = fetch_ics()
    name = cal.get("X-WR-CALNAME", "Unknown")
    events = [c for c in cal.walk() if c.name == "VEVENT"]
    print(f"  Calendar: {name}")
    print(f"  Total events in feed: {len(events)}")
    print("  OK!")
    print()
