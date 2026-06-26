# Gleap API — Use Cases & Patterns

Common patterns for building support analytics and automations with the Gleap REST API.

**Base URL:** `https://api.gleap.io/v3`
**Auth headers:** `Authorization: Bearer $GLEAP_TOKEN` and `Project: $GLEAP_PROJECT`

---

## Helpers

### Date variables (reused throughout)

```bash
# Today
TODAY_START=$(date -u +%Y-%m-%dT00:00:00.000Z)
TODAY_END=$(date -u +%Y-%m-%dT23:59:59.999Z)

# Yesterday
YESTERDAY_START=$(date -u -v-1d +%Y-%m-%dT00:00:00.000Z)
YESTERDAY_END=$(date -u -v-1d +%Y-%m-%dT23:59:59.999Z)

# Last 7 days
WEEK_START=$(date -u -v-7d +%Y-%m-%dT00:00:00.000Z)

# Previous 7 days (the week before last week, for comparison)
PREV_WEEK_START=$(date -u -v-14d +%Y-%m-%dT00:00:00.000Z)
PREV_WEEK_END=$(date -u -v-8d +%Y-%m-%dT23:59:59.999Z)

# Last 30 days
MONTH_START=$(date -u -v-30d +%Y-%m-%dT00:00:00.000Z)
```

### Time formatting function

Gleap returns time metrics in **seconds**. Use this function to convert to human-readable format:

```bash
fmt_time() {
  local secs="${1%.*}"  # strip decimals
  if [ "$secs" -lt 60 ]; then
    echo "${secs}s"
  elif [ "$secs" -lt 3600 ]; then
    echo "$(echo "scale=1; $secs / 60" | bc)min"
  elif [ "$secs" -lt 86400 ]; then
    echo "$(echo "scale=1; $secs / 3600" | bc)h"
  else
    echo "$(echo "scale=1; $secs / 86400" | bc)d"
  fi
}

# jq equivalent (inline in pipelines):
# jq 'def fmt: if . < 60 then "\(.)s" elif . < 3600 then "\(. / 60 * 10 | round / 10)min" elif . < 86400 then "\(. / 3600 * 10 | round / 10)h" else "\(. / 86400 * 10 | round / 10)d" end;'
```

Examples:
- `fmt_time 45` → `45s`
- `fmt_time 120` → `2.0min`
- `fmt_time 6570` → `1.8h`
- `fmt_time 93600` → `1.0d`

### Pagination pattern

The `/statistics/raw-data` and `/tickets` endpoints support pagination via `limit` and `skip` query parameters.

```bash
# Paginate through raw-data (fetches all pages into a single array)
ALL_DATA="[]"
SKIP=0
LIMIT=500
while true; do
  PAGE=$(curl -s "https://api.gleap.io/v3/statistics/raw-data?chartType=CREATE_TICKET&startDate=$WEEK_START&endDate=$TODAY_END&limit=$LIMIT&skip=$SKIP" \
    -H "Authorization: Bearer $GLEAP_TOKEN" \
    -H "Project: $GLEAP_PROJECT")

  COUNT=$(echo "$PAGE" | jq '.data | length')
  ALL_DATA=$(echo "$ALL_DATA" | jq --argjson page "$(echo "$PAGE" | jq '.data')" '. + $page')

  if [ "$COUNT" -lt "$LIMIT" ]; then
    break
  fi
  SKIP=$((SKIP + LIMIT))
done
echo "$ALL_DATA" | jq 'length'  # total records fetched
```

