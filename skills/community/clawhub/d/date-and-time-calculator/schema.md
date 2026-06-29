# Date and Time Calculator Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `date-calculator-and-timestamp-tool-set`

x402 availability: not enabled for this product.

## `add-days`

Action slug: `add-days`

Price: `5` credits

Add a number of days to a date. Returns the resulting date in ISO format.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date` | `string` | yes | Starting date in ISO or parseable format. |
| `days` | `integer` | yes | Number of days to add. |

Sample parameters:

```json
{
  "date": "example date",
  "days": 1
}
```

Generated JSON parameter schema:

```json
{
  "date": {
    "description": "Starting date in ISO or parseable format.",
    "required": true,
    "type": "string"
  },
  "days": {
    "description": "Number of days to add.",
    "required": true,
    "type": "integer"
  }
}
```

## `add-hours`

Action slug: `add-hours`

Price: `5` credits

Add hours to a datetime. Returns the resulting datetime in ISO format.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date` | `string` | yes | Starting datetime in ISO or parseable format. |
| `hours` | `number` | yes | Number of hours to add (supports decimals, e.g., 5.5). |

Sample parameters:

```json
{
  "date": "example date",
  "hours": 1
}
```

Generated JSON parameter schema:

```json
{
  "date": {
    "description": "Starting datetime in ISO or parseable format.",
    "required": true,
    "type": "string"
  },
  "hours": {
    "description": "Number of hours to add (supports decimals, e.g., 5.5).",
    "required": true,
    "type": "number"
  }
}
```

## `add-minutes`

Action slug: `add-minutes`

Price: `5` credits

Add minutes to a datetime. Returns the resulting datetime in ISO format.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date` | `string` | yes | Starting datetime in ISO or parseable format. |
| `minutes` | `number` | yes | Number of minutes to add. |

Sample parameters:

```json
{
  "date": "example date",
  "minutes": 1
}
```

Generated JSON parameter schema:

```json
{
  "date": {
    "description": "Starting datetime in ISO or parseable format.",
    "required": true,
    "type": "string"
  },
  "minutes": {
    "description": "Number of minutes to add.",
    "required": true,
    "type": "number"
  }
}
```

## `business-days-between`

Action slug: `business-days-between`

Price: `5` credits

Calculate the number of business days (weekdays only, Mon-Fri) between two dates. Does not account for public holidays.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `end_date` | `string` | yes | End date in ISO or parseable format. |
| `start_date` | `string` | yes | Start date in ISO or parseable format. |

Sample parameters:

```json
{
  "end_date": "example end date",
  "start_date": "example start date"
}
```

Generated JSON parameter schema:

```json
{
  "end_date": {
    "description": "End date in ISO or parseable format.",
    "required": true,
    "type": "string"
  },
  "start_date": {
    "description": "Start date in ISO or parseable format.",
    "required": true,
    "type": "string"
  }
}
```

## `convert-timezone`

Action slug: `convert-timezone`

Price: `5` credits

Convert a datetime from one timezone to another. Uses IANA timezone names.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date_string` | `string` | yes | Datetime string to convert. |
| `from_timezone` | `string` | yes | Source timezone (e.g., 'America/New_York'). |
| `to_timezone` | `string` | yes | Target timezone (e.g., 'Europe/London'). |

Sample parameters:

```json
{
  "date_string": "example date string",
  "from_timezone": "example from timezone",
  "to_timezone": "example to timezone"
}
```

Generated JSON parameter schema:

```json
{
  "date_string": {
    "description": "Datetime string to convert.",
    "required": true,
    "type": "string"
  },
  "from_timezone": {
    "description": "Source timezone (e.g., 'America/New_York').",
    "required": true,
    "type": "string"
  },
  "to_timezone": {
    "description": "Target timezone (e.g., 'Europe/London').",
    "required": true,
    "type": "string"
  }
}
```

## `date-to-unix`

Action slug: `date-to-unix`

Price: `5` credits

