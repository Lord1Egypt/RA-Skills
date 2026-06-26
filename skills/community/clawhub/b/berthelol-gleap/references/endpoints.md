# Gleap REST API -- Endpoint Reference

Base URL: `https://api.gleap.io/v3`

All requests require these headers:

```
Authorization: Bearer $GLEAP_TOKEN
Project: $GLEAP_PROJECT
```

---

## 1. GET `/statistics/facts`

Returns a single aggregate KPI for a given date range. Use this when you need one number (e.g., total new tickets, median reply time).

### Parameters

| Parameter   | Type   | Required | Description                                      |
|-------------|--------|----------|--------------------------------------------------|
| `chartType` | string | yes      | The metric to compute. See chartType table below. |
| `startDate` | string | yes      | ISO 8601 date (`YYYY-MM-DD`)                     |
| `endDate`   | string | yes      | ISO 8601 date (`YYYY-MM-DD`)                     |
| `timezone`  | string | yes      | IANA timezone, e.g. `Europe/Berlin`               |

### Response structure (count metrics)

```json
{
  "title": "New tickets",
  "value": 446,
  "valueUnit": "",
  "progressLabel": "Document Count",
  "progressUnit": "%",
  "progressValue": 12.06
}
```

| Field           | Type   | Description                                                        |
|-----------------|--------|--------------------------------------------------------------------|
| `title`         | string | Human-readable name of the metric                                  |
| `value`         | number | The computed value for the requested date range                    |
| `valueUnit`     | string | Unit for `value` (empty string for counts, `"h"` for hours, etc.) |
| `progressLabel` | string | Label describing what the progress percentage refers to            |
| `progressUnit`  | string | Always `"%"`                                                       |
| `progressValue` | number | Percentage change compared to the previous equivalent period       |

### Response structure (time metrics)

Time-based chartTypes (reply time, close time, etc.) include an extra `rawValue` field:

```json
{
  "title": "Median time to first close",
  "value": 30.56,
  "rawValue": 110028.21,
  "valueUnit": "h",
  "progressLabel": "Median time to first close",
  "progressUnit": "%",
  "progressValue": 25.28
}
```

| Field      | Type   | Description                                                  |
|------------|--------|--------------------------------------------------------------|
| `rawValue` | number | The raw measurement in seconds, before human-friendly conversion |
| `value`    | number | Human-friendly value (converted to the unit in `valueUnit`)  |

### Example

```bash
curl -s "https://api.gleap.io/v3/statistics/facts?\
chartType=NEW_TICKETS&\
startDate=2026-03-01&\
endDate=2026-03-31&\
timezone=Europe/Berlin" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT"
```

---

## 2. GET `/statistics/bar-chart`

Returns time-series data grouped by day, month, or year. Use this when you need to see a metric over time (trends, volume per day, etc.).

### Parameters

| Parameter       | Type   | Required | Description                                      |
|-----------------|--------|----------|--------------------------------------------------|
| `chartType`     | string | yes      | The metric to compute. See chartType table below. |
| `groupInterval` | string | yes      | Grouping: `day`, `month`, or `year`               |
| `startDate`     | string | yes      | ISO 8601 date (`YYYY-MM-DD`)                     |
| `endDate`       | string | yes      | ISO 8601 date (`YYYY-MM-DD`)                     |
| `timezone`      | string | yes      | IANA timezone, e.g. `Europe/Berlin`               |

### Response structure (count metrics)

```json
{
  "title": "New tickets",
  "dataSets": [
    {
      "label": "New tickets",
      "data": [
        { "label": "Feb 23", "value": 20 },
        { "label": "Feb 22", "value": 59 },
        { "label": "Feb 21", "value": 33 }
      ]
    }
  ]
}
```

| Field                    | Type   | Description                                 |
|--------------------------|--------|---------------------------------------------|
| `title`                  | string | Human-readable metric name                  |
| `dataSets`               | array  | Always contains one dataset object          |
| `dataSets[].label`       | string | Dataset label (same as title)               |
| `dataSets[].data`        | array  | Array of data points, one per time bucket   |
| `dataSets[].data[].label`| string | Human-readable date label (e.g. `"Feb 23"`) |
| `dataSets[].data[].value`| number | The metric value for that bucket            |

### Response structure (time metrics)