```bash
# Paginate through tickets
ALL_TICKETS="[]"
SKIP=0
LIMIT=50
while true; do
  PAGE=$(curl -s "https://api.gleap.io/v3/tickets?limit=$LIMIT&skip=$SKIP" \
    -H "Authorization: Bearer $GLEAP_TOKEN" \
    -H "Project: $GLEAP_PROJECT")

  COUNT=$(echo "$PAGE" | jq '.tickets | length')
  ALL_TICKETS=$(echo "$ALL_TICKETS" | jq --argjson page "$(echo "$PAGE" | jq '.tickets')" '. + $page')

  if [ "$COUNT" -lt "$LIMIT" ]; then
    break
  fi
  SKIP=$((SKIP + LIMIT))
done

# Filter to a date range client-side (tickets endpoint has no native date filter)
echo "$ALL_TICKETS" | jq --arg start "$WEEK_START" '[.[] | select(.createdAt >= $start)]'
```

---

## 1. Daily Support Report

Build a comprehensive daily summary covering ticket volume, agent performance, AI involvement, and open ticket snapshot.

### Step 1: Fetch ticket volume metrics

```bash
# New tickets created yesterday
NEW=$(curl -s "https://api.gleap.io/v3/statistics/facts?chartType=NEW_TICKETS_COUNT&startDate=$YESTERDAY_START&endDate=$YESTERDAY_END" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT")

# Tickets closed yesterday
CLOSED=$(curl -s "https://api.gleap.io/v3/statistics/facts?chartType=TICKET_CLOSE_COUNT&startDate=$YESTERDAY_START&endDate=$YESTERDAY_END" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT")

# Replies sent yesterday
REPLIES=$(curl -s "https://api.gleap.io/v3/statistics/facts?chartType=REPLIES_COUNT&startDate=$YESTERDAY_START&endDate=$YESTERDAY_END" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT")

# Combine into a volume summary
jq -n \
  --argjson new "$NEW" \
  --argjson closed "$CLOSED" \
  --argjson replies "$REPLIES" \
  '{
    new_tickets: $new.value,
    closed_tickets: $closed.value,
    net_change: ($new.value - $closed.value),
    replies_sent: $replies.value
  }'
```

### Step 2: AI bot vs human escalations

```bash
# AI-handled tickets
AI=$(curl -s "https://api.gleap.io/v3/statistics/facts?chartType=KAI_INVOLVED&startDate=$YESTERDAY_START&endDate=$YESTERDAY_END" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT")

# Escalated to human
ESCALATED=$(curl -s "https://api.gleap.io/v3/statistics/facts?chartType=CUSTOMER_SUPPORT_REQUESTED&startDate=$YESTERDAY_START&endDate=$YESTERDAY_END" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT")

jq -n \
  --argjson ai "$AI" \
  --argjson esc "$ESCALATED" \
  '{
    ai_handled: $ai.value,
    human_escalated: $esc.value,
    ai_resolution_rate: (if ($ai.value + $esc.value) > 0 then (($ai.value / ($ai.value + $esc.value)) * 100 | round | tostring) + "%" else "N/A" end)
  }'
```

### Step 3: Open ticket snapshot by type

```bash
curl -s "https://api.gleap.io/v3/statistics/lists?chartType=SNAPSHOT_TICKETS&startDate=$YESTERDAY_START&endDate=$YESTERDAY_END" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT" \
  | jq '[.data[] | {type: .type, open: .openCount, closed: .closedCount, total: (.openCount + .closedCount)}]'
```

### Step 4: Per-agent performance

```bash
curl -s "https://api.gleap.io/v3/statistics/lists?chartType=TEAM_PERFORMANCE_LIST&startDate=$YESTERDAY_START&endDate=$YESTERDAY_END" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT" \
  | jq '[.data[] | {
      agent: .processingUserREF,
      assigned: .totalCountForUser.value,
      replies: .commentCount.value,
      closed: .rawClosed.value,
      median_reply_time_seconds: .medianResponseTime.rawValue,
      median_reply_time: (if .medianResponseTime.rawValue then (.medianResponseTime.rawValue / 3600 * 10 | round / 10 | tostring) + "h" else "N/A" end)
    }]'
```

### Step 5: Combine everything into a single report