Convert a date string to a Unix timestamp.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date_format` | `string` | no | Python strftime format string for parsing (default: '%Y-%m-%d %H:%M:%S'). If omitted, common formats are tried automatically. |
| `date_string` | `string` | yes | Date string to convert. |

Sample parameters:

```json
{
  "date_format": "%Y-%m-%d %H:%M:%S",
  "date_string": "example date string"
}
```

Generated JSON parameter schema:

```json
{
  "date_format": {
    "default": "%Y-%m-%d %H:%M:%S",
    "description": "Python strftime format string for parsing (default: '%Y-%m-%d %H:%M:%S'). If omitted, common formats are tried automatically.",
    "required": false,
    "type": "string"
  },
  "date_string": {
    "description": "Date string to convert.",
    "required": true,
    "type": "string"
  }
}
```

## `days-between`

Action slug: `days-between`

Price: `5` credits

Calculate the number of calendar days between two dates.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `end_date` | `string` | yes | End date in ISO or parseable format. |
| `start_date` | `string` | yes | Start date in ISO or parseable format. |

Sample parameters:

```json
{
  "end_date": "example end date",
  "start_date": "example start date"
}
```

Generated JSON parameter schema:

```json
{
  "end_date": {
    "description": "End date in ISO or parseable format.",
    "required": true,
    "type": "string"
  },
  "start_date": {
    "description": "Start date in ISO or parseable format.",
    "required": true,
    "type": "string"
  }
}
```

## `format-duration`

Action slug: `format-duration`

Price: `5` credits

Format a number of seconds into human-readable text (e.g., '2 days, 3 hours, 15 minutes').

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `seconds` | `number` | yes | Duration in seconds to format. |

Sample parameters:

```json
{
  "seconds": 1
}
```

Generated JSON parameter schema:

```json
{
  "seconds": {
    "description": "Duration in seconds to format.",
    "required": true,
    "type": "number"
  }
}
```

## `is-leap-year`

Action slug: `is-leap-year`

Price: `5` credits

Check whether a given year is a leap year.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `year` | `integer` | yes | Year to check. |

Sample parameters:

```json
{
  "year": 1
}
```

Generated JSON parameter schema:

```json
{
  "year": {
    "description": "Year to check.",
    "minimum": 1,
    "required": true,
    "type": "integer"
  }
}
```

## `parse-duration`

Action slug: `parse-duration`

Price: `5` credits

Parse a human-readable duration string into total seconds. Supports s/sec/seconds, m/min/minutes, h/hr/hours, d/day/days.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `duration_str` | `string` | yes | Duration text to parse (e.g., '2h 30m 15s', '5 days 3 hours'). |

Sample parameters:

```json
{
  "duration_str": "example duration str"
}
```

Generated JSON parameter schema:

```json
{
  "duration_str": {
    "description": "Duration text to parse (e.g., '2h 30m 15s', '5 days 3 hours').",
    "required": true,
    "type": "string"
  }
}
```

## `quarter`

Action slug: `quarter`

Price: `5` credits

Get the fiscal quarter (1-4) for a date.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date` | `string` | yes | Date to check in ISO or parseable format. |

Sample parameters:

```json
{
  "date": "example date"
}
```

Generated JSON parameter schema:

```json
{
  "date": {
    "description": "Date to check in ISO or parseable format.",
    "required": true,
    "type": "string"
  }
}
```

## `seconds-to-human`

Action slug: `seconds-to-human`

Price: `5` credits

Convert seconds to compact human-readable format (e.g., '1d 2h 30m 15s').

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `seconds` | `number` | yes | Number of seconds to convert. |

Sample parameters:

```json
{
  "seconds": 1
}
```

Generated JSON parameter schema:

```json
{
  "seconds": {
    "description": "Number of seconds to convert.",
    "required": true,
    "type": "number"
  }
}
```

## `subtract-days`

Action slug: `subtract-days`

Price: `5` credits

Subtract a number of days from a date. Returns the resulting date in ISO format.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date` | `string` | yes | Starting date in ISO or parseable format. |
| `days` | `integer` | yes | Number of days to subtract. |

Sample parameters:

```json
{
  "date": "example date",
  "days": 1
}
```

Generated JSON parameter schema:

```json
{
  "date": {
    "description": "Starting date in ISO or parseable format.",
    "required": true,
    "type": "string"
  },
  "days": {
    "description": "Number of days to subtract.",
    "required": true,
    "type": "integer"
  }
}
```

## `subtract-hours`

Action slug: `subtract-hours`

Price: `5` credits

Subtract hours from a datetime. Returns the resulting datetime in ISO format.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date` | `string` | yes | Starting datetime in ISO or parseable format. |
| `hours` | `number` | yes | Number of hours to subtract. |

Sample parameters:

```json
{
  "date": "example date",
  "hours": 1
}
```

Generated JSON parameter schema:

```json
{
  "date": {
    "description": "Starting datetime in ISO or parseable format.",
    "required": true,
    "type": "string"
  },
  "hours": {
    "description": "Number of hours to subtract.",
    "required": true,
    "type": "number"
  }
}
```

## `subtract-minutes`

Action slug: `subtract-minutes`

Price: `5` credits

