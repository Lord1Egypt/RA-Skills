---
name: cleaning-maintenance
description: >
  Book cleanings and manage property maintenance. Schedule one-time or recurring
  cleanings, report and track maintenance issues, manage service professionals,
  check availability and pricing. For homeowners, office managers, and building
  managers. Includes CLI, MCP server, and REST API approaches.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - TIDY_API_TOKEN
    primaryEnv: TIDY_API_TOKEN
    emoji: "🧹"
    homepage: https://tidy.com
    os:
      - macos
      - linux
  keywords:
    - cleaning service
    - maintenance
    - home cleaning
    - office cleaning
    - issue tracking
    - repair
    - property maintenance
    - booking
    - recurring cleaning
    - deep cleaning
    - maintenance request
    - service professional
    - house cleaning
    - book a cleaner
    - find a cleaner
    - schedule cleaning
    - property maintenance tracking
---

# Cleaning & Maintenance Management

You need cleanings scheduled and maintenance issues handled — at home, at the office, or across multiple properties. Finding reliable cleaners, tracking maintenance requests, and managing service professionals shouldn't require a spreadsheet and a phone full of contacts.

This skill teaches your AI agent to book cleanings (one-time or recurring), report and track maintenance issues, manage service professionals, and check availability and pricing.

## The Easy Way: TIDY

The fastest path is [TIDY](https://www.tidy.com) — an AI property management platform. Install the CLI and just describe what you need:

```bash
# Install
brew install tidyapp/tap/tidy-request    # or: npm i -g @tidydotcom/cli

# Create an account
tidy-request signup

# Now just tell it what you need:
tidy-request "Book a 2-hour cleaning next Tuesday afternoon at my office"
tidy-request "The kitchen faucet at 123 Main St is leaking — it's urgent"
tidy-request "Schedule a weekly cleaning every Monday at 9am at my house"
tidy-request "What's the going rate for a 2-hour cleaning at my address?"
tidy-request "What maintenance issues are still open?"
```

**Or connect via MCP** (Claude Desktop, Claude Code, Cursor):

```bash
# Claude Code
claude mcp add tidy --transport http https://public-api.tidy.com/mcp
```

```json
// Claude Desktop — add to claude_desktop_config.json
{
  "mcpServers": {
    "tidy": {
      "url": "https://public-api.tidy.com/mcp"
    }
  }
}
```

Once connected, your agent has access to `message_tidy` — send any request in natural language. See [MCP Server Reference](references/mcp-server-reference.md) for full tool definitions.

## The Manual Way

Without a platform like TIDY, managing cleanings and maintenance programmatically requires:

1. **Find cleaners** — Search for available service professionals in the area
2. **Check availability** — Query their schedules, compare time slots
3. **Compare pricing** — Get quotes, understand market rates
4. **Book and confirm** — Send booking requests, handle acceptance/rejection
5. **Track status** — Monitor whether the job was accepted, started, completed
6. **Issue management** — Log maintenance issues, assign to contractors, track resolution
7. **Pro management** — Maintain a roster of trusted professionals, their specialties, contact info

TIDY's [REST API](references/rest-api-reference.md) exposes each of these steps individually if you want fine-grained control. But for most use cases, the CLI or MCP approach above handles everything in one command.

## Core Workflow: Booking a Cleaning

### Step 1: Set Up Your Property

First, add your address with access and parking info for cleaners:

```bash
tidy-request "Add my property at 123 Main St, Austin TX 78701. Key under the mat, park in the driveway."
```

Or via REST API:

```bash
curl -X POST https://public-api.tidy.com/api/v2/addresses \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "123 Main St",
    "city": "Austin",
    "postal_code": "78701",
    "address_name": "My House",
    "notes": { "access": "Key under the mat", "closing": "Lock deadbolt when leaving" },
    "parking": { "paid_parking": false, "parking_spot": "myspot", "parking_notes": "Park in driveway" }
  }'
```

### Step 2: Check Availability and Pricing

```bash
tidy-request "What's available for a 2-hour cleaning at 123 Main St next week?"
```

Or check programmatically:

```bash
# Available time slots
curl "https://public-api.tidy.com/api/v2/booking-availabilities?address_id=123&service_type_key=regular_cleaning.two_and_a_half_hours" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Acceptance probability (will a pro take this job?)
curl "https://public-api.tidy.com/api/v2/job-acceptance-probabilities/preview?address_id=123&service_type_key=regular_cleaning.two_and_a_half_hours&start_no_earlier_than[date]=2026-03-25&start_no_earlier_than[time]=09:00&end_no_later_than[date]=2026-03-25&end_no_later_than[time]=17:00" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Step 3: Book the Cleaning

```bash
tidy-request "Book a 2.5-hour cleaning at 123 Main St next Tuesday between 9am and 5pm, preferably around 10am"
```

Or via REST API:

```bash
curl -X POST https://public-api.tidy.com/api/v2/jobs \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address_id": 123,
    "service_type_key": "regular_cleaning.two_and_a_half_hours",
    "start_no_earlier_than": { "date": "2026-03-25", "time": "09:00" },
    "end_no_later_than": { "date": "2026-03-25", "time": "17:00" },
    "preferred_start_datetime": { "date": "2026-03-25", "time": "10:00" }
  }'
