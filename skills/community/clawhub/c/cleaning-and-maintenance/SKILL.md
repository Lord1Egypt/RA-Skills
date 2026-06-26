---
name: cleaning-and-maintenance
description: Schedule cleanings, manage maintenance tasks, check availability, and add service professionals with TIDY.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - TIDY_API_TOKEN
    primaryEnv: TIDY_API_TOKEN
    emoji: "🧹"
    homepage: https://tidy.com
---

# Cleaning & Maintenance — TIDY

Schedule and manage cleaning jobs, create maintenance tasks, check booking availability, and add service professionals through the TIDY API. Built for property managers, Airbnb hosts, and cleaning service coordinators.

## Authentication

All requests require a Bearer token.

```bash
# Log in
curl -X POST https://public-api.tidy.com/api/v2/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"jane@example.com","password":"secret123"}'

# Returns: { "token": "abc123..." }
export TIDY_API_TOKEN="abc123..."
```

Tokens do not expire. Include `Authorization: Bearer $TIDY_API_TOKEN` on all requests.

---

## Jobs (Cleaning Bookings)

Jobs represent scheduled cleaning appointments.

### Service Types

| Service Type Key | Description |
|---|---|
| `regular_cleaning.one_hour` | 1-hour regular cleaning |
| `regular_cleaning.two_and_a_half_hours` | 2.5-hour regular cleaning |
| `regular_cleaning.four_hours` | 4-hour regular cleaning |
| `deep_cleaning.two_and_a_half_hours` | 2.5-hour deep cleaning |
| `deep_cleaning.four_hours` | 4-hour deep cleaning |
| `turnover_cleaning.two_and_a_half_hours` | 2.5-hour turnover cleaning |
| `turnover_cleaning.four_hours` | 4-hour turnover cleaning |

### Booking Statuses

`scheduled` → `in_progress` → `completed` or `cancelled` or `failed`

### Check Availability

Before creating a booking, check available time slots:

```bash
curl -s "https://public-api.tidy.com/api/v2/booking-availabilities?address_id=123&service_type_key=regular_cleaning.two_and_a_half_hours" \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

**Required:** `address_id`, `service_type_key`.

### List all jobs

```bash
curl -s https://public-api.tidy.com/api/v2/jobs \
  -H "Authorization: Bearer $TIDY_API_TOKEN"

# Filter by address
curl -s "https://public-api.tidy.com/api/v2/jobs?address_id=123" \
  -H "Authorization: Bearer $TIDY_API_TOKEN"

# Filter by status (comma-separated)
curl -s "https://public-api.tidy.com/api/v2/jobs?status=scheduled,in_progress" \
  -H "Authorization: Bearer $TIDY_API_TOKEN"

# Filter by to-do list
curl -s "https://public-api.tidy.com/api/v2/jobs?to_do_list_id=789" \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

### Get a single job

```bash
curl -s https://public-api.tidy.com/api/v2/jobs/456 \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

Response fields: `id`, `address_id`, `to_do_list_id`, `status`, `price`, `service_type_key`, `service_type_name`, `current_start_datetime` (`date`, `time`), `preferred_start_datetime` (`date`, `time`), `start_no_earlier_than` (`date`, `time`), `end_no_later_than` (`date`, `time`), `is_partially_completed`, `cancelled_by`, `url`, `created_at`.

### Create a job

```bash
curl -X POST https://public-api.tidy.com/api/v2/jobs \
  -H "Authorization: Bearer $TIDY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address_id": 123,
    "service_type_key": "regular_cleaning.two_and_a_half_hours",
    "start_no_earlier_than": { "date": "2026-04-10", "time": "09:00" },
    "end_no_later_than": { "date": "2026-04-10", "time": "17:00" },
    "preferred_start_datetime": { "date": "2026-04-10", "time": "10:00" },
    "to_do_list_id": 789
  }'
```

**Required:** `address_id`, `service_type_key`, `start_no_earlier_than` (with `date` and `time`), `end_no_later_than` (with `date` and `time`).

**Optional:** `preferred_start_datetime` (with `date`, `time`), `to_do_list_id`.

The time window (`start_no_earlier_than` to `end_no_later_than`) defines when the service provider can arrive. `preferred_start_datetime` is a soft preference within that window.

Date format: `YYYY-MM-DD`. Time format: `HH:MM` (24-hour).

### Update a job

```bash
curl -X PUT https://public-api.tidy.com/api/v2/jobs/456 \
  -H "Authorization: Bearer $TIDY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "to_do_list_id": 790,
    "start_no_earlier_than": { "date": "2026-04-11", "time": "08:00" },
    "end_no_later_than": { "date": "2026-04-11", "time": "14:00" }
  }'
```

### Cancel a job

```bash
curl -X POST https://public-api.tidy.com/api/v2/jobs/456/cancel \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

### Reschedule a job