Subtract minutes from a datetime. Returns the resulting datetime in ISO format.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date` | `string` | yes | Starting datetime in ISO or parseable format. |
| `minutes` | `number` | yes | Number of minutes to subtract. |

Sample parameters:

```json
{
  "date": "example date",
  "minutes": 1
}
```

Generated JSON parameter schema:

```json
{
  "date": {
    "description": "Starting datetime in ISO or parseable format.",
    "required": true,
    "type": "string"
  },
  "minutes": {
    "description": "Number of minutes to subtract.",
    "required": true,
    "type": "number"
  }
}
```

## `time-since`

Action slug: `time-since`

Price: `5` credits

Calculate time elapsed since a past date. Returns days, hours, minutes, seconds.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `past_date` | `string` | yes | Past date in ISO format or any parseable format. |

Sample parameters:

```json
{
  "past_date": "example past date"
}
```

Generated JSON parameter schema:

```json
{
  "past_date": {
    "description": "Past date in ISO format or any parseable format.",
    "required": true,
    "type": "string"
  }
}
```

## `time-until`

Action slug: `time-until`

Price: `5` credits

Calculate time remaining until a future date. Returns days, hours, minutes, seconds.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `target_date` | `string` | yes | Target date in ISO format or any parseable format (e.g., '2026-12-31T23:59:59', 'December 31, 2026'). |

Sample parameters:

```json
{
  "target_date": "example target date"
}
```

Generated JSON parameter schema:

```json
{
  "target_date": {
    "description": "Target date in ISO format or any parseable format (e.g., '2026-12-31T23:59:59', 'December 31, 2026').",
    "required": true,
    "type": "string"
  }
}
```

## `timezone-offset`

Action slug: `timezone-offset`

Price: `5` credits

Get the current UTC offset for a timezone.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `timezone` | `string` | yes | Timezone name (e.g., 'America/New_York', 'UTC', 'Europe/London'). |

Sample parameters:

```json
{
  "timezone": "example timezone"
}
```

Generated JSON parameter schema:

```json
{
  "timezone": {
    "description": "Timezone name (e.g., 'America/New_York', 'UTC', 'Europe/London').",
    "required": true,
    "type": "string"
  }
}
```

## `unix-to-date`

Action slug: `unix-to-date`

Price: `5` credits

Convert a Unix timestamp to a formatted date string, optionally in a specific timezone.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `timestamp` | `number` | yes | Unix timestamp in seconds since epoch. |
| `timezone` | `string` | no | Timezone name (defaults to local time). Example: 'America/Chicago'. |

Sample parameters:

```json
{
  "timestamp": 1,
  "timezone": "example timezone"
}
```

Generated JSON parameter schema:

```json
{
  "timestamp": {
    "description": "Unix timestamp in seconds since epoch.",
    "required": true,
    "type": "number"
  },
  "timezone": {
    "description": "Timezone name (defaults to local time). Example: 'America/Chicago'.",
    "required": false,
    "type": "string"
  }
}
```

## `unix-to-iso`

Action slug: `unix-to-iso`

Price: `5` credits

Convert a Unix timestamp to ISO 8601 format.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `timestamp` | `number` | yes | Unix timestamp in seconds since epoch. |

Sample parameters:

```json
{
  "timestamp": 1
}
```

Generated JSON parameter schema:

```json
{
  "timestamp": {
    "description": "Unix timestamp in seconds since epoch.",
    "required": true,
    "type": "number"
  }
}
```

## `week-number`

Action slug: `week-number`

Price: `5` credits

Get the ISO week number (1-53) for a date.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `date` | `string` | yes | Date to check in ISO or parseable format. |

Sample parameters:

```json
{
  "date": "example date"
}
```

Generated JSON parameter schema:

```json
{
  "date": {
    "description": "Date to check in ISO or parseable format.",
    "required": true,
    "type": "string"
  }
}
```

## `working-hours-overlap`

Action slug: `working-hours-overlap`

Price: `5` credits

Check whether two time periods overlap. Useful for scheduling across time zones.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `end1` | `string` | yes | End time of first period in HH:MM format (e.g., '17:00'). |
| `end2` | `string` | yes | End time of second period in HH:MM format (e.g., '22:00'). |
| `start1` | `string` | yes | Start time of first period in HH:MM format (e.g., '09:00'). |
| `start2` | `string` | yes | Start time of second period in HH:MM format (e.g., '14:00'). |

Sample parameters:

```json
{
  "end1": "example end1",
  "end2": "example end2",
  "start1": "example start1",
  "start2": "example start2"
}
```

Generated JSON parameter schema:

```json
{
  "end1": {
    "description": "End time of first period in HH:MM format (e.g., '17:00').",
    "required": true,
    "type": "string"
  },
  "end2": {
    "description": "End time of second period in HH:MM format (e.g., '22:00').",
    "required": true,
    "type": "string"
  },
  "start1": {
    "description": "Start time of first period in HH:MM format (e.g., '09:00').",
    "required": true,
    "type": "string"
  },
  "start2": {
    "description": "Start time of second period in HH:MM format (e.g., '14:00').",
    "required": true,
    "type": "string"
  }
}
```