For time-based chartTypes, each data point includes an additional `count` field:

```json
{
  "title": "Median reply time",
  "dataSets": [
    {
      "label": "Median reply time",
      "data": [
        { "label": "Feb 23", "value": 45.2, "count": 12 },
        { "label": "Feb 22", "value": 38.7, "count": 8 }
      ]
    }
  ]
}
```

| Field   | Type   | Description                                          |
|---------|--------|------------------------------------------------------|
| `count` | number | Number of samples (conversations) used to compute the median |

### Example

```bash
curl -s "https://api.gleap.io/v3/statistics/bar-chart?\
chartType=NEW_TICKETS&\
groupInterval=day&\
startDate=2026-03-01&\
endDate=2026-03-31&\
timezone=Europe/Berlin" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT"
```

---

## 3. GET `/statistics/lists`

Returns tabular data with a columns definition and row data. Used for team performance tables, ticket snapshots, SLA reports, and rating breakdowns.

### Parameters

| Parameter   | Type   | Required | Description                                      |
|-------------|--------|----------|--------------------------------------------------|
| `chartType` | string | yes      | The list type. See below for supported values.    |
| `startDate` | string | yes      | ISO 8601 date (`YYYY-MM-DD`)                     |
| `endDate`   | string | yes      | ISO 8601 date (`YYYY-MM-DD`)                     |
| `timezone`  | string | yes      | IANA timezone, e.g. `Europe/Berlin`               |

### Supported chartType values

| chartType                              | Description                                  |
|----------------------------------------|----------------------------------------------|
| `TEAM_PERFORMANCE_LIST`                | Per-agent performance metrics                |
| `SNAPSHOT_TICKETS`                     | Ticket counts grouped by type/status         |
| `LIVE_AGENTS_TEAM`                     | Currently online agents                      |
| `AVERAGE_RATING_PER_USER_RESULT_LIST`  | Average conversation rating per agent        |
| `TICKETS_WITH_RATING_LIST`             | Individual tickets that received a rating    |
| `SLA_REPORTS_LIST`                     | SLA compliance data                          |

### Response structure: `TEAM_PERFORMANCE_LIST`

```json
{
  "title": "Team performance",
  "columns": [
    { "label": "User", "key": "user" },
    { "label": "Assigned to", "key": "assignedTo" },
    { "label": "Replies sent", "key": "repliesSent" },
    { "label": "First closed", "key": "firstClosed" },
    { "label": "Median reply time", "key": "medianReplyTime" },
    { "label": "Median first reply time", "key": "medianFirstReplyTime" },
    { "label": "Median first assignment reply time", "key": "medianFirstAssignmentReplyTime" },
    { "label": "Median time to close", "key": "medianTimeToClose" },
    { "label": "Tickets worked on", "key": "ticketsWorkedOn" },
    { "label": "Hours active", "key": "hoursActive" },
    { "label": "Conversation rating", "key": "conversationRating" }
  ],
  "data": [
    {
      "user": { "value": "Alice Smith", "rawValue": null, "progressValue": null },
      "assignedTo": { "value": 42, "rawValue": null, "progressValue": 5.0 },
      "repliesSent": { "value": 180, "rawValue": null, "progressValue": 12.3 },
      "firstClosed": { "value": 35, "rawValue": null, "progressValue": -2.1 },
      "medianReplyTime": { "value": 2.4, "rawValue": 8640, "progressValue": -15.0 },
      "medianFirstReplyTime": { "value": 5.1, "rawValue": 18360, "progressValue": 3.2 },
      "medianFirstAssignmentReplyTime": { "value": 1.8, "rawValue": 6480, "progressValue": -8.5 },
      "medianTimeToClose": { "value": 24.3, "rawValue": 87480, "progressValue": 10.0 },
      "ticketsWorkedOn": { "value": 55, "rawValue": null, "progressValue": 7.0 },
      "hoursActive": { "value": 38.5, "rawValue": null, "progressValue": 2.0 },
      "conversationRating": { "value": 4.7, "rawValue": null, "progressValue": 1.5 }
    },
    {
      "user": { "value": "Team average", "rawValue": null, "progressValue": null },
      "assignedTo": { "value": 35, "rawValue": null, "progressValue": 3.0 },
      "repliesSent": { "value": 150, "rawValue": null, "progressValue": 8.0 },
      "firstClosed": { "value": 30, "rawValue": null, "progressValue": -1.0 },
      "medianReplyTime": { "value": 3.1, "rawValue": 11160, "progressValue": -10.0 },
      "medianFirstReplyTime": { "value": 6.0, "rawValue": 21600, "progressValue": 2.0 },
      "medianFirstAssignmentReplyTime": { "value": 2.5, "rawValue": 9000, "progressValue": -5.0 },
      "medianTimeToClose": { "value": 28.0, "rawValue": 100800, "progressValue": 8.0 },
      "ticketsWorkedOn": { "value": 45, "rawValue": null, "progressValue": 5.0 },
      "hoursActive": { "value": 35.0, "rawValue": null, "progressValue": 1.0 },
      "conversationRating": { "value": 4.5, "rawValue": null, "progressValue": 0.5 }
    }
  ]
}
```