```bash
# Fetch all pieces (run these first as shown above, storing each in a variable)
# Then combine:
jq -n \
  --argjson new "$NEW" \
  --argjson closed "$CLOSED" \
  --argjson replies "$REPLIES" \
  --argjson ai "$AI" \
  --argjson escalated "$ESCALATED" \
  '{
    report_date: (now | strftime("%Y-%m-%d")),
    volume: {
      new_tickets: $new.value,
      closed_tickets: $closed.value,
      net_change: ($new.value - $closed.value),
      replies_sent: $replies.value
    },
    automation: {
      ai_handled: $ai.value,
      human_escalated: $escalated.value
    }
  }'
```

---

## 2. Weekly Trends Report

Use `/statistics/facts` with a 7-day range. The `progressValue` field automatically compares against the previous equivalent period (i.e., the 7 days before your range).

### Fetch week-over-week changes

```bash
METRICS="NEW_TICKETS_COUNT MEDIAN_FIRST_RESPONSE_TIME MEDIAN_TIME_TO_CLOSE TICKET_CLOSE_COUNT REPLIES_COUNT MEDIAN_REPLY_TIME"

for metric in $METRICS; do
  curl -s "https://api.gleap.io/v3/statistics/facts?chartType=$metric&startDate=$WEEK_START&endDate=$TODAY_END" \
    -H "Authorization: Bearer $GLEAP_TOKEN" \
    -H "Project: $GLEAP_PROJECT"
done | jq -s '[.[] | {
  metric: .title,
  current_value: .value,
  unit: .valueUnit,
  week_over_week_change_pct: .progressValue
}]'
```

### Interpret progressValue

```bash
# progressValue semantics:
#   positive number = increase vs previous period
#   negative number = decrease vs previous period
#   null            = no data for previous period
#
# For volume metrics (tickets, replies):
#   positive = more volume (could be good or bad depending on context)
#
# For time metrics (response time, close time):
#   positive = SLOWER (bad — times increased)
#   negative = FASTER (good — times decreased)

curl -s "https://api.gleap.io/v3/statistics/facts?chartType=MEDIAN_FIRST_RESPONSE_TIME&startDate=$WEEK_START&endDate=$TODAY_END" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT" \
  | jq '{
      metric: .title,
      current_seconds: .value,
      current_human: (if .value < 60 then "\(.value)s" elif .value < 3600 then "\(.value / 60 * 10 | round / 10)min" else "\(.value / 3600 * 10 | round / 10)h" end),
      change_pct: .progressValue,
      direction: (if .progressValue > 0 then "SLOWER (worse)" elif .progressValue < 0 then "FASTER (better)" else "no change" end)
    }'
```

### Full trends summary

```bash
# Fetch all trend metrics into a combined report
TRENDS=$(for metric in NEW_TICKETS_COUNT MEDIAN_FIRST_RESPONSE_TIME MEDIAN_TIME_TO_CLOSE; do
  curl -s "https://api.gleap.io/v3/statistics/facts?chartType=$metric&startDate=$WEEK_START&endDate=$TODAY_END" \
    -H "Authorization: Bearer $GLEAP_TOKEN" \
    -H "Project: $GLEAP_PROJECT"
done | jq -s '.')

echo "$TRENDS" | jq '[.[] | {
  metric: .title,
  value: .value,
  unit: .valueUnit,
  change_pct: .progressValue,
  trend: (
    if .progressValue == null then "no prior data"
    elif .progressValue > 5 then "up significantly"
    elif .progressValue > 0 then "up slightly"
    elif .progressValue > -5 then "down slightly"
    else "down significantly"
    end
  )
}]'
```

---

## 3. Team Performance Dashboard

### Fetch full team performance

```bash
TEAM=$(curl -s "https://api.gleap.io/v3/statistics/lists?chartType=TEAM_PERFORMANCE_LIST&startDate=$WEEK_START&endDate=$TODAY_END" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT")
```

### Extract per-agent metrics

