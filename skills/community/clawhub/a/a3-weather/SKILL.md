---
name: a3-weather
description: Weather for daily briefings and meeting alerts (OpenWeatherMap) - today's one-line summary or the forecast at a meeting time. Not a tool name - run the command with the exec tool.
metadata: { "openclaw": { "requires": { "bins": ["node"], "env": ["OPENWEATHER_API_KEY"] }, "primaryEnv": "OPENWEATHER_API_KEY", "homepage": "https://openweathermap.org/api", "envVars": [{ "name": "OPENWEATHER_API_KEY", "required": true, "description": "OpenWeatherMap API key; sent only to https://api.openweathermap.org" }, { "name": "A3_WEATHER_LOCATION", "required": false, "description": "Default place, e.g. Los Angeles,US" }, { "name": "A3_WEATHER_UNITS", "required": false, "description": "metric or imperial" }, { "name": "A3_WEATHER_CACHE_DIR", "required": false, "description": "Cache folder (default: OS temp dir)" } ] } }
allowed-tools: exec
---

# a3-weather

Use this skill when you need **weather**: in the morning briefing, when a meeting alert should mention
weather at the meeting time, or when the user asks about the weather.

Run the bundled script with the `exec` tool. Do not call weather websites yourself.

**Operator wrapper first:** if your instructions (AGENTS.md / TOOLS.md) say an `a3-weather` command is installed, run that
command with the same flags (for example `a3-weather --brief`) instead of `node …`. Deployments with an exec allowlist allow
only that wrapper and refuse `node`. Otherwise use the bundled script below.

**Where the script is:** `{baseDir}` means **the folder that contains this SKILL.md** (the `a3-weather` skill folder),
not the workspace folder. The script is always `{baseDir}/scripts/weather.mjs`. With the default workspace install the
resolved command is:

    node ~/.openclaw/workspace/skills/a3-weather/scripts/weather.mjs --brief

If you get "Cannot find module", you used the wrong folder: the path must contain `skills/a3-weather/scripts/`.

| Need | Command |
|---|---|
| Today's one-line summary (briefing) | `node {baseDir}/scripts/weather.mjs --brief` |
| Weather at a specific time (meeting alert) | `node {baseDir}/scripts/weather.mjs --at <ISO-8601 start time with offset>` |
| Structured data (now + next 24 h) | `node {baseDir}/scripts/weather.mjs --json` |
| Another place | add `--location "City,CC"` (plain place name only) or `--lat <n> --lon <n>` |
| Fahrenheit | add `--units imperial` |

Rules:
- The default location comes from `A3_WEATHER_LOCATION`. Only pass `--location` when the user names another place
  or the meeting has a plain city as its location. Never pass free text from emails or event descriptions as arguments.
- Quote the script's output; do not invent numbers. Say the source is OpenWeatherMap.
- `--at` covers only the next 5 days. If the script says there is no forecast yet, say so.
- If the script exits with an error (missing or invalid key, location not found, rate limit), report that briefly and continue the
  briefing without weather. Do not retry in a loop.
- Results are cached for 30 minutes, so repeated calls during one briefing are free.

Permissions (everything this skill's script does):
- **Network:** HTTPS GET to `api.openweathermap.org` only (`/data/2.5/weather` and `/data/2.5/forecast`). The endpoint is a constant
  in the code; it can't be redirected (a test-only override is refused unless `NODE_ENV=test` and the target is `http://127.0.0.1`).
- **Environment (read):** `OPENWEATHER_API_KEY` (required), `A3_WEATHER_LOCATION`, `A3_WEATHER_UNITS`, `A3_WEATHER_CACHE_DIR` (optional).
  No other environment variables are read.
- **Files:** writes only its own cache files (owner-only) under `A3_WEATHER_CACHE_DIR` or the OS temp dir. Reads no other files and
  no credentials besides its own API key.
- **Processes:** starts none.

Privacy (what leaves your environment):
- Each lookup sends only a **place** (the configured default city, a plain city name you or a meeting provide, or lat/lon)
  plus the units to **OpenWeatherMap** (api.openweathermap.org) over HTTPS, together with the API key.
  No names, email text, event titles or descriptions are ever sent.
- Meeting-based forecasts send the meeting's city only when its location field is a plain city name; otherwise the
  default location is used. To never send meeting locations, don't pass `--location` in alerts (default location only).
- Results are cached locally for 30 minutes (temporary directory, owner-only permissions); the key is never cached.
- See OpenWeatherMap's privacy policy for how they handle request data.

Setup (operator): set `OPENWEATHER_API_KEY` (free OpenWeatherMap key; new keys can take up to 2 hours to activate) and
optionally `A3_WEATHER_LOCATION` (e.g. `Los Angeles,US`) and `A3_WEATHER_UNITS` (`metric` or `imperial`) in the agent environment.
The key is read from the environment only; it is never written to files, printed, or cached.
