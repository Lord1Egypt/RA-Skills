---
name: date-and-time-calculator
description: "Date and Time Calculator: Date/time calculations: add/subtract days, business days, time until/since, timezone conversion, week. Use when an agent needs date and time calculator, date calculator and timestamp tool set, building countdown timers for events or deadlines, calculating project durations in business days excluding weekends, scheduling meetings across multiple timezones, converting api timestamps to human readable formats, add days, date through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/date-calculator-and-timestamp-tool-set
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/date-calculator-and-timestamp-tool-set"}}
---
# Date and Time Calculator

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Time Tools is a date and time utility providing 18 operations across two categories: time calculations and format conversions.
Time calculation operations handle date arithmetic and temporal analysis. These include calculating time remaining until a future date, calculating time elapsed since a past date, adding or subtracting days from a date, counting total days between two dates, counting business days (weekdays only) between two dates, converting datetimes between timezones, retrieving UTC offset for any timezone, formatting duration in seconds to human-readable text, parsing human-readable duration strings (such as "2h 30m") into seconds, getting ISO week number for a date, determining fiscal quarter (1–4), checking leap year status, checking if two time periods overlap, and converting Unix timestamps to ISO format.
Conversion operations handle format transformations between Unix timestamps, formatted date strings, and human-readable durations. Unix timestamps can be converted to formatted dates with optional timezone specification, date strings can be converted to Unix timestamps using configurable format patterns, and raw seconds can be converted to compact human-readable format (such as "1d 2h 30m 15s").
Date parsing is flexible and accepts multiple input formats. All timezone operations use the pytz library and support standard timezone names.

## Product Instructions
### Date and Time Calculator

Comprehensive date/time calculations, timezone conversions, and duration tools.

#### Actions

##### time-until
Calculate time remaining until a future date.
- **Required:** `target_date` (string) - Target date in ISO or parseable format
- **Example:** `{"action": "time-until", "target_date": "2026-12-31T23:59:59"}`

##### time-since
Calculate time elapsed since a past date.
- **Required:** `past_date` (string) - Past date in ISO or parseable format
- **Example:** `{"action": "time-since", "past_date": "2024-01-01"}`

##### add-days
Add a number of days to a date.
- **Required:** `date` (string) - Starting date; `days` (integer) - Number of days to add
- **Example:** `{"action": "add-days", "date": "2026-03-10", "days": 30}`

##### subtract-days
Subtract a number of days from a date.
- **Required:** `date` (string) - Starting date; `days` (integer) - Number of days to subtract
- **Example:** `{"action": "subtract-days", "date": "2026-03-10", "days": 14}`

##### add-hours
Add hours to a datetime.
- **Required:** `date` (string) - Starting datetime; `hours` (number) - Hours to add
- **Example:** `{"action": "add-hours", "date": "2026-03-10T09:00:00", "hours": 5.5}`

##### subtract-hours
Subtract hours from a datetime.
- **Required:** `date` (string) - Starting datetime; `hours` (number) - Hours to subtract
- **Example:** `{"action": "subtract-hours", "date": "2026-03-10T17:00:00", "hours": 3}`

##### add-minutes
Add minutes to a datetime.
- **Required:** `date` (string) - Starting datetime; `minutes` (number) - Minutes to add
- **Example:** `{"action": "add-minutes", "date": "2026-03-10T09:00:00", "minutes": 45}`

##### subtract-minutes
Subtract minutes from a datetime.
- **Required:** `date` (string) - Starting datetime; `minutes` (number) - Minutes to subtract
- **Example:** `{"action": "subtract-minutes", "date": "2026-03-10T10:30:00", "minutes": 15}`

##### days-between
Calculate the number of calendar days between two dates.
- **Required:** `start_date` (string) - Start date; `end_date` (string) - End date
- **Example:** `{"action": "days-between", "start_date": "2026-01-01", "end_date": "2026-12-31"}`

##### business-days-between
Calculate the number of business days (weekdays only, Mon-Fri) between two dates.
- **Required:** `start_date` (string) - Start date; `end_date` (string) - End date
- **Example:** `{"action": "business-days-between", "start_date": "2026-03-01", "end_date": "2026-03-31"}`

##### convert-timezone
Convert a datetime from one timezone to another.
- **Required:** `date_string` (string) - Datetime to convert; `from_timezone` (string) - Source timezone; `to_timezone` (string) - Target timezone
- **Example:** `{"action": "convert-timezone", "date_string": "2026-03-10 09:00:00", "from_timezone": "America/New_York", "to_timezone": "Europe/London"}`

##### timezone-offset
Get the current UTC offset for a timezone.
- **Required:** `timezone` (string) - Timezone name (e.g., "America/New_York", "Europe/London", "Asia/Tokyo")
- **Example:** `{"action": "timezone-offset", "timezone": "America/Los_Angeles"}`

##### format-duration
Format a number of seconds into human-readable text (e.g., "2 days, 3 hours, 15 minutes").
- **Required:** `seconds` (number) - Duration in seconds
- **Example:** `{"action": "format-duration", "seconds": 90061}`