```bash
curl -X POST https://public-api.tidy.com/api/v2/jobs/456/reschedule \
  -H "Authorization: Bearer $TIDY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "service_type_key": "regular_cleaning.two_and_a_half_hours",
    "start_no_earlier_than": { "date": "2026-04-15", "time": "09:00" },
    "end_no_later_than": { "date": "2026-04-15", "time": "17:00" },
    "preferred_start_datetime": { "date": "2026-04-15", "time": "11:00" }
  }'
```

**Required:** `service_type_key`, `start_no_earlier_than`, `end_no_later_than`.

**Optional:** `preferred_start_datetime`, `to_do_list_id`.

---

## Tasks (Maintenance / Issue Reports)

Tasks represent maintenance issues or repair requests tied to a property.

### Task Statuses

`reported` → `in_progress` → `completed`

### Task Urgency Levels

`low`, `normal`, `high`, `emergency`

### List tasks

```bash
curl -s https://public-api.tidy.com/api/v2/tasks \
  -H "Authorization: Bearer $TIDY_API_TOKEN"

# Filter by address, status, type, or urgency (comma-separated)
curl -s "https://public-api.tidy.com/api/v2/tasks?address_id=123&urgency=high" \
  -H "Authorization: Bearer $TIDY_API_TOKEN"

# Filter by concierge assignment
curl -s "https://public-api.tidy.com/api/v2/tasks?assigned_to_concierge=true" \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

### Get a single task

```bash
curl -s https://public-api.tidy.com/api/v2/tasks/789 \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

Response fields: `id`, `address_id`, `title`, `description`, `reporter_type`, `reporter_name`, `type`, `status`, `urgency`, `due_date`, `assigned_to_concierge`, `archived_at`, `created_at`.

### Create a task

```bash
curl -X POST https://public-api.tidy.com/api/v2/tasks \
  -H "Authorization: Bearer $TIDY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address_id": 123,
    "title": "Broken window in master bedroom",
    "description": "The left window pane is cracked and letting in air. Needs glass replacement.",
    "type": "repair",
    "urgency": "high",
    "due_date": "2026-04-05",
    "assigned_to_concierge": true
  }'
```

**Required:** `address_id`, `title`, `description`, `type`.

**Optional:** `status`, `urgency`, `due_date` (`YYYY-MM-DD`), `assigned_to_concierge` (boolean — if `true`, TIDY will auto-handle).

### Update a task

```bash
curl -X PUT https://public-api.tidy.com/api/v2/tasks/789 \
  -H "Authorization: Bearer $TIDY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "in_progress",
    "urgency": "medium",
    "due_date": "2026-04-12"
  }'
```

### Delete a task

```bash
curl -X DELETE https://public-api.tidy.com/api/v2/tasks/789 \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

---

## Service Professionals (Pros)

Add your own cleaning or maintenance professionals to the TIDY platform.

```bash
curl -X POST https://public-api.tidy.com/api/v2/pros \
  -H "Authorization: Bearer $TIDY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Maria Garcia",
    "email": "maria@example.com",
    "phone": "+1-555-0199",
    "service_types": ["regular_cleaning"]
  }'
```

**Required:** `name`, `email`.

**Optional:** `phone`, `service_types` (array, default `["regular_cleaning"]`).

---

## To-Do Lists

To-do lists are cleaning checklists attached to jobs.

```bash
curl -s https://public-api.tidy.com/api/v2/to-do-lists \
  -H "Authorization: Bearer $TIDY_API_TOKEN"

# Filter by address
curl -s "https://public-api.tidy.com/api/v2/to-do-lists?address_id=123" \
  -H "Authorization: Bearer $TIDY_API_TOKEN"
```

---

## Natural Language (message-tidy)

For complex or multi-step operations, send a natural language request:

```bash
curl -X POST https://public-api.tidy.com/api/v2/message-tidy \
  -H "Authorization: Bearer $TIDY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Schedule a deep clean at my Beach House for next Tuesday afternoon",
    "context": { "address_id": 123 }
  }'
```

This is asynchronous. Poll `GET /api/v2/message-tidy/{id}` every 3–5 seconds until `status` is `completed`.

### Example requests

- "Schedule a 2.5 hour deep clean at address 123 for next Tuesday between 9am and 5pm"
- "Cancel booking 456"
- "Reschedule my cleaning to Friday"
- "Create a maintenance task: the dishwasher is leaking at my Beach House"
- "Show me all scheduled cleanings"
- "What time slots are available for a 4-hour cleaning at address 123?"

---

## CLI Alternative

Install: `brew install tidyapp/tap/tidy-request` or `npm i -g @tidydotcom/cli`.

```bash
tidy-request login
tidy-request "Schedule a deep clean for next Tuesday" --address-id 123
tidy-request "Cancel booking 456" --booking-id 456
tidy-request "Report a broken dishwasher" --address-id 123
tidy-request "What cleaning slots are available next week?" --address-id 123
```

---

## Error Handling

| HTTP Status | Error Type | When |
|---|---|---|
| 400 | `invalid_request_error` | Missing or invalid parameters |
| 401 | `authentication_error` | Bad credentials or missing token |
| 404 | `not_found_error` | Resource does not exist |
| 500 | `internal_error` | Server error |
