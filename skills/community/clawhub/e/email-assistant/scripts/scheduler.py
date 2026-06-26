#!/usr/bin/env python3
"""
Scheduler - Extract calendar events from emails and generate ICS files
"""

import json
import re
import argparse
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from email.utils import parsedate_to_datetime
import uuid


# Date/time patterns to match
DATETIME_PATTERNS = [
    # 2024年3月15日 14:00
    (r"(\d{4})年(\d{1,2})月(\d{1,2})日\s*(\d{1,2}):(\d{2})", "datetime"),
    # 2024-03-15 14:00 or 2024/03/15 14:00
    (r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})\s+(\d{1,2}):(\d{2})", "datetime"),
    # March 15, 2024 14:00
    (r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(\d{1,2}),?\s+(\d{4})\s+(\d{1,2}):(\d{2})", "datetime"),
    # 3月15日 14:00
    (r"(\d{1,2})月(\d{1,2})日\s*(\d{1,2}):(\d{2})", "datetime_short"),
]

DATE_PATTERNS = [
    # 2024年3月15日
    (r"(\d{4})年(\d{1,2})月(\d{1,2})日", "date"),
    # 2024-03-15 or 2024/03/15
    (r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", "date"),
    # March 15, 2024
    (r"(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(\d{1,2}),?\s+(\d{4})", "date_short"),
]

MONTH_MAP = {
    "jan": 1, "january": 1,
    "feb": 2, "february": 2,
    "mar": 3, "march": 3,
    "apr": 4, "april": 4,
    "may": 5,
    "jun": 6, "june": 6,
    "jul": 7, "july": 7,
    "aug": 8, "august": 8,
    "sep": 9, "september": 9,
    "oct": 10, "october": 10,
    "nov": 11, "november": 11,
    "dec": 12, "december": 12,
}


def parse_datetime(match, year_hint=None) -> Optional[datetime]:
    """Parse datetime from regex match."""
    try:
        if len(match.groups()) == 5:
            g = match.groups()
            if g[0].isdigit() and len(g[0]) == 4:  # Full year
                year, month, day, hour, minute = int(g[0]), int(g[1]), int(g[2]), int(g[3]), int(g[4])
            elif g[0].lower() in MONTH_MAP:  # Month name
                month = MONTH_MAP[g[0].lower()]
                day, year, hour, minute = int(g[1]), int(g[2]), int(g[3]), int(g[4])
                if year_hint:
                    year = year_hint
            else:  # Short format (month, day, hour, minute)
                month, day, year, hour, minute = int(g[0]), int(g[1]), year_hint or datetime.now().year, int(g[2]), int(g[3])
            return datetime(year, month, day, hour, minute)
    except Exception:
        pass
    return None


def parse_date(match, year_hint=None) -> Optional[datetime]:
    """Parse date from regex match."""
    try:
        g = match.groups()
        if len(g) >= 3:
            if g[0].isdigit() and len(g[0]) == 4:  # Full format
                year, month, day = int(g[0]), int(g[1]), int(g[2])
                return datetime(year, month, day)
            elif g[0].lower() in MONTH_MAP:  # Month name
                month = MONTH_MAP[g[0].lower()]
                day, year = int(g[1]), int(g[2])
                return datetime(year, month, day)
    except Exception:
        pass
    return None


def extract_ical_events(text: str) -> List[Dict]:
    """Extract iCal events from text."""
    events = []
    # Simple VCALENDAR parser
    if "BEGIN:VEVENT" in text:
        in_event = False
        event_data = {}
        
        for line in text.split('\n'):
            line = line.strip()
            
            if line == "BEGIN:VEVENT":
                in_event = True
                event_data = {}
            elif line == "END:VEVENT":
                in_event = False
                if event_data:
                    events.append(event_data)
            elif in_event:
                if line.startswith("SUMMARY:"):
                    event_data["summary"] = line[8:]
                elif line.startswith("DTSTART"):
                    if ":" in line:
                        event_data["dtstart"] = line.split(":")[1]
                elif line.startswith("DTEND"):
                    if ":" in line:
                        event_data["dtend"] = line.split(":")[1]
                elif line.startswith("DESCRIPTION:"):
                    event_data["description"] = line[12:]
                elif line.startswith("LOCATION:"):
                    event_data["location"] = line[9:]
    
    return events


def extract_text_events(text: str, year_hint=None) -> List[Dict]:
    """Extract events from plain text."""
    events = []
    
    # Try datetime patterns first
    for pattern, ptype in DATETIME_PATTERNS:
        for match in re.finditer(pattern, text):
            dt = None
            if ptype == "datetime":
                dt = parse_datetime(match, year_hint)
            elif ptype == "datetime_short":
                dt = parse_datetime(match, year_hint)
            
            if dt:
                # Extract context (surrounding text)
                start = max(0, match.start() - 30)
                end = min(len(text), match.end() + 100)
                context = text[start:end].strip()
                
                # Try to extract title from context
                title = context.split('\n')[0][:50]
                
                events.append({
                    "dtstart": dt,
                    "dtend": dt + timedelta(hours=1),
                    "summary": title,
                    "description": context,
                    "source": "text"
                })
                break
    
    # Try date patterns
    if not events:
        for pattern, ptype in DATE_PATTERNS:
            for match in re.finditer(pattern, text):
                dt = None
                if ptype == "date":
                    dt = parse_date(match, year_hint)
                elif ptype == "date_short":
                    dt = parse_date(match, year_hint)
                
                if dt:
                    start = max(0, match.start() - 30)
                    end = min(len(text), match.end() + 100)
                    context = text[start:end].strip()
                    title = context.split('\n')[0][:50]
                    
                    events.append({
                        "dtstart": dt,
                        "dtend": dt + timedelta(hours=1),
                        "summary": title,
                        "description": context,
                        "source": "text"
                    })
                    break
    
    return events


def generate_ics(events: List[Dict]) -> str:
    """Generate ICS calendar file content."""
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Email Assistant//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
    ]
    
    for event in events:
        uid = str(uuid.uuid4())
        dtstart = event.get("dtstart")
        dtend = event.get("dtend")
        
        if isinstance(dtstart, datetime):
            dtstart_str = dtstart.strftime("%Y%m%dT%H%M%S")
        else:
            dtstart_str = str(dtstart)
        
        if isinstance(dtend, datetime):
            dtend_str = dtend.strftime("%Y%m%dT%H%M%S")
        else:
            dtend_str = str(dtend)
        
        lines.extend([
            "BEGIN:VEVENT",
            f"UID:{uid}",
            f"DTSTART:{dtstart_str}",
            f"DTEND:{dtend_str}",
            f"SUMMARY:{event.get('summary', 'Event')}",
        ])
        
        if event.get("description"):
            lines.append(f"DESCRIPTION:{event.get('description')}")
        
        if event.get("location"):
            lines.append(f"LOCATION:{event.get('location')}")
        
        lines.extend([
            "END:VEVENT",
        ])
    
    lines.append("END:VCALENDAR")
    return "\n".join(lines)