```bash
echo "$TEAM" | jq '[.data[] | {
  agent: .processingUserREF,
  assigned: .totalCountForUser.value,
  replies: .commentCount.value,
  closed: .rawClosed.value,
  median_reply_time_sec: .medianResponseTime.rawValue,
  median_reply_time_human: (
    if .medianResponseTime.rawValue == null then "N/A"
    elif .medianResponseTime.rawValue < 60 then "\(.medianResponseTime.rawValue | round)s"
    elif .medianResponseTime.rawValue < 3600 then "\(.medianResponseTime.rawValue / 60 * 10 | round / 10)min"
    else "\(.medianResponseTime.rawValue / 3600 * 10 | round / 10)h"
    end
  ),
  hours_active: .activeHours.value,
  rating: .medianConversationRating.value
}]'
```

### Filter specific agents

```bash
# Filter to specific agents by name
echo "$TEAM" | jq '[.data[] | select(
  .processingUserREF == "Alice" or
  .processingUserREF == "Bob"
) | {
  agent: .processingUserREF,
  assigned: .totalCountForUser.value,
  replies: .commentCount.value,
  closed: .rawClosed.value
}]'

# Filter agents with more than 10 assigned tickets
echo "$TEAM" | jq '[.data[] | select(.totalCountForUser.value > 10) | {
  agent: .processingUserREF,
  assigned: .totalCountForUser.value
}]'
```

### Team average (last row)

The team average is always the last entry in the `data` array:

```bash
echo "$TEAM" | jq '.data[-1] | {
  label: .processingUserREF,
  avg_assigned: .totalCountForUser.value,
  avg_replies: .commentCount.value,
  avg_closed: .rawClosed.value,
  avg_reply_time_sec: .medianResponseTime.rawValue,
  avg_rating: .medianConversationRating.value
}'
```

### Compare each agent to team average

```bash
echo "$TEAM" | jq '
  (.data[-1]) as $avg |
  [.data[:-1][] | {
    agent: .processingUserREF,
    assigned: .totalCountForUser.value,
    vs_avg_assigned: (if $avg.totalCountForUser.value > 0 then ((.totalCountForUser.value / $avg.totalCountForUser.value - 1) * 100 | round | tostring) + "%" else "N/A" end),
    closed: .rawClosed.value,
    vs_avg_closed: (if $avg.rawClosed.value > 0 then ((.rawClosed.value / $avg.rawClosed.value - 1) * 100 | round | tostring) + "%" else "N/A" end)
  }]'
```

### Export as CSV

```bash
curl -s "https://api.gleap.io/v3/statistics/lists/export?chartType=TEAM_PERFORMANCE_LIST&startDate=$WEEK_START&endDate=$TODAY_END&timezone=Europe/Paris" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT" \
  -o team_performance.csv

# Preview the CSV
head -5 team_performance.csv
```

---

## 4. Peak Hours Analysis

### Fetch heatmap data

```bash
HEATMAP=$(curl -s "https://api.gleap.io/v3/statistics/heatmap?chartType=BUSIEST_HOURS_PER_WEEKDAY&startDate=$MONTH_START&endDate=$TODAY_END&timezone=Europe/Paris" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT")
```

### Find busiest hours per day

```bash
# For each day, find the hour with the highest ticket volume
echo "$HEATMAP" | jq '[.series[] | {
  day: .name,
  busiest_hour: (.data | max_by(.y) | .x),
  ticket_count: (.data | max_by(.y) | .y),
  top_3_hours: [.data | sort_by(-.y) | .[:3][] | {hour: .x, count: .y}]
}]'
```

### Find busiest day of the week

```bash
# Sum ticket volume across all hours for each day
echo "$HEATMAP" | jq '[.series[] | {
  day: .name,
  total_tickets: ([.data[].y] | add)
}] | sort_by(-.total_tickets)'
```

### Find overall peak hour across the entire week

