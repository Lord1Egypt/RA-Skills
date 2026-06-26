# Claw Calendar API Reference

## Base URL

```
${CALENDAR_API_BASE_URL}
```

This value is configured via the `CALENDAR_API_BASE_URL` environment variable (e.g., https://claw-calendar.com).
The URL should include the API path prefix if your server requires it (e.g., https://claw-calendar.com/api).

## Authentication

**IMPORTANT**: This API uses API Key authentication, NOT Bearer Token.

All API endpoints require the `X-API-Key` header with your API key.

```
X-API-Key: ${CALENDAR_API_KEY}
```

### Obtaining an API Key

1. Log in to your Claw Calendar account at the web interface
2. Go to Settings → API Keys
3. Create a new API Key and copy the value

### Required Environment Variables

| Variable | Description |
|----------|-------------|
| `CALENDAR_API_BASE_URL` | Your Claw Calendar server URL (e.g., https://claw-calendar.com) |
| `CALENDAR_API_KEY` | Your API key from Settings → API Keys |

## Calendar Endpoints

### List Calendars

```
GET /api/calendars
Headers:
  X-API-Key: ${CALENDAR_API_KEY}
```

Returns all calendars owned by the authenticated user.

**Response Fields:**
| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Calendar unique identifier |
| name | string | Calendar display name |
| description | string | Calendar description |
| color | string | Hex color code (e.g., "#4285F4") |
| isPublic | boolean | Whether calendar is publicly accessible |
| eventCount | number | Total events in calendar |
| subscriptionUrl | string | ICS subscription URL |
| createdAt | ISO8601 | Creation timestamp |

### Create Calendar

```
POST /api/calendars
Headers:
  X-API-Key: ${CALENDAR_API_KEY}
  Content-Type: application/json
```

**Request Body:**
```json
{
  "name": "Work Calendar",
  "description": "Work related events",
  "color": "#4285F4",
  "isPublic": false
}
```

### Get Calendar

```
GET /api/calendars/{calendarId}
Headers:
  X-API-Key: ${CALENDAR_API_KEY}
```

### Update Calendar

```
PUT /api/calendars/{calendarId}
Headers:
  X-API-Key: ${CALENDAR_API_KEY}
```

### Delete Calendar

```
DELETE /api/calendars/{calendarId}
Headers:
  X-API-Key: ${CALENDAR_API_KEY}
```

## Event Endpoints

### List Events (All Calendars)

```
GET /api/events
Headers:
  X-API-Key: ${CALENDAR_API_KEY}
```

### List Events (Single Calendar)

```
GET /api/calendars/{calendarId}/events
Headers:
  X-API-Key: ${CALENDAR_API_KEY}
```

### Create Event

```
POST /api/calendars/{calendarId}/events
Headers:
  X-API-Key: ${CALENDAR_API_KEY}
  Content-Type: application/json
```

**Request Body Fields:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| title | string | Yes | Event title (max 255 chars) |
| description | string | No | Event description (max 5000 chars) |
| location | string | No | Event location (max 500 chars) |
| startDate | string | Yes | Start date (YYYY-MM-DD) |
| endDate | string | Yes | End date (YYYY-MM-DD) |
| startTime | string | No | Start time (HH:mm) |
| endTime | string | No | End time (HH:mm) |
| isAllDay | boolean | No | All-day event flag |
| alarmEnabled | boolean | No | Enable reminder |
| alarmMinutes | integer | No | Minutes before event to remind (0-10080, max 7 days) |
| recurrenceRule | string | No | iCal RRULE format |

**Example - All-day event:**
```json
{
  "title": "Team Meeting",
  "description": "Weekly sync",
  "startDate": "2026-05-01",
  "endDate": "2026-05-01",
  "isAllDay": true,
  "alarmEnabled": true,
  "alarmMinutes": 15
}
```

**Example - Timed event:**
```json
{
  "title": "Lunch with John",
  "location": "Restaurant ABC",
  "startDate": "2026-05-01",
  "endDate": "2026-05-01",
  "startTime": "12:00",
  "endTime": "13:00",
  "isAllDay": false,
  "alarmEnabled": true,
  "alarmMinutes": 30
}
```

**Example - Multi-day event:**
```json
{
  "title": "Conference",
  "description": "Annual tech conference",
  "startDate": "2026-06-15",
  "endDate": "2026-06-17",
  "isAllDay": true,
  "alarmEnabled": true,
  "alarmMinutes": 1440
}
```

### Update Event

```
PUT /api/calendars/{calendarId}/events/{eventId}
Headers:
  X-API-Key: ${CALENDAR_API_KEY}
```

All fields optional. Only include fields to update.

### Delete Event

```
DELETE /api/calendars/{calendarId}/events/{eventId}
Headers:
  X-API-Key: ${CALENDAR_API_KEY}
```

Returns the deleted event data (for potential undo functionality).

## Response Format

All responses follow this format:

**Success:**
```json
{
  "success": true,
  "data": { ... }
}
```

**Error:**
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| UNAUTHORIZED | 401 | Invalid or missing API key |
| FORBIDDEN | 403 | No permission to access resource |
| NOT_FOUND | 404 | Resource not found |
| BAD_REQUEST | 400 | Invalid request data |
| VALIDATION_ERROR | 400 | Schema validation failed |
| INTERNAL_ERROR | 500 | Server error |

## Rate Limiting

No rate limiting is enforced at the API level. However, respect the server's resources and avoid excessive requests.

## Schema Definitions

### Event Schema
```javascript
{
  id: UUID,
  calendarId: UUID,
  title: string (1-255),
  description: string (0-5000),
  location: string (0-500),
  startDate: YYYY-MM-DD,
  endDate: YYYY-MM-DD,
  startTime: HH:mm | null,
  endTime: HH:mm | null,
  isAllDay: boolean,
  alarmEnabled: boolean,
  alarmMinutes: integer (0-10080),
  recurrenceRule: string | null,
  createdAt: ISO8601,
  updatedAt: ISO8601
}
```

### Calendar Schema
```javascript
{
  id: UUID,
  userId: UUID,
  name: string (1-255),
  description: string (0-2000),
  color: #RRGGBB,
  isPublic: boolean,
  createdAt: ISO8601,
  updatedAt: ISO8601
}
```