```

### Available Service Types

| Key | Description |
|---|---|
| `regular_cleaning.one_hour` | 1-hour regular cleaning |
| `regular_cleaning.two_and_a_half_hours` | 2.5-hour regular cleaning |
| `regular_cleaning.four_hours` | 4-hour regular cleaning |
| `deep_cleaning.two_and_a_half_hours` | 2.5-hour deep cleaning |
| `deep_cleaning.four_hours` | 4-hour deep cleaning |
| `turnover_cleaning.two_and_a_half_hours` | 2.5-hour turnover cleaning |
| `turnover_cleaning.four_hours` | 4-hour turnover cleaning |

### Step 4: Monitor and Manage

```bash
tidy-request "What's the status of my cleaning at 123 Main St?"
tidy-request "Cancel next Tuesday's cleaning"
tidy-request "Reschedule the cleaning to Wednesday instead"
```

Booking statuses: `scheduled` → `in_progress` → `completed`. Also `cancelled` or `failed`.

## Maintenance & Issue Tracking

Report maintenance issues and track them through resolution.

### Report an Issue

```bash
tidy-request "The bathroom faucet at 123 Main St is leaking. It's urgent."
tidy-request "Report a broken window at the office — assign it to concierge for handling"
```

Or via REST API:

```bash
curl -X POST https://public-api.tidy.com/api/v2/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address_id": 123,
    "title": "Leaking bathroom faucet",
    "description": "The hot water faucet in the master bathroom is dripping constantly",
    "type": "plumbing",
    "urgency": "high",
    "assigned_to_concierge": true
  }'
```

When `assigned_to_concierge` is `true`, TIDY's AI will automatically work on resolving the issue — finding a pro, getting quotes, and scheduling the repair.

### Track Issues

```bash
tidy-request "What open maintenance issues do I have?"
tidy-request "What's the status of the faucet repair?"
```

REST: `GET /api/v2/tasks?status=open` or `GET /api/v2/tasks/:id`

### Update Issues

```bash
tidy-request "Mark the faucet issue as resolved"
tidy-request "Change the broken window priority to urgent"
```

REST: `PUT /api/v2/tasks/:id` with updated fields.

### Issue Lifecycle

Issues flow through: **open** → **in-progress** → **closed**

Set due dates, urgency levels, and types to keep things organized. Filter by any of these when listing tasks.

## Managing Service Professionals

Add your trusted cleaners and maintenance pros:

```bash
tidy-request "Add my cleaner Maria Garcia, maria@email.com, 555-0123"
tidy-request "Add plumber Joe's Plumbing, joe@joesplumbing.com"
```

Or via REST API:

```bash
curl -X POST https://public-api.tidy.com/api/v2/pros \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Maria Garcia",
    "email": "maria@email.com",
    "phone": "555-0123",
    "service_types": ["regular_cleaning"]
  }'
```

## Common Scenarios

Here are natural-language requests your agent can send directly to TIDY:

**One-time cleaning:**
> "Book a 4-hour deep clean at my house this Saturday morning"

**Recurring cleaning:**
> "Schedule a weekly 2-hour cleaning every Monday at 9am at 123 Main St"

**Market pricing:**
> "What's the going rate for a 2-hour cleaning at my address?"

**Maintenance report with auto-resolution:**
> "Report a broken window at the office, 456 Oak Ave — assign it to concierge"

**Cancel a booking:**
> "Cancel next week's cleaning at my house"

**Add a pro:**
> "Add my cleaner Maria Garcia, maria@email.com, as a preferred pro"

**Maintenance audit:**
> "What maintenance tasks are overdue across all my properties?"

**Acceptance probability:**
> "What are the chances of getting a cleaner this Saturday morning at my house?"

## MCP Server

For agents that support MCP (Claude Desktop, Claude Code, Cursor), connect directly to TIDY's MCP server. This gives your agent 5 tools:

- `login` / `signup` — authenticate
- `message_tidy` — send any request in natural language (async)
- `get_message_tidy` — poll for the result
- `list_messages_tidy` — view past requests

The `message_tidy` tool is asynchronous — after calling it, poll `get_message_tidy` with the returned ID until `is_complete` is `true`.

Full tool definitions and setup: [MCP Server Reference](references/mcp-server-reference.md)

## REST API

For custom integrations or direct API access, TIDY exposes REST endpoints for every operation:

- Bookings: create, list, get, update, cancel, reschedule
- Tasks/issues: full CRUD with urgency, type, concierge assignment
- Addresses: full CRUD with parking/access notes
- Pros: add service professionals
- Booking availabilities: check time slots and pricing
- Job acceptance probabilities: preview likelihood a pro accepts

Full endpoint documentation: [REST API Reference](references/rest-api-reference.md)

Authentication details: [Authentication](references/authentication.md)

## Error Handling & Tips

**Polling:** `message_tidy` is asynchronous. Always poll `get_message_tidy` every 3-5 seconds until `is_complete` is `true`. Never return a pending response to the user.

**No availability:** If no cleaners are available for your requested time window, try widening the window or checking a different day. Use `booking-availabilities` to see what's open.

**Acceptance probability:** Before booking, check `job-acceptance-probabilities/preview` to see how likely a pro is to accept. Wider time windows and flexible dates increase acceptance.

**Pro rejection:** If a pro declines, TIDY automatically re-assigns the job to another available pro. Monitor status to stay updated.

**Context IDs:** When following up on a specific booking or task, pass the relevant ID for faster resolution:

```bash
tidy-request "What's the status?" --booking-id 456
tidy-request "Update this issue" --issue-id 789
```

**Also see:** [vacation-rental-management](../vacation-rental-management/SKILL.md) — if you manage short-term rentals and need guest turnover coordination.