```bash
echo "$HEATMAP" | jq '[.series[] | .name as $day | .data[] | {day: $day, hour: .x, count: .y}] | max_by(.count)'
```

### Build a scheduling recommendation

```bash
# Find hours with above-average volume (candidate hours for extra staffing)
echo "$HEATMAP" | jq '
  [.series[] | .name as $day | .data[] | {day: $day, hour: .x, count: .y}] as $all |
  ($all | map(.count) | add / length) as $avg |
  {
    average_hourly_volume: ($avg | round),
    high_volume_slots: [$all[] | select(.count > ($avg * 1.5)) | {day, hour, count}] | sort_by(-.count),
    low_volume_slots: [$all[] | select(.count < ($avg * 0.3) and .count > 0) | {day, hour, count}] | sort_by(.count)
  }'
```

---

## 5. Ticket Topic Analysis

### Fetch raw ticket creation events

```bash
RAW_TICKETS=$(curl -s "https://api.gleap.io/v3/statistics/raw-data?chartType=CREATE_TICKET&startDate=$WEEK_START&endDate=$TODAY_END&limit=10000" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT")

# Count of tickets created
echo "$RAW_TICKETS" | jq '.data | length'
```

### Fetch actual ticket objects

```bash
# Get tickets and filter to recent ones
TICKETS=$(curl -s "https://api.gleap.io/v3/tickets?limit=100&skip=0" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT")

# Filter to tickets created in the last 7 days
echo "$TICKETS" | jq --arg start "$WEEK_START" '[.tickets[] | select(.createdAt >= $start) | {
  id: .ticketNumber,
  title: .title,
  type: .type,
  status: .status,
  created: .createdAt
}]'
```

### Extract ticket titles for topic analysis

```bash
# Get all recent ticket titles as a newline-separated list
echo "$TICKETS" | jq -r --arg start "$WEEK_START" '.tickets[] | select(.createdAt >= $start) | .title'
```

### Pattern: Pass titles to an LLM for topic clustering

```bash
# 1. Extract titles to a file
echo "$TICKETS" | jq -r --arg start "$WEEK_START" \
  '.tickets[] | select(.createdAt >= $start) | .title' > /tmp/gleap_titles.txt

# 2. Count raw titles
wc -l /tmp/gleap_titles.txt

# 3. Use the titles file as input to an LLM prompt
# With Claude Code, you can read the file and ask:
#   "Cluster these support ticket titles into topic groups and rank by frequency:
#    $(cat /tmp/gleap_titles.txt)"
#
# Or via the Anthropic API:
TITLES=$(cat /tmp/gleap_titles.txt)
curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d "$(jq -n --arg titles "$TITLES" '{
    model: "claude-sonnet-4-20250514",
    max_tokens: 1024,
    messages: [{
      role: "user",
      content: ("Cluster these support ticket titles into topic groups. Rank topics by frequency. Return JSON with {topics: [{name, count, example_titles}]}.\n\nTitles:\n" + $titles)
    }]
  }')" | jq '.content[0].text | fromjson'
```

### Ticket type distribution (without LLM)

```bash
# Group tickets by type
echo "$TICKETS" | jq --arg start "$WEEK_START" '
  [.tickets[] | select(.createdAt >= $start)] | group_by(.type) |
  [.[] | {type: .[0].type, count: length}] | sort_by(-.count)'
```

---

## 6. SLA Monitoring

### Track SLA breaches vs started

```bash
# SLA breaches in the period
BREACHES=$(curl -s "https://api.gleap.io/v3/statistics/facts?chartType=SLA_BREACHES_COUNT&startDate=$WEEK_START&endDate=$TODAY_END" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT")

# SLA tracking started (total tickets under SLA)
STARTED=$(curl -s "https://api.gleap.io/v3/statistics/facts?chartType=SLA_STARTED_COUNT&startDate=$WEEK_START&endDate=$TODAY_END" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT")

# Calculate compliance rate
jq -n \
  --argjson breaches "$BREACHES" \
  --argjson started "$STARTED" \
  '{
    sla_started: $started.value,
    sla_breaches: $breaches.value,
    compliance_rate: (if $started.value > 0 then ((($started.value - $breaches.value) / $started.value) * 100 * 10 | round / 10 | tostring) + "%" else "N/A" end),
    breach_trend_pct: $breaches.progressValue
  }'
```

