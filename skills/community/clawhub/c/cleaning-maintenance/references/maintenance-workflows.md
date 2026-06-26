# Cleaning & Maintenance Workflows

Detailed end-to-end workflows for common cleaning and maintenance scenarios.

---

## Workflow 1: Maintenance Issue Lifecycle (Complete Example)

A faucet is leaking. Report it, get it fixed, track it through resolution.

### Using the CLI

```bash
# 1. Report the issue
tidy-request "The kitchen faucet at 123 Main St is leaking badly. It's urgent — assign to concierge."

# 2. Check status
tidy-request "What's the status of the faucet issue at 123 Main St?"

# 3. After repair, mark resolved
tidy-request "The faucet at 123 Main St is fixed, mark it as resolved"
```

### Using the REST API

```bash
# 1. Create the task
curl -X POST https://public-api.tidy.com/api/v2/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address_id": 123,
    "title": "Kitchen faucet leaking",
    "description": "The hot water faucet in the kitchen is dripping constantly. Water pooling under the sink.",
    "type": "plumbing",
    "urgency": "high",
    "assigned_to_concierge": true
  }'
# → { "id": 456, "status": "open", ... }

# 2. Check status
curl https://public-api.tidy.com/api/v2/tasks/456 \
  -H "Authorization: Bearer YOUR_TOKEN"
# → { "id": 456, "status": "in_progress", ... }

# 3. Update when resolved
curl -X PUT https://public-api.tidy.com/api/v2/tasks/456 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "status": "closed" }'
```

### Using MCP

```
message_tidy("Kitchen faucet at 123 Main St is leaking. Urgent. Assign to concierge.")
  → { id: 7001, status: "processing", is_complete: false }

get_message_tidy(7001)
  → { id: 7001, status: "completed", is_complete: true,
      response_message: "I've created a maintenance task for the kitchen faucet leak at 123 Main St, marked as urgent, and assigned it to concierge for automatic handling." }
```

---

## Workflow 2: Recurring Cleaning Setup

Set up a regular cleaning schedule:

### Weekly cleaning

```bash
tidy-request "Schedule a 2-hour cleaning every Monday at 9am at my house, 123 Main St"
```

### One-time with follow-up

```bash
# Book one cleaning
tidy-request "Book a 2.5-hour cleaning at 123 Main St next Tuesday between 9am and 5pm"

# After it goes well, set up recurring
tidy-request "That went great — make it weekly, same time"
```

### REST API booking

```bash
curl -X POST https://public-api.tidy.com/api/v2/jobs \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "address_id": 123,
    "service_type_key": "regular_cleaning.two_and_a_half_hours",
    "start_no_earlier_than": { "date": "2025-03-25", "time": "09:00" },
    "end_no_later_than": { "date": "2025-03-25", "time": "17:00" },
    "preferred_start_datetime": { "date": "2025-03-25", "time": "09:00" }
  }'
```

### Manage scheduled cleanings

```bash
# View upcoming
tidy-request "What cleanings do I have scheduled?"

# Skip a week
tidy-request "Cancel next Monday's cleaning — I'll be traveling"

# Reschedule
tidy-request "Move this week's cleaning to Wednesday instead of Monday"
```

---

## Workflow 3: Pro Management and Preferred Scheduling

Add your trusted pros and request them for jobs:

### Add a pro

```bash
tidy-request "Add my cleaner Maria Garcia, maria@email.com, 555-0123"
```

REST API:

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

### Request a specific pro

```bash
tidy-request "Book a cleaning next Tuesday at 123 Main St — request Maria if she's available"
```

### Add multiple pros for different needs

```bash
tidy-request "Add Joe's Plumbing, joe@joesplumbing.com, for maintenance"
tidy-request "Add Sparkle Clean Team, team@sparkleclean.com, for deep cleanings"
```

---

## Workflow 4: Cost Comparison and Market Rates

Before booking, check what's available and how likely it is to get accepted:

### Check availability

```bash
tidy-request "What's available for a 2-hour cleaning at 123 Main St next week?"
```

REST API:

```bash
curl "https://public-api.tidy.com/api/v2/booking-availabilities?address_id=123&service_type_key=regular_cleaning.two_and_a_half_hours" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Check acceptance probability

```bash
tidy-request "What are the chances of getting a cleaner this Saturday morning?"
```

REST API:

```bash
curl "https://public-api.tidy.com/api/v2/job-acceptance-probabilities/preview?address_id=123&service_type_key=regular_cleaning.two_and_a_half_hours&start_no_earlier_than[date]=2025-03-29&start_no_earlier_than[time]=08:00&end_no_later_than[date]=2025-03-29&end_no_later_than[time]=12:00" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Compare service types

```bash
tidy-request "Compare pricing for 1-hour vs 2.5-hour vs 4-hour cleaning at my house"
```

Available service types:

| Key | Duration |
|---|---|
| `regular_cleaning.one_hour` | 1 hour |
| `regular_cleaning.two_and_a_half_hours` | 2.5 hours |
| `regular_cleaning.four_hours` | 4 hours |
| `deep_cleaning.two_and_a_half_hours` | 2.5 hours |
| `deep_cleaning.four_hours` | 4 hours |

---

## Workflow 5: Multi-Property Maintenance Audit

Review maintenance across all properties:

```bash
# See all open issues
tidy-request "What open maintenance issues do I have across all properties?"

# Filter by urgency
tidy-request "Show me all urgent maintenance tasks"

# Filter by type
tidy-request "List all plumbing issues"

# Set due dates
tidy-request "The broken window at 456 Oak Ave needs to be fixed by March 30"
```

REST API:

```bash
# All open tasks
curl "https://public-api.tidy.com/api/v2/tasks?status=open" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Filter by urgency and address
curl "https://public-api.tidy.com/api/v2/tasks?urgency=high&address_id=123" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Update due date
curl -X PUT https://public-api.tidy.com/api/v2/tasks/789 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "due_date": "2025-03-30" }'
```