def load_emails(filepath: str) -> List[Dict]:
    """Load emails from JSON file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and "emails" in data:
                return data["emails"]
            else:
                return [data]
    except Exception as e:
        print(f"✗ Failed to load emails: {e}")
        sys.exit(1)


def extract_events_from_emails(emails: List[Dict]) -> List[Dict]:
    """Extract calendar events from emails."""
    all_events = []
    year_hint = datetime.now().year
    
    for email in emails:
        subject = email.get("subject", "")
        body_text = email.get("body_text", "")
        body_html = email.get("body_html", "")
        preview = email.get("preview", "")
        
        # Combine all text
        full_text = f"{subject}\n{preview}\n{body_text}"
        
        # Extract iCal events
        ical_events = extract_ical_events(full_text)
        for e in ical_events:
            e["email_subject"] = subject
            e["email_from"] = email.get("from", "")
        all_events.extend(ical_events)
        
        # Extract text events
        text_events = extract_text_events(full_text, year_hint)
        for e in text_events:
            e["email_subject"] = subject
            e["email_from"] = email.get("from", "")
        all_events.extend(text_events)
    
    return all_events


def main():
    parser = argparse.ArgumentParser(description="Extract calendar events from emails")
    parser.add_argument("--emails", help="Path to JSON file containing emails")
    parser.add_argument("--output", default="events.ics", help="Output ICS file")
    parser.add_argument("--list", action="store_true", help="List events without generating ICS")
    
    args = parser.parse_args()
    
    if not args.emails:
        parser.print_help()
        sys.exit(1)
    
    print(f"Loading emails from {args.emails}...")
    emails = load_emails(args.emails)
    print(f"Loaded {len(emails)} emails")
    
    print("\nExtracting events...")
    events = extract_events_from_emails(emails)
    
    print(f"Found {len(events)} events")
    
    if args.list:
        for i, event in enumerate(events, 1):
            print(f"\n{i}. {event.get('summary', 'Untitled')}")
            dtstart = event.get("dtstart")
            if isinstance(dtstart, datetime):
                print(f"   Date: {dtstart.strftime('%Y-%m-%d %H:%M')}")
            print(f"   Source: {event.get('source', 'unknown')}")
            if event.get("email_subject"):
                print(f"   From email: {event['email_subject'][:50]}")
    
    if not args.list:
        ics_content = generate_ics(events)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(ics_content)
        print(f"\n✓ Events exported to {args.output}")
        
        # Also save as JSON for debugging
        json_output = args.output.replace(".ics", ".json")
        json_data = []
        for event in events:
            json_event = {
                "summary": event.get("summary"),
                "dtstart": str(event.get("dtstart")) if event.get("dtstart") else None,
                "dtend": str(event.get("dtend")) if event.get("dtend") else None,
                "source": event.get("source"),
                "email_subject": event.get("email_subject"),
            }
            json_data.append(json_event)
        
        with open(json_output, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print(f"✓ Debug data saved to {json_output}")


if __name__ == "__main__":
    main()