### SLA breach trend over time

```bash
curl -s "https://api.gleap.io/v3/statistics/bar-chart?chartType=SLA_BREACHES_COUNT&startDate=$MONTH_START&endDate=$TODAY_END&timezone=Europe/Paris" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT" \
  | jq '[.series[0].data[] | select(.y > 0) | {date: .x, breaches: .y}]'
```

### SLA reports list (detailed compliance data)

```bash
curl -s "https://api.gleap.io/v3/statistics/lists?chartType=SLA_REPORTS_LIST&startDate=$WEEK_START&endDate=$TODAY_END" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT" \
  | jq '.data'
```

### Daily SLA compliance check

```bash
# Useful for a daily alert: did we breach any SLAs yesterday?
YESTERDAY_BREACHES=$(curl -s "https://api.gleap.io/v3/statistics/facts?chartType=SLA_BREACHES_COUNT&startDate=$YESTERDAY_START&endDate=$YESTERDAY_END" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT" | jq '.value')

if [ "$YESTERDAY_BREACHES" -gt 0 ]; then
  echo "WARNING: $YESTERDAY_BREACHES SLA breach(es) yesterday"
else
  echo "All SLAs met yesterday"
fi
```

---

## 7. Integration Patterns

### Push to Notion

Create a page in a Notion database with the daily report data.

```bash
# 1. Fetch your Gleap metrics (from use case 1)
NEW_COUNT=$(echo "$NEW" | jq '.value')
CLOSED_COUNT=$(echo "$CLOSED" | jq '.value')
REPLIES_COUNT=$(echo "$REPLIES" | jq '.value')

# 2. Create a Notion page via the Notion API
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" \
  -H "Notion-Version: 2022-06-28" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg db_id "$NOTION_DATABASE_ID" \
    --arg date "$(date +%Y-%m-%d)" \
    --argjson new "$NEW_COUNT" \
    --argjson closed "$CLOSED_COUNT" \
    --argjson replies "$REPLIES_COUNT" \
    '{
      parent: {database_id: $db_id},
      properties: {
        "Date": {date: {start: $date}},
        "New Tickets": {number: $new},
        "Closed Tickets": {number: $closed},
        "Replies": {number: $replies},
        "Net Change": {number: ($new - $closed)}
      }
    }')"
```

If using the Notion MCP (available in Claude Code), you can create pages directly by asking Claude to use the `notion-create-pages` tool with the data.

### Push to Slack

Post a daily summary to a Slack channel via incoming webhook.

```bash
# 1. Build the report (reuse variables from use case 1)
# 2. Post to Slack
curl -s -X POST "$SLACK_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --argjson new "$(echo "$NEW" | jq '.value')" \
    --argjson closed "$(echo "$CLOSED" | jq '.value')" \
    --argjson replies "$(echo "$REPLIES" | jq '.value')" \
    --argjson ai "$(echo "$AI" | jq '.value')" \
    --argjson escalated "$(echo "$ESCALATED" | jq '.value')" \
    '{
      text: "Daily Support Report",
      blocks: [
        {type: "header", text: {type: "plain_text", text: "Daily Support Report"}},
        {type: "section", text: {type: "mrkdwn", text: ("*New tickets:* \($new) | *Closed:* \($closed) | *Net:* \($new - $closed)\n*Replies sent:* \($replies)\n*AI handled:* \($ai) | *Human escalated:* \($escalated)")}},
      ]
    }')"
```

For Slack Bot API (richer formatting):