**Key notes on `TEAM_PERFORMANCE_LIST`:**

- Every cell (except `user`) is an object with `{ value, rawValue, progressValue }`.
- `rawValue` is populated only for time-based columns (reply time, close time) and holds the value in seconds.
- `progressValue` is the percentage change vs. the previous equivalent period.
- The last row is always `"Team average"` -- an aggregate across all agents.

### Response structure: `SNAPSHOT_TICKETS`

```json
{
  "title": "Ticket snapshot",
  "columns": [
    { "label": "Type", "key": "type" },
    { "label": "Open", "key": "openCount" },
    { "label": "Other status", "key": "otherStatusCount" },
    { "label": "Closed", "key": "closedCount" },
    { "label": "Queued", "key": "queuedCount" }
  ],
  "data": [
    {
      "type": "BUG",
      "openCount": 12,
      "otherStatusCount": 3,
      "closedCount": 45,
      "queuedCount": 2
    }
  ]
}
```

### Example

```bash
curl -s "https://api.gleap.io/v3/statistics/lists?\
chartType=TEAM_PERFORMANCE_LIST&\
startDate=2026-03-01&\
endDate=2026-03-31&\
timezone=Europe/Berlin" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT"
```

---

## 4. GET `/statistics/lists/export`

Same as `/statistics/lists` but returns CSV text instead of JSON. Use this when you need a downloadable or parseable flat-file export.

### Parameters

Same as `/statistics/lists`: `chartType`, `startDate`, `endDate`, `timezone`.

Supports the same `chartType` values: `TEAM_PERFORMANCE_LIST`, `SNAPSHOT_TICKETS`, `LIVE_AGENTS_TEAM`, `AVERAGE_RATING_PER_USER_RESULT_LIST`, `TICKETS_WITH_RATING_LIST`, `SLA_REPORTS_LIST`.

### Response

Raw CSV text. Content-Type is `text/csv`. Example for `TEAM_PERFORMANCE_LIST`:

```
User,Assigned to,Replies sent,First closed,Median reply time,Median first reply time,Median first assignment reply time,Median time to close,Tickets worked on,Hours active,Conversation rating
Alice Smith,42,180,35,2.4h,5.1h,1.8h,24.3h,55,38.5,4.7
Team average,35,150,30,3.1h,6.0h,2.5h,28.0h,45,35.0,4.5
```

### Example

```bash
curl -s "https://api.gleap.io/v3/statistics/lists/export?\
chartType=TEAM_PERFORMANCE_LIST&\
startDate=2026-03-01&\
endDate=2026-03-31&\
timezone=Europe/Berlin" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT"
```

---

## 5. GET `/statistics/heatmap`

Returns volume data bucketed by hour-of-day and weekday. Use this to identify peak support hours.

### Parameters

| Parameter   | Type   | Required | Description                                        |
|-------------|--------|----------|----------------------------------------------------|
| `chartType` | string | yes      | `BUSIEST_HOURS_PER_WEEKDAY` or `BUSIEST_COMMENTS_PER_WEEKDAY` |
| `startDate` | string | yes      | ISO 8601 date (`YYYY-MM-DD`)                       |
| `endDate`   | string | yes      | ISO 8601 date (`YYYY-MM-DD`)                       |
| `timezone`  | string | yes      | IANA timezone, e.g. `Europe/Berlin`                 |

### Response structure