##### parse-duration
Parse a human-readable duration string into total seconds. Supports units: s/sec/seconds, m/min/minutes, h/hr/hours, d/day/days.
- **Required:** `duration_str` (string) - Duration text to parse
- **Example:** `{"action": "parse-duration", "duration_str": "2h 30m 15s"}`

##### week-number
Get the ISO week number (1-53) for a date.
- **Required:** `date` (string) - Date to check
- **Example:** `{"action": "week-number", "date": "2026-03-10"}`

##### quarter
Get the fiscal quarter (1-4) for a date.
- **Required:** `date` (string) - Date to check
- **Example:** `{"action": "quarter", "date": "2026-08-15"}`

##### is-leap-year
Check whether a given year is a leap year.
- **Required:** `year` (integer) - Year to check (minimum: 1)
- **Example:** `{"action": "is-leap-year", "year": 2028}`

##### working-hours-overlap
Check whether two time periods overlap (useful for scheduling across time zones).
- **Required:** `start1` (string) - Start of first period (HH:MM); `end1` (string) - End of first period (HH:MM); `start2` (string) - Start of second period (HH:MM); `end2` (string) - End of second period (HH:MM)
- **Example:** `{"action": "working-hours-overlap", "start1": "09:00", "end1": "17:00", "start2": "14:00", "end2": "22:00"}`

##### unix-to-iso
Convert a Unix timestamp to ISO 8601 format.
- **Required:** `timestamp` (number) - Unix timestamp in seconds
- **Example:** `{"action": "unix-to-iso", "timestamp": 1773331200}`

##### unix-to-date
Convert a Unix timestamp to a formatted date string, optionally in a specific timezone.
- **Required:** `timestamp` (number) - Unix timestamp in seconds
- **Optional:** `timezone` (string) - Timezone name (defaults to local time)
- **Example:** `{"action": "unix-to-date", "timestamp": 1773331200, "timezone": "America/Chicago"}`

##### date-to-unix
Convert a date string to a Unix timestamp.
- **Required:** `date_string` (string) - Date string to convert
- **Optional:** `format` (string) - Date format pattern (default: "%Y-%m-%d %H:%M:%S")
- **Example:** `{"action": "date-to-unix", "date_string": "2026-03-10 12:00:00"}`

##### seconds-to-human
Convert seconds to a compact human-readable format (e.g., "1d 2h 30m 15s").
- **Required:** `seconds` (number) - Number of seconds
- **Example:** `{"action": "seconds-to-human", "seconds": 95415}`

#### Common Workflows

**Project deadline countdown:** Use `time-until` with the deadline date to show remaining time, then `business-days-between` to count working days left.

**Meeting scheduling across time zones:** Use `convert-timezone` to align meeting times, then `working-hours-overlap` to confirm both parties are within work hours.

**Date arithmetic for invoicing:** Use `add-days` to compute due dates (e.g., Net 30), or `subtract-days` to find a billing period start.

**Log timestamp conversion:** Use `unix-to-iso` or `unix-to-date` to convert raw timestamps into readable dates, or `date-to-unix` to convert back.

#### Important Notes
- Dates accept ISO 8601 format or most common parseable formats (e.g., "March 10, 2026", "2026-03-10", "10/03/2026").
- Timezone names use the IANA database (e.g., "America/New_York", "Europe/London", "Asia/Tokyo", "UTC").
- `business-days-between` counts weekdays only (Monday through Friday) and does not account for public holidays.
- `format-duration` produces verbose output ("2 days, 3 hours") while `seconds-to-human` produces compact output ("2d 3h").
- `parse-duration` supports flexible input: "2h 30m", "5 days 3 hours", "90s", etc.

## When To Use
- Use this skill for `Date and Time Calculator` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: date and time calculator, date calculator and timestamp tool set, building countdown timers for events or deadlines, calculating project durations in business days excluding weekends, scheduling meetings across multiple timezones, converting api timestamps to human readable formats, add days, date.
- Supported action names: `add-days`, `add-hours`, `add-minutes`, `business-days-between`, `convert-timezone`, `date-to-unix`, `days-between`, `format-duration`, `is-leap-year`, `parse-duration`, `quarter`, `seconds-to-human`, `subtract-days`, `subtract-hours`, `subtract-minutes`, `time-since`, `time-until`, `timezone-offset`, `unix-to-date`, `unix-to-iso`, `week-number`, `working-hours-overlap`.

## Use Cases
- Building countdown timers for events or deadlines
- calculating project durations in business days excluding weekends
- scheduling meetings across multiple timezones
- converting API timestamps to human-readable formats
- parsing user-entered durations like "2 hours 30 minutes" into seconds
- determining fiscal quarters for financial reporting
- validating date ranges for booking systems
- checking working hours overlap between distributed teams
- generating relative timestamps for activity feeds
- calculating age or tenure from start dates
- converting between Unix epoch and display formats for logs
- determining week numbers for sprint planning
- building time-tracking applications
- validating leap years for date calculations
- formatting elapsed time for dashboards and reports.

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `22`.
x402 availability: not enabled for this product.

