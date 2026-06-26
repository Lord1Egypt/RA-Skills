---
name: daily-digest
description: End-of-day report with trajectory timeline, dwell-time stats, and notification summary
metadata: { "openclaw": { "emoji": "📊" } }
---

# Daily Digest

Compile the day's location trajectory, dwell times, and notifications into a structured daily report.

## Steps

### 1. Get Current State

Call `clawpaw_get_context` for current time, location, and status.

### 2. Query Today's Trajectory

Call `clawpaw_query_events` (type=place_visit, hours=24, limit=100) to get all place visit events today.

Extract from events:
- `enter_place` events: arrival time and place tag/label
- Sort chronologically to build the trajectory timeline
- Calculate dwell time at each place (gap between consecutive enter events)

### 3. Query Notification Stats

Call `clawpaw_notification_changes` (hours=24, limit=100) for today's notification changes.

Aggregate:
- New notification count per app (group by packageName)
- Total notification count
- Top 3 most active apps

### 4. Generate Report

Structure the output:

```
📊 Daily Digest — [Month] [Day], [Weekday]

━━━━━━━━━━━━━━━━━━━━

📍 Trajectory
Home (7h) → Office (9h) → Gym (1.5h) → Home (now)

━━━━━━━━━━━━━━━━━━━━

🕐 Timeline
08:15  Left Home
08:52  Arrived at Office
18:30  Left Office
18:45  Arrived at Gym
20:15  Left Gym
20:35  Arrived Home

━━━━━━━━━━━━━━━━━━━━

⏱️ Dwell Time
Office     ████████████████░░░░  9h 38m (56%)
Home       ████████░░░░░░░░░░░░  7h 35m (28%)
Gym        ███░░░░░░░░░░░░░░░░░  1h 30m (9%)
Commute    ██░░░░░░░░░░░░░░░░░░  1h 17m (7%)

━━━━━━━━━━━━━━━━━━━━

📬 Notifications (XX total)
WeChat: XX | Email: XX | Others: XX

━━━━━━━━━━━━━━━━━━━━

💬 Summary
[Data-driven one-liner, e.g. "A long day at the office — 10 hours — but a gym session to wind down."]
```

### Dwell Time Calculation

1. Each `enter_place` event marks arrival at a place
2. Departure = next `enter_place` event's timestamp
3. Last place's dwell = current time - arrival time
4. UNKNOWN-tagged stays are grouped as "Commute / Transit"
5. Progress bar: █ and ░ characters, 20 chars total

### Summary Generation Guide

Pick the dominant pattern from the data:
- Worked 10+ hours → mention hard work / long day
- Exercised / gym visit → acknowledge healthy habit
- Stayed home all day → "A quiet day at home"
- Visited many places → "A busy day, [X] places visited"
- Lots of notifications → "A notification-heavy day"

## When to Use

- User says "summarize today", "daily report", "how was my day"
- User says "what did I do today", "review my day"
- Evening hours, user is chatting casually

## When NOT to Use

- Morning hours (not enough data yet — use morning-brief instead)
- User is only asking about current location or status
- User is discussing work reports or writing tasks
