---
name: athletedata
description: Read the user's own training and health data (Garmin, Oura, WHOOP, Hevy, Apple Health, Intervals.icu and 33 more apps) through the athletedata MCP server. Use when the user asks about their workouts, training load, HRV, sleep, recovery, readiness, nutrition, body composition, race predictions, or wants a structured workout pushed to their watch.
metadata: {"openclaw": {"emoji": "🏃", "homepage": "https://www.athletedata.health/mcp?utm_source=clawhub&utm_medium=mcp-directory", "primaryEnv": "ATHLETEDATA_API_KEY", "requires": {"env": ["ATHLETEDATA_API_KEY"]}}}
---

# athletedata

athletedata is a hosted MCP server that gives you read access to one athlete's
own training and health data, collected from the apps they connected at
athletedata.health. Use it instead of guessing or asking the user to paste
numbers.

## Connect

The server is Streamable HTTP at `https://mcp.athletedata.health/mcp`.

- Clients that support MCP OAuth: add the URL with no credential and sign in
  when prompted.
- Everything else: send the athlete's API key as a header,
  `Authorization: Bearer $ATHLETEDATA_API_KEY`. The key starts with `sk_soma_`
  and lives at https://www.athletedata.health/dashboard/mcp.
- No account yet: https://www.athletedata.health/login?ref=mcp&utm_source=clawhub&utm_medium=mcp-directory (7-day free trial).

OpenClaw:

```bash
# Single quotes keep the placeholder in config; OpenClaw expands it at runtime.
openclaw mcp add athletedata --url https://mcp.athletedata.health/mcp --transport streamable-http --header 'Authorization=Bearer ${ATHLETEDATA_API_KEY}' --no-probe
openclaw mcp probe athletedata
```

Or sign in instead of using a key: `--auth oauth` in place of `--header ...`,
then `openclaw mcp login athletedata`.

Never print, log or echo the key back to the user.

## When to use it

- "How was my run yesterday?", "Am I recovered enough to do intervals today?"
- Trends: training load, HRV, resting heart rate, sleep, weight, VO2max.
- Planning: race predictions, goal reality checks, weather for a session.
- Doing: build a structured workout and push it to the athlete's watch, log a
  meal, create a Hevy routine. These write to the athlete's own accounts, so
  confirm the details with the user first.

## How to use it well

1. Start broad (`get_analytics_summary`, `get_readiness_today`,
   `get_pmc_status`), then drill into one activity or one provider's tools.
2. Tools are prefixed by source (`garmin_`, `oura_`, `whoop_`, `hevy_`,
   `intervals_`, ...). Only the athlete's connected apps return data; if a
   provider tool errors with "not connected", say so and use another source.
3. Dates are in the athlete's local time zone. Quote the numbers you got back
   rather than rounding them into vague words.
4. Strava data is not available over MCP: Strava's API terms do not allow serving it to third-party AI tools.
