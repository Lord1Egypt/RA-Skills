---
name: calendar-manager
description: Manage calendar availability, schedule meetings across timezones, find optimal meeting times, and send calendar invites. Use when user wants to (1) find available time slots, (2) schedule meetings, (3) check availability across timezones, (4) generate calendar invite files (.ics), or (5) manage multiple calendars.
---

# Calendar Manager

Find availability and schedule meetings across timezones.

## Core Functions

### Find Availability
```python
# Check for free slots between two datetime ranges
# Default: 9am-5pm local, 30/60min meeting slots
available_slots = find_free_slots(calendar_events, duration=30)
```

### Timezone Conversion
```python
# Convert between timezones
meeting_time = convert_timezone(meeting_time, "America/New_York", "Europe/London")
```

### Generate ICS Files
Create calendar invites users can import:
```python
ics_content = generate_ics(
    summary="Meeting Title",
    description="Meeting details",
    start=datetime(2026, 4, 15, 14, 0),
    duration_minutes=30,
    attendees=["email@example.com"]
)
```

## Workflow

1. **Get constraints** - Duration, date range, participant timezones
2. **Check existing events** - Parse calendar files or ask user
3. **Find slots** - Algorithm: exclude busy times, respect working hours
4. **Suggest times** - Offer 3 best options with timezone context
5. **Create invite** - Generate .ics for selected time

## Output Format

```
📅 Proposed Meeting Times

Option A: Tuesday, April 15 at 2:00 PM EST
  → 7:00 PM London | 9:00 AM Los Angeles

Option B: Wednesday, April 16 at 10:00 AM EST  
  → 3:00 PM London | 7:00 AM Los Angeles

Option C: Thursday, April 17 at 3:00 PM EST
  → 8:00 PM London | 12:00 PM Los Angeles

Reply with A, B, or C to confirm - I'll send invites!
```

## Timezone Reference

Common business timezones:
- EST (America/New_York)
- PST (America/Los_Angeles)
- GMT (Europe/London)
- CET (Europe/Paris)
- JST (Asia/Tokyo)
- IST (Asia/Kolkata)
- AEST (Australia/Sydney)

Use `pytz` or `zoneinfo` for conversions.
