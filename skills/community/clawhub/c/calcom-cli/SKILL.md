---
name: calcom
description: "Manage Cal.com calendars via CLI - schedules, bookings, event types, slots, user profile. Use when user mentions 'Cal.com', 'scheduling', 'bookings', or needs to interact with the Cal.com API."
category: productivity
---

# calcom-cli

## When To Use This Skill

Use the `calcom-cli` skill when you need to:

- Manage Cal.com schedules (create, update, delete availability)
- View, cancel, reschedule, or confirm bookings
- Create and manage event types
- Check available time slots for scheduling
- View user profile information

## Capabilities

- **Schedules**: List, create, update, delete availability schedules with timezone support
- **Bookings**: List, view, cancel, reschedule, and confirm bookings with filters (status, date range, attendee)
- **Event Types**: Create and manage event types with custom durations, buffers, and booking fields
- **Slots**: Query available time slots for booking
- **Profile**: View current user profile details

## Common Use Cases

- "List all my upcoming bookings"
- "Cancel booking xyz with reason 'Schedule conflict'"
- "Create a new 30-minute meeting event type"
- "Show available slots for tomorrow between 9am and 5pm"
- "Update my work hours schedule to use Pacific timezone"
- "Reschedule booking abc to next Tuesday at 2pm"

## Setup

If `calcom-cli` is not installed, install it from GitHub:
```bash
npx api2cli install Melvynx/calcom-cli
```

If `calcom-cli` is not found, install and build it:
```bash
bun --version || curl -fsSL https://bun.sh/install | bash
npx api2cli bundle calcom
npx api2cli link calcom
```

`api2cli link` adds `~/.local/bin` to PATH automatically. The CLI is available in the next command.

Always use `--json` flag when calling commands programmatically.

## Working Rules

- Always use `--json` for agent-driven calls so downstream steps can parse the result.
- Start with `--help` if the exact action or flags are unclear instead of guessing.
- Prefer read commands first when you need to inspect current state before mutating data.

## Authentication

```bash
calcom-cli auth set "your-token"
calcom-cli auth test
```

Auth commands: `auth set <token>`, `auth show`, `auth remove`, `auth test`

Token is stored in `~/.config/tokens/calcom-cli.txt`.

## Resources

### schedules
Manage availability schedules.
- `list` - List all schedules
- `get <id>` - Get a specific schedule
- `create --name <name> --time-zone <tz>` - Create new schedule
- `update <id> [--name] [--time-zone]` - Update schedule
- `delete <id>` - Delete schedule

### bookings
Manage meeting bookings.
- `list [--status] [--after-start] [--before-end] [--attendee-email]` - List bookings with filters
- `get <uid>` - Get booking details
- `cancel <uid> [--cancellation-reason]` - Cancel a booking
- `reschedule <uid> --start <datetime> [--reschedule-reason]` - Reschedule booking
- `confirm <uid>` - Confirm a pending booking

### event-types
Manage event type configurations.
- `list [--event-slug]` - List all event types
- `get <id>` - Get event type details
- `create --title <title> --slug <slug> --length-in-minutes <n>` - Create event type
- `update <id> [options]` - Update event type
- `delete <id>` - Delete event type

### slots
Query available time slots.
- `list --start-time <datetime> --end-time <datetime> [--event-type-id]` - Get available slots

### me
View user profile.
- `get` - Get current user profile

## Output Format

`--json` returns a standardized envelope:
```json
{ "ok": true, "data": { ... }, "meta": { "total": 42 } }
```

On error: `{ "ok": false, "error": { "message": "...", "status": 401 } }`

## Quick Reference

```bash
calcom-cli --help                    # List all resources and global flags
calcom-cli <resource> --help         # List all actions for a resource
calcom-cli <resource> <action> --help # Show flags for a specific action
```

## Global Flags

All commands support: `--json`, `--format <text|json|csv|yaml>`, `--verbose`, `--no-color`, `--no-header`

Exit codes: 0 = success, 1 = API error, 2 = usage error