```json
{
  "series": [
    {
      "name": "Monday",
      "data": [
        { "x": "0", "y": 10 },
        { "x": "1", "y": 8 },
        { "x": "2", "y": 3 },
        { "x": "3", "y": 1 },
        { "x": "4", "y": 0 },
        { "x": "5", "y": 2 },
        { "x": "6", "y": 5 },
        { "x": "7", "y": 14 },
        { "x": "8", "y": 22 },
        { "x": "9", "y": 31 },
        { "x": "10", "y": 28 },
        { "x": "11", "y": 35 },
        { "x": "12", "y": 30 },
        { "x": "13", "y": 27 },
        { "x": "14", "y": 25 },
        { "x": "15", "y": 20 },
        { "x": "16", "y": 18 },
        { "x": "17", "y": 15 },
        { "x": "18", "y": 10 },
        { "x": "19", "y": 7 },
        { "x": "20", "y": 5 },
        { "x": "21", "y": 4 },
        { "x": "22", "y": 3 },
        { "x": "23", "y": 2 }
      ]
    },
    { "name": "Tuesday", "data": [ "..." ] },
    { "name": "Wednesday", "data": [ "..." ] },
    { "name": "Thursday", "data": [ "..." ] },
    { "name": "Friday", "data": [ "..." ] },
    { "name": "Saturday", "data": [ "..." ] },
    { "name": "Sunday", "data": [ "..." ] }
  ]
}
```

| Field            | Type   | Description                                        |
|------------------|--------|----------------------------------------------------|
| `series`         | array  | 7 entries, one per weekday (Monday through Sunday)  |
| `series[].name`  | string | Weekday name                                       |
| `series[].data`  | array  | 24 entries, one per hour                           |
| `series[].data[].x` | string | Hour of day as string (`"0"` through `"23"`)   |
| `series[].data[].y` | number | Count for that hour/day combination             |

### Example

```bash
curl -s "https://api.gleap.io/v3/statistics/heatmap?\
chartType=BUSIEST_HOURS_PER_WEEKDAY&\
startDate=2026-03-01&\
endDate=2026-03-31&\
timezone=Europe/Berlin" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT"
```

---

## 6. GET `/statistics/raw-data`

Returns individual event records (raw activity log). Use this when you need event-level detail rather than aggregates.

### Parameters

| Parameter   | Type   | Required | Description                                      |
|-------------|--------|----------|--------------------------------------------------|
| `startDate` | string | yes      | ISO 8601 date (`YYYY-MM-DD`)                     |
| `endDate`   | string | yes      | ISO 8601 date (`YYYY-MM-DD`)                     |
| `timezone`  | string | yes      | IANA timezone, e.g. `Europe/Berlin`               |
| `limit`     | number | no       | Max events to return (for pagination)             |
| `skip`      | number | no       | Number of events to skip (for pagination)         |

### Response structure

Returns an array of event objects. Each event has this shape:

```json
{
  "action": "CREATE_TICKET",
  "createdAt": "2026-03-15T10:23:45.000Z",
  "actionUser": {
    "name": "John Doe",
    "email": "john@example.com"
  },
  "data": {
    "contact": {
      "name": "John Doe",
      "email": "john@example.com"
    },
    "type": "BUG",
    "status": "OPEN"
  }
}
```

### Action types and their data fields

#### `CREATE_TICKET` -- Ticket created

| Field              | Type   | Description                        |
|--------------------|--------|------------------------------------|
| `actionUser`       | object | The user who created the ticket    |
| `data.contact`     | object | Contact info (`name`, `email`)     |
| `data.type`        | string | Ticket type (e.g. `"BUG"`, `"FEATURE_REQUEST"`) |
| `data.status`      | string | Initial status (e.g. `"OPEN"`)     |

#### `TICKET_STATUS_CHANGE` -- Status changed

| Field              | Type   | Description                        |
|--------------------|--------|------------------------------------|
| `data.oldStatus`   | string | Previous status                    |
| `data.newStatus`   | string | New status                         |

#### `ASSIGN_TICKET` -- Ticket assigned to agent

| Field                        | Type   | Description                                   |
|------------------------------|--------|-----------------------------------------------|
| `data.processingUser`        | object | The agent the ticket was assigned to           |
| `data.timeToAssignmentInSec` | number | Seconds from ticket creation to assignment     |

#### `UNASSIGN_TICKET` -- Ticket unassigned from agent

