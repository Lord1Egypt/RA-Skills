---
name: discord-event-planner
description: Plan and coordinate events in Discord. Use when users ask to create, schedule, or manage events, plan meetups, organize activities, set up reminders, or track RSVPs in Discord.
---

# Discord Event Planner

Organize events in Discord with scheduling, RSVP tracking, and reminders.

## Commands

### Create Event
```
!event create <title> <YYYY-MM-DD> <HH:MM> [description]
```
- Title: required, event name
- Date/time: required, use 24h format
- Description: optional, event details

### List Events
```
!event list
```
Shows all upcoming events with date, time, title, and RSVP count.

### RSVP
```
!event rsvp <event-id> <attend|maybe|decline>
```
- `attend` - definitely going
- `maybe` - might attend  
- `decline` - can't make it

### Cancel Event
```
!event cancel <event-id>
```
Deletes the event and notifies attendees.

### Event Details
```
!event show <event-id>
```
Shows full event info with RSVP list.

## Storage

Events stored in `events.json`:
```json
{
  "events": {
    "evt_001": {
      "id": "evt_001",
      "title": "Game Night",
      "date": "2026-05-15",
      "time": "20:00",
      "description": "Weekly gaming session",
      "created_by": "user123",
      "rsvps": {
        "attend": ["user1", "user2"],
        "maybe": ["user3"],
        "decline": []
      }
    }
  },
  "next_id": 2
}
```

## Script Usage

```bash
python scripts/event_manager.py create "Game Night" "2026-05-15" "20:00" "Weekly gaming"
python scripts/event_manager.py list
python scripts/event_manager.py rsvp evt_001 attend
python scripts/event_manager.py show evt_001
python scripts/event_manager.py cancel evt_001
```

## Discord Formatting

- Event cards use block quotes with borders
- Timestamps show in user-friendly format
- RSVP counts color-coded: green (attend), yellow (maybe), red (decline)

## Workflow

1. User requests event creation → parse args → validate date → save
2. RSVP updates → modify the rsvps object → save
3. List events → sort by date → show upcoming only
4. Cancel → remove from events → save