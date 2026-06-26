#!/usr/bin/env python3
import sys
import json
from datetime import datetime, timedelta
import os

def load_holidays(holidays_path):
    holidays_file = os.path.join(os.path.dirname(__file__), '..', 'references', 'sask_holidays.json')
    try:
        with open(holidays_file) as f:
            data = json.load(f)
            year = datetime.now().year
            return set(data.get(str(year), []))
    except:
        return set()

def generate_ics(events, holidays, output_file):
    tz_offset = '-0600'  # America/Regina standard, no DST for simplicity
    ics_content = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//ClawHub Dev Calendar v1.0//EN
CALSCALE:GREGORIAN
"""

    # Add holidays as all-day
    for h_date in holidays:
        dt = datetime.fromisoformat(h_date + 'T00:00:00{tz}'.format(tz=tz_offset))
        ics_content += f"""BEGIN:VEVENT
UID:holiday-{h_date}@clawhub.dev
DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%S{tz_offset}')}
DTSTART;VALUE=DATE:{dt.strftime('%Y%m%d')}
SUMMARY:SK Statutory Holiday
DESCRIPTION:From sask_holidays.json
END:VEVENT
"""

    for event in events:
        start_str = event['start'].strftime('%Y%m%dT%H%M%S{tz_offset}')
        end_str = event['end'].strftime('%Y%m%dT%H%M%S{tz_offset}')
        uid = event['uid'].replace(' ', '_')
        ics_content += f"""BEGIN:VEVENT
UID:{uid}@clawhub.dev
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
DTSTART:{start_str}
DTEND:{end_str}
SUMMARY:{event['summary']}
DESCRIPTION:{event.get('description', '')}
END:VEVENT
"""

    ics_content += "END:VCALENDAR\n"
    with open(output_file, 'w') as f:
        f.write(ics_content)
    print(f"Generated {len(events)} events + holidays → {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 generate_ics.py project.json [output.ics]")
        sys.exit(1)
    
    proj_path = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else 'dev_calendar.ics'
    
    with open(proj_path) as f:
        proj = json.load(f)
    
    holidays = load_holidays(proj_path)
    
    events = []
    start = datetime.fromisoformat(proj['start'])
    cum_hours = 0
    for m in proj['milestones']:
        duration = timedelta(hours=m['hours'])
        e_start = start + timedelta(hours=cum_hours)
        e_end = e_start + duration
        summary = f"{proj['name']}: {m['name']} ({m['hours']}h @ $150/hr)"
        desc = f"Cumulative: {cum_hours + m['hours']}h. Init fee $500 separate."
        events.append({
            'uid': f"{proj['name']}-{m['name']}",
            'start': e_start,
            'end': e_end,
            'summary': summary,
            'description': desc
        })
        cum_hours += m['hours']
    
    generate_ics(events, holidays, output)