| Field                        | Type   | Description                                   |
|------------------------------|--------|-----------------------------------------------|
| `data.processingUser`        | object | The agent who was unassigned                   |
| `data.timeToAssignmentInSec` | number | Duration of the assignment in seconds          |

#### `TICKET_REPLY` -- Agent replied to ticket

| Field                              | Type   | Description                                           |
|------------------------------------|--------|-------------------------------------------------------|
| `data.processingUser`              | object | The agent who replied                                 |
| `data.replyTimeInSec`             | number | Seconds from last customer message to this reply      |
| `data.workingHourReplyTimeInSec`  | number | Same as above but counting only working hours         |

#### `COMMENT_CREATED` -- Comment added to a ticket

| Field              | Type   | Description                        |
|--------------------|--------|------------------------------------|
| `data.comment`     | string | The comment text                   |
| `actionUser`       | object | Who posted the comment             |

#### `CUSTOMER_SUPPORT_REQUESTED` -- Human support escalation

Fired when a customer explicitly requests human support (e.g., after interacting with the AI bot).

| Field              | Type   | Description                        |
|--------------------|--------|------------------------------------|
| `actionUser`       | object | The customer who requested support |

#### `KAI_INVOLVED` -- AI bot (Kai) entered the conversation

Indicates the AI bot started processing a conversation.

#### `KAI_ANSWERED` -- AI bot provided an answer

Indicates the AI bot successfully answered the customer.

#### `KAI_ANSWERED_WITH_NO_ANSWER` -- AI bot could not answer

Indicates the AI bot was involved but could not provide a satisfactory answer.

#### `KAI_QUESTION` -- AI bot received a question

Logs each question the AI bot received from the customer.

### Example

```bash
curl -s "https://api.gleap.io/v3/statistics/raw-data?\
startDate=2026-03-01&\
endDate=2026-03-31&\
timezone=Europe/Berlin&\
limit=100&\
skip=0" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT"
```

---

## 7. GET `/tickets`

Fetches ticket objects. Returns tickets in chronological order (oldest first). There is no native date filtering on this endpoint -- use `limit` and `skip` to paginate through all tickets.

### Parameters

| Parameter | Type   | Required | Description                           |
|-----------|--------|----------|---------------------------------------|
| `limit`   | number | no       | Max number of tickets to return       |
| `skip`    | number | no       | Number of tickets to skip (offset)    |

### Response structure

```json
{
  "totalCount": 1523,
  "tickets": [
    {
      "id": "abc123",
      "type": "BUG",
      "status": "OPEN",
      "title": "Login button not working",
      "createdAt": "2026-01-15T08:30:00.000Z",
      "updatedAt": "2026-03-20T14:12:00.000Z",
      "contact": {
        "name": "Jane Doe",
        "email": "jane@example.com"
      },
      "processingUser": {
        "name": "Alice Smith",
        "email": "alice@company.com"
      },
      "tags": ["critical", "auth"],
      "priority": "HIGH"
    }
  ]
}
```

| Field        | Type   | Description                                      |
|--------------|--------|--------------------------------------------------|
| `totalCount` | number | Total number of tickets matching the query       |
| `tickets`    | array  | Array of ticket objects                          |

**Important:** Because there is no date filtering, retrieving tickets for a specific period requires paginating through all tickets and filtering by `createdAt` client-side, or using `/statistics/raw-data` with `CREATE_TICKET` events instead.

### Example

```bash
curl -s "https://api.gleap.io/v3/tickets?\
limit=50&\
skip=0" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT"
```

---

## Complete chartType Reference

Every `chartType` value, which endpoints support it, what it measures, and the unit (if applicable).

### Count metrics

