---
name: aerobase-calendar
description: Google Calendar sync for flight events
---

# Calendar Sync

Keep the user's travel world in sync. The killer feature: when a new flight is imported,
check the calendar for events within 48 hours of arrival. Calculate body clock time at each event.
"You have a 9 AM board meeting and your body clock will be at 3 AM — push it, or start
pre-adaptation 3 days early."

## API Endpoints

- POST /api/calendar/connect — initiate OAuth (`{ provider: "google" }`)
- GET /api/calendar/connections — list active connections
- POST /api/calendar/disconnect — remove connection (`{ provider }`)
- POST /api/calendar/create-events — create jetlag recovery events
- POST /api/calendar/sync-flight — sync a flight's events to calendar
- POST /api/trips/{tripId}/calendar — sync all trip flights to calendar
- POST /api/calendar/preferences — sync preferences (color, event types, reminders)
- GET /api/calendar/export-ics — ICS export fallback

## Concierge Calendar Integration

**Endpoint:** `GET /api/concierge/instances/{instanceId}/calendar/events`

Returns calendar events for the next 7 days:
```json
{
  "connected": true,
  "events": [
    { "id": "...", "title": "Team Standup", "start": "2026-02-25T10:00:00-08:00", "end": "2026-02-25T10:30:00-08:00", "location": "Zoom" }
  ],
  "count": 5
}
```

The agent uses this to:
1. Get upcoming events within 48h of arrival
2. Calculate body clock time at each event
3. Flag conflicts: "Your 9 AM meeting will be at 3 AM body clock"

## Calendar Event Types

- Flight events (departure/arrival times, gate, terminal)
- Layover activities (tentative)
- Recovery plan milestones (light therapy, sleep windows)
- Hotel check-in/checkout
- Reminders: 24h before (check-in), 3h before (leave for airport)

## Body Clock Conflict Detection

When a new flight is imported:
1. Get events within 48h of arrival from user's calendar
2. Calculate body clock time at each event using origin timezone + flight duration
3. Flag conflicts: "Your 9 AM meeting will happen at 3 AM body clock"
4. Suggest pre-adaptation or rescheduling

## Auto-Sync

- Flight added → calendar event created
- Flight cancelled → calendar event updated/removed
- Flight time changed → calendar event updated, conflicts rechecked

## Access Pattern

The agent accesses Google Calendar through Aerobase API endpoints (backend mediates OAuth tokens).
The agent does not call Google APIs directly.

## Rate Limits

- Calendar sync cron: daily at 08:00 UTC (do not increase). Max 20 events per sync.
- Read upcoming events: max 10/hr. If Google returns 429: back off 15 min.
