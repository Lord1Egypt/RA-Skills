---
name: claw-calendar
description: Create and manage calendar events via Claw Calendar API. Use when users ask to schedule meetings, add reminders, or manage personal calendars. Trigger: "create an event", "add a meeting", "帮我创建日程", "安排一个事件".
version: 1.3.0
homepage: https://github.com/5twang/claw-calendar
repository: https://github.com/5twang/claw-calendar
metadata:
  openclaw:
    requires:
      env:
        - CALENDAR_API_BASE_URL
        - CALENDAR_API_KEY
    primaryEnv: CALENDAR_API_KEY
---

# Claw Calendar

## Overview

This skill enables AI assistants to interact with Claw Calendar, a calendar management API. It provides the ability to create, view, update, and delete calendar events through natural language commands.

## How to Use

When user wants to create/manage calendar events:

1. Check if user has configured:
   - `CALENDAR_API_BASE_URL` (e.g., https://claw-calendar.com)
   - `CALENDAR_API_KEY` (API Key from Claw Calendar settings)

2. If not configured, tell user to configure these environment variables in WorkBuddy settings.

3. If configured, use the API endpoints below.

## API Authentication

**IMPORTANT**: Use `X-API-Key` header, NOT `Authorization: Bearer`

```
Headers:
  X-API-Key: ${CALENDAR_API_KEY}
```

## API Endpoints

Base URL: `${CALENDAR_API_BASE_URL}`

### List Calendars
```
GET /api/calendars
Headers: X-API-Key: ${CALENDAR_API_KEY}
```

### Create Event
```
POST /api/calendars/{calendarId}/events
Headers: 
  X-API-Key: ${CALENDAR_API_KEY}
  Content-Type: application/json
Body: {
  "title": "Event Title",
  "startDate": "YYYY-MM-DD",
  "endDate": "YYYY-MM-DD",
  "startTime": "HH:mm (optional)",
  "endTime": "HH:mm (optional)",
  "isAllDay": true,
  "description": "optional",
  "location": "optional",
  "alarmEnabled": true,
  "alarmMinutes": 15
}
```

### List Events
```
GET /api/events
Headers: X-API-Key: ${CALENDAR_API_KEY}
```

### Update Event
```
PUT /api/calendars/{calendarId}/events/{eventId}
Headers: X-API-Key: ${CALENDAR_API_KEY}
```

### Delete Event
```
DELETE /api/calendars/{calendarId}/events/{eventId}
Headers: X-API-Key: ${CALENDAR_API_KEY}
```

## Response Format

Success: `{ "success": true, event/calendars/events: {...} }`
Error: `{ "success": false, error: { code, message } }`

## Parsing Examples

- "明天上午10点会议" → tomorrow, 10:00
- "下周三生日派对" → next Wednesday
- "今天下午3-4点面试" → today, 15:00-16:00

Defaults: isAllDay=true if no time, alarmMinutes=15, endDate=same as startDate