- `add-days` (action slug: `add-days`): Add a number of days to a date. Returns the resulting date in ISO format. Price: `5` credits. Parameters: `date`, `days`.
- `add-hours` (action slug: `add-hours`): Add hours to a datetime. Returns the resulting datetime in ISO format. Price: `5` credits. Parameters: `date`, `hours`.
- `add-minutes` (action slug: `add-minutes`): Add minutes to a datetime. Returns the resulting datetime in ISO format. Price: `5` credits. Parameters: `date`, `minutes`.
- `business-days-between` (action slug: `business-days-between`): Calculate the number of business days (weekdays only, Mon-Fri) between two dates. Does not account for public holidays. Price: `5` credits. Parameters: `end_date`, `start_date`.
- `convert-timezone` (action slug: `convert-timezone`): Convert a datetime from one timezone to another. Uses IANA timezone names. Price: `5` credits. Parameters: `date_string`, `from_timezone`, `to_timezone`.
- `date-to-unix` (action slug: `date-to-unix`): Convert a date string to a Unix timestamp. Price: `5` credits. Parameters: `date_format`, `date_string`.
- `days-between` (action slug: `days-between`): Calculate the number of calendar days between two dates. Price: `5` credits. Parameters: `end_date`, `start_date`.
- `format-duration` (action slug: `format-duration`): Format a number of seconds into human-readable text (e.g., '2 days, 3 hours, 15 minutes'). Price: `5` credits. Parameters: `seconds`.
- `is-leap-year` (action slug: `is-leap-year`): Check whether a given year is a leap year. Price: `5` credits. Parameters: `year`.
- `parse-duration` (action slug: `parse-duration`): Parse a human-readable duration string into total seconds. Supports s/sec/seconds, m/min/minutes, h/hr/hours, d/day/days. Price: `5` credits. Parameters: `duration_str`.
- `quarter` (action slug: `quarter`): Get the fiscal quarter (1-4) for a date. Price: `5` credits. Parameters: `date`.
- `seconds-to-human` (action slug: `seconds-to-human`): Convert seconds to compact human-readable format (e.g., '1d 2h 30m 15s'). Price: `5` credits. Parameters: `seconds`.
- `subtract-days` (action slug: `subtract-days`): Subtract a number of days from a date. Returns the resulting date in ISO format. Price: `5` credits. Parameters: `date`, `days`.
- `subtract-hours` (action slug: `subtract-hours`): Subtract hours from a datetime. Returns the resulting datetime in ISO format. Price: `5` credits. Parameters: `date`, `hours`.
- `subtract-minutes` (action slug: `subtract-minutes`): Subtract minutes from a datetime. Returns the resulting datetime in ISO format. Price: `5` credits. Parameters: `date`, `minutes`.
- `time-since` (action slug: `time-since`): Calculate time elapsed since a past date. Returns days, hours, minutes, seconds. Price: `5` credits. Parameters: `past_date`.
- `time-until` (action slug: `time-until`): Calculate time remaining until a future date. Returns days, hours, minutes, seconds. Price: `5` credits. Parameters: `target_date`.
- `timezone-offset` (action slug: `timezone-offset`): Get the current UTC offset for a timezone. Price: `5` credits. Parameters: `timezone`.
- `unix-to-date` (action slug: `unix-to-date`): Convert a Unix timestamp to a formatted date string, optionally in a specific timezone. Price: `5` credits. Parameters: `timestamp`, `timezone`.
- `unix-to-iso` (action slug: `unix-to-iso`): Convert a Unix timestamp to ISO 8601 format. Price: `5` credits. Parameters: `timestamp`.
- `week-number` (action slug: `week-number`): Get the ISO week number (1-53) for a date. Price: `5` credits. Parameters: `date`.
- `working-hours-overlap` (action slug: `working-hours-overlap`): Check whether two time periods overlap. Useful for scheduling across time zones. Price: `5` credits. Parameters: `end1`, `end2`, `start1`, `start2`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "date-calculator-and-timestamp-tool-set"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "date-calculator-and-timestamp-tool-set"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "date-calculator-and-timestamp-tool-set"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "date-calculator-and-timestamp-tool-set"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "date-calculator-and-timestamp-tool-set"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "date-calculator-and-timestamp-tool-set"
  }
}
```

## Call This Tool
Product slug: `date-calculator-and-timestamp-tool-set`

Marketplace page: https://www.agentpmt.com/marketplace/date-calculator-and-timestamp-tool-set

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Date-and-Time-Calculator",
    "arguments": {
      "action": "add-days",
      "date": "example date",
      "days": 1
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "date-calculator-and-timestamp-tool-set",
  "parameters": {
    "action": "add-days",
    "date": "example date",
    "days": 1
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `add-days` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/date-calculator-and-timestamp-tool-set
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