```bash
curl -s -X POST "https://slack.com/api/chat.postMessage" \
  -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  -H "Content-Type: application/json" \
  -d "$(jq -n \
    --arg channel "$SLACK_CHANNEL" \
    --arg text "Daily Support Report: \(env.NEW_COUNT) new, \(env.CLOSED_COUNT) closed" \
    '{channel: $channel, text: $text}')"
```

### Save to files

```bash
# Save as JSON
REPORT=$(jq -n \
  --argjson new "$NEW" \
  --argjson closed "$CLOSED" \
  '{date: (now | strftime("%Y-%m-%d")), new: $new.value, closed: $closed.value}')

echo "$REPORT" > /tmp/gleap_report_$(date +%Y%m%d).json

# Save as Markdown
cat > /tmp/gleap_report_$(date +%Y%m%d).md <<REPORT_EOF
# Support Report — $(date +%Y-%m-%d)

| Metric | Value |
|--------|-------|
| New tickets | $(echo "$NEW" | jq '.value') |
| Closed tickets | $(echo "$CLOSED" | jq '.value') |
| Replies sent | $(echo "$REPLIES" | jq '.value') |
| AI handled | $(echo "$AI" | jq '.value') |
| Escalated | $(echo "$ESCALATED" | jq '.value') |
REPORT_EOF

# Save team CSV export to project directory
curl -s "https://api.gleap.io/v3/statistics/lists/export?chartType=TEAM_PERFORMANCE_LIST&startDate=$WEEK_START&endDate=$TODAY_END&timezone=Europe/Paris" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT" \
  -o ./reports/team_$(date +%Y%m%d).csv
```

---

## 8. Automation: Scheduled Reports

### Cron-based pattern

Create a script and schedule it with cron:

```bash
#!/usr/bin/env bash
# /path/to/gleap_daily_report.sh
# Run daily at 8am: 0 8 * * * /path/to/gleap_daily_report.sh

set -euo pipefail

export GLEAP_TOKEN="your-token-here"   # or source from a secrets file
export GLEAP_PROJECT="your-project-id"

YESTERDAY_START=$(date -u -v-1d +%Y-%m-%dT00:00:00.000Z)
YESTERDAY_END=$(date -u -v-1d +%Y-%m-%dT23:59:59.999Z)

# Fetch metrics
NEW=$(curl -s "https://api.gleap.io/v3/statistics/facts?chartType=NEW_TICKETS_COUNT&startDate=$YESTERDAY_START&endDate=$YESTERDAY_END" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT" | jq '.value')

CLOSED=$(curl -s "https://api.gleap.io/v3/statistics/facts?chartType=TICKET_CLOSE_COUNT&startDate=$YESTERDAY_START&endDate=$YESTERDAY_END" \
  -H "Authorization: Bearer $GLEAP_TOKEN" \
  -H "Project: $GLEAP_PROJECT" | jq '.value')

# Post to Slack
curl -s -X POST "$SLACK_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Yesterday: $NEW new tickets, $CLOSED closed (net: $((NEW - CLOSED)))\"}"
```

Add to crontab:

```bash
# Daily at 8am
crontab -e
# Add: 0 8 * * * /path/to/gleap_daily_report.sh

# Weekly on Monday at 9am
# Add: 0 9 * * 1 /path/to/gleap_weekly_report.sh
```

### Claude Code scheduled agents

You can also use Claude Code's scheduled agent feature to run reports automatically. This is useful when you want Claude to interpret the data and write summaries in natural language.

Set up a scheduled agent that:
1. Fetches Gleap metrics using the patterns above
2. Analyzes trends and anomalies
3. Posts a formatted summary to Slack or saves to a file

Use `/schedule` in Claude Code to create a trigger, for example:
- **Daily report**: runs every morning, fetches yesterday's data, posts to Slack
- **Weekly digest**: runs Monday morning, compares this week vs last week, saves report

The agent has access to all the curl patterns in this file and can combine them with natural language analysis.
