# Claw Calendar Skill

Smart Calendar Assistant for WorkBuddy - Manage calendars and events via Claw Calendar API.

## Features

- List all calendars
- Create new calendars with .ics subscription URL
- List events with date range filtering
- Create events with reminders

## Quick Start

### 1. Get API Key

1. Sign up at [claw-calendar.com](https://claw-calendar.com)
2. Go to Settings → API Keys
3. Create a new API Key

### 2. Set Environment Variable

```bash
export CLAW_CALENDAR_API_KEY=your-api-key
```

### 3. Create Your First Calendar

```bash
node scripts/create-calendar.js --name "My Calendar" --color "#4f46e5"
```

### 4. Add Events

```bash
node scripts/create-event.js \
  --calendar-id <calendar-id> \
  --title "Meeting" \
  --start-date 2026-04-15 \
  --start-time "14:00:00" \
  --end-time "15:00:00" \
  --alarm
```

## Scripts

| Script | Description |
|--------|-------------|
| `list-calendars.js` | List all calendars |
| `create-calendar.js` | Create a new calendar |
| `list-events.js` | List events in a calendar |
| `create-event.js` | Create a new event |

## License

MIT