| chartType | Endpoints | Measures | Unit |
|-----------|-----------|----------|------|
| `NEW_TICKETS` | facts, bar-chart | Number of new tickets created | count |
| `CLOSED_TICKETS` | facts, bar-chart | Number of tickets closed | count |
| `OPEN_TICKETS` | facts, bar-chart | Number of tickets currently open | count |
| `QUEUED_TICKETS` | facts, bar-chart | Number of tickets in queue | count |
| `TOTAL_REPLIES` | facts, bar-chart | Total agent replies sent | count |
| `TOTAL_COMMENTS` | facts, bar-chart | Total comments (agent + customer) | count |
| `UNIQUE_CONTACTS` | facts, bar-chart | Unique customers who created tickets | count |
| `CUSTOMER_SUPPORT_REQUESTED` | facts, bar-chart | Times a customer requested human support | count |
| `KAI_INVOLVED` | facts, bar-chart | Conversations where the AI bot was involved | count |
| `KAI_ANSWERED` | facts, bar-chart | Conversations where the AI bot answered | count |
| `KAI_ANSWERED_WITH_NO_ANSWER` | facts, bar-chart | Conversations where the AI bot failed to answer | count |
| `KAI_QUESTION` | facts, bar-chart | Total questions received by the AI bot | count |
| `KAI_RESOLUTION_RATE` | facts, bar-chart | Percentage of conversations resolved by AI bot | % |
| `AVERAGE_RATING` | facts, bar-chart | Average conversation rating | rating (1-5) |
| `RATED_CONVERSATIONS` | facts, bar-chart | Number of conversations that received a rating | count |

### Time metrics

| chartType | Endpoints | Measures | Unit |
|-----------|-----------|----------|------|
| `MEDIAN_REPLY_TIME` | facts, bar-chart | Median time for an agent to reply | hours (rawValue in seconds) |
| `MEDIAN_FIRST_REPLY_TIME` | facts, bar-chart | Median time to first agent reply | hours (rawValue in seconds) |
| `MEDIAN_FIRST_ASSIGNMENT_REPLY_TIME` | facts, bar-chart | Median time from assignment to first reply | hours (rawValue in seconds) |
| `MEDIAN_TIME_TO_CLOSE` | facts, bar-chart | Median time from creation to close | hours (rawValue in seconds) |
| `MEDIAN_TIME_TO_FIRST_CLOSE` | facts, bar-chart | Median time from creation to first close | hours (rawValue in seconds) |
| `MEDIAN_TIME_TO_ASSIGNMENT` | facts, bar-chart | Median time from creation to first assignment | hours (rawValue in seconds) |

### List types (for `/statistics/lists` and `/statistics/lists/export` only)

| chartType | Measures |
|-----------|----------|
| `TEAM_PERFORMANCE_LIST` | Per-agent performance metrics (assignments, replies, reply times, close times, hours active, ratings) |
| `SNAPSHOT_TICKETS` | Ticket counts by type and status (open, closed, other, queued) |
| `LIVE_AGENTS_TEAM` | Currently online agents |
| `AVERAGE_RATING_PER_USER_RESULT_LIST` | Average conversation rating broken down per agent |
| `TICKETS_WITH_RATING_LIST` | Individual tickets that received a customer rating |
| `SLA_REPORTS_LIST` | SLA compliance metrics and breach data |

### Heatmap types (for `/statistics/heatmap` only)

| chartType | Measures |
|-----------|----------|
| `BUSIEST_HOURS_PER_WEEKDAY` | Ticket volume by hour-of-day and weekday |
| `BUSIEST_COMMENTS_PER_WEEKDAY` | Comment volume by hour-of-day and weekday |

---

## Pagination pattern

For endpoints that support `limit` and `skip`, use this pattern to iterate through all results:

```bash
SKIP=0
LIMIT=100

while true; do
  RESPONSE=$(curl -s "https://api.gleap.io/v3/statistics/raw-data?\
startDate=2026-03-01&\
endDate=2026-03-31&\
timezone=Europe/Berlin&\
limit=$LIMIT&\
skip=$SKIP" \
    -H "Authorization: Bearer $GLEAP_TOKEN" \
    -H "Project: $GLEAP_PROJECT")

  # Process $RESPONSE here

  COUNT=$(echo "$RESPONSE" | jq 'length')
  if [ "$COUNT" -lt "$LIMIT" ]; then
    break
  fi
  SKIP=$((SKIP + LIMIT))
done
```

---

## Error handling

All endpoints return standard HTTP status codes:

| Status | Meaning |
|--------|---------|
| `200`  | Success |
| `401`  | Invalid or missing `Authorization` header |
| `403`  | Valid token but insufficient permissions, or missing/wrong `Project` header |
| `400`  | Invalid parameters (bad chartType, malformed dates, etc.) |
| `429`  | Rate limited -- back off and retry |
| `500`  | Server error -- retry with backoff |
