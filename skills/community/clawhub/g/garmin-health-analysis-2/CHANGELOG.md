# Changelog

## v1.6.1 (2026-10-17)

### Listing: distinguish the fork from upstream in the name and summary

ClawHub builds the listing header from the skill's frontmatter, not its body:
`--name` sets the display name, and the `description:` field becomes the
summary. Both were byte-identical to upstream `eversonl/garmin-health-analysis`
(stuck at 1.2.2), so the only thing telling the two listings apart was the
version number.

- Display name is now **Garmin Health Analysis (Maintained Fork)**.
- The summary now leads with what this fork adds over 1.2.2: the Garmin
  calendar, confirmation-gated Jet Lag trips, and the extended metric tables.

No code change. Also fixed an em dash in the README quote line.

## v1.6.0 (2026-10-17)

### Security: confirmation gate on destructive trip operations

ClawHub's security audit flagged `trip-delete` (Medium): it checked only that
`--trip-id` was non-empty and then deleted, with no confirmation gate. Correct
finding, and it also under-reported: `trip-update` is a full **replace**, so an
incomplete flight list silently drops legs.

Both are now **read-only by default**:

- `trip-delete` resolves the target, reports exactly what would be removed, and
  exits **2** having changed nothing. Deleting requires `--confirm-delete`.
- `trip-update` shows the current trip beside the payload that would replace it,
  and exits **2**. Applying requires `--confirm-update`.
- A missing or unknown trip id is an error (exit 1), not a silent no-op.
- `trip-add` is not gated: it creates a new trip rather than destroying one.

Exit **2** is deliberate, so no caller can mistake "here is what would happen"
for "it happened". SKILL.md and README document the gate and the
preview-then-confirm rule for agents.

## v1.5.3 (2026-10-17)

### Docs: SKILL.md now carries the README's content

ClawHub renders SKILL.md, so it is the skill page. It lacked everything the
README gained: fork context, the feature-diff table, and the scripts tree.
Anyone landing on the listing saw no sign of the calendar, the trip API or the
fork at all.

- Added "What's Different Here" (feature diff vs the original) and "What's
  Included" (scripts tree, now listing `garmin_calendar.py`)
- Fork note with the upstream link and why the fork exists
- `author:` -> `EversonL, bolinches`; Version Info credits both, and links the
  fork repo
- Install metadata pins `garminconnect>=0.3.18`
- Troubleshooting names the trip-API floor instead of a bare upgrade line

## v1.5.2 (2026-10-17)

### Docs: drop Clawdbot-era setup text

The setup section still said "Clawdbot", pointed at `~/.clawdbot/clawdbot.json`
and `~/.clawdbot/skills/`, and described "two different setups" in Clawdbot terms.
That text renders as the skill page, so the listing read as an old clone. Now
OpenClaw throughout, with the current config path and workspace layout.

## v1.5.0 (2026-10-17)

### ✈️ Jet Lag Adviser trips: read AND write

**NEW: trips can now be created, replaced and deleted from the CLI.** Trips have
their own API ([`garminconnect`](https://github.com/cyberjunky/python-garminconnect)
>= 0.3.18), separate from the calendar, and it is writable.

- Added `trip-list` / `trip-add` / `trip-update` / `trip-delete` subcommands to
  `garmin_calendar.py`.
- Endpoints: `GET|POST|PUT /jetlag-service/jetlag/trip`, `DELETE
  /jetlag-service/jetlag/trip/{id}`, `GET /jetlag-service/jetlag/status/daily/{date}`.
- **Live-tested end to end** on a real account: create → read-back → replace →
  delete, each verified against `trip-list` and cleaned up afterwards.
- Flight fields (all six required, one entry per leg, so a connection is two):
  `originLocation`, `originTimezone`, `originTimestamp`, `destinationLocation`,
  `destinationTimezone`, `destinationTimestamp`. Garmin does not geocode; give
  free-text locations and the UTC offset for that date. Timestamps are local time
  with no offset.
- **Gotcha found live:** a timestamp without a fractional second
  (`...T15:45:00`) is rejected with `HTTP 500`. With `...T15:45:00.0` it
  succeeds. The script normalises this, so either form may be passed.
- A trip overlapping an existing one is refused: `HTTP 400 "A trip already
  exists for this date range"`.
- Trips are auto-deleted by Garmin once they end and the user has re-adjusted to
  home time. So `trip-list` holds only current/recent trips; older travel survives
  as `jetLagTrip` day markers in the calendar. Both sources are kept for that
  reason.
- `install.sh` now pins `garminconnect>=0.3.18` (0.3.18 also dropped `garth`).

## v1.4.0 (2026-10-17)

### 📅 Calendar: Trips, Races, Events

**NEW: read the Garmin Connect calendar via `scripts/garmin_calendar.py`.**

The Garmin calendar-service carries more than workouts. Trips and races added in
the Garmin app land there, and trips are `itemType="jetLagTrip"`, one item **per
calendar day** of the trip.

- Added `garmin_calendar.py` with subcommands:
  - `calendar` — every item in the window
  - `trips` — trip days, grouped into windows. **The only source for FUTURE trips**:
    `get_stats().isJetLagDay` reports only days that have already happened, so the
    calendar is what makes pre-trip advice possible. `--with-names` labels past
    days from `get_stats().jetLagTripName` (one call per past day; names are not
    published for future days).
  - `races` / `events` — races and booked events, **with title and URL**
  - `nap` — recorded naps
  - `summary` — counts by item type, plus future trip days
- Item types observed: `activity`, `jetLagTrip`, `nap`, `userTimeChanged`
  (timezone change — the flight-day tell), `weight`, `event`, `wellnessActivity`,
  `bloodpressure`.
- Endpoint: `GET /calendar-service/year/{year}/month/{month-1}` (0-indexed month)
  via `get_scheduled_workouts(year, month)`.
- Dedupes items that calendar-service re-yields across adjacent month boundaries
  (events near a month edge arrived two or more times before this).
- Month-level errors are reported in `errors` rather than aborting the window,
  because calendar-service has a history floor (nothing before ~2024-12).

**Usage examples:**
```bash
# Upcoming and past trips, grouped into windows
python3 scripts/garmin_calendar.py trips --months-back 14 --months-fwd 6

# Label past trip days with their Garmin trip name
python3 scripts/garmin_calendar.py trips --months-back 2 --with-names

# Races and events
python3 scripts/garmin_calendar.py races --months-back 24

# Quick overview
python3 scripts/garmin_calendar.py summary --months-back 14 --months-fwd 4
```

## v1.3.0 (2026-06-02)

### 🏃 Activity Detail & Splits - Per-Second and Per-Lap Data

**NEW: Query individual activity details with per-second time-series and per-lap splits!**

- Added `activity_splits` subcommand to `garmin_data.py` — get per-lap HR, speed, distance, power, cadence, elevation for any activity
- Added `activity_detail` subcommand to `garmin_data.py` — get per-second time-series data with all metrics (HR, speed, distance, elevation, power, cadence, GPS coordinates, and more)
  - `--metrics` flag to select specific metrics (e.g., `directHeartRate,directSpeed,sumDistance`)
  - `--sample-interval` flag to downsample output (e.g., `--sample-interval 30` for every 30 seconds)
- Added `activity_id` field to `activities` output — makes it easy to query specific activity details
- Updated SKILL.md with new command documentation and question examples
- 20+ available per-second metrics including: heart rate, speed, distance, elevation, power, cadence, GPS, grade-adjusted speed, vertical oscillation, ground contact time, stride length, vertical ratio, performance condition

**Usage examples:**
```bash
# Get lap splits for a run
python3 scripts/garmin_data.py activity_splits --activity-id 600107330

# Get per-second HR and speed (sampled every 30s)
python3 scripts/garmin_data.py activity_detail --activity-id 600107330 \
  --metrics directHeartRate,directSpeed,sumDistance --sample-interval 30

# Get all metrics at full resolution
python3 scripts/garmin_data.py activity_detail --activity-id 600107330
```

## v1.2.2 (2026-01-26)

### 🧹 Repository Cleanup & Focus

**Removed old MCP server files** - Now using dedicated MCP server repo for Claude Desktop users:
- Removed `CLAUDE_DESKTOP.md` (old MCP setup docs)
- Removed `mcp_server.py` (old Python MCP server - 750+ lines)
- Removed `requirements.txt` (old MCP dependencies)

**Updated documentation for clarity:**
- README.md now clearly identifies this as the Clawdbot skill
- Added prominent callout directing Claude Desktop users to the dedicated MCP server repo
- Simplified `references/mcp_setup.md` to redirect to https://github.com/eversonl/garmin-health-mcp-server
- Updated file tree to reflect current structure

**New dedicated MCP server** for Claude Desktop users:
- Purpose-built Node.js MCP server at https://github.com/eversonl/garmin-health-mcp-server
- Uses modern @modelcontextprotocol/sdk
- Easy `npm install` + `npm run auth` setup
- Comprehensive installation guide and troubleshooting

**Both can coexist** - Shared authentication allows users to install both the Clawdbot skill and MCP server simultaneously.

**This repo is now focused exclusively on the Clawdbot skill** for automated health monitoring, scheduled reports, and proactive check-ins.

## v1.2.0 (2026-01-26)

### 🚀 Major Feature: MCP Server for Claude Desktop & Code

**NEW: Works with Claude Desktop, Claude Code, and any MCP client!**

- Added `mcp_server.py` - full MCP (Model Context Protocol) server implementation
- Exposes all Garmin tools to Claude Desktop, Claude Code, and other MCP-compatible clients
- New installation guide: `CLAUDE_DESKTOP.md` with step-by-step setup
- 14 MCP tools available:
  - Health metrics (sleep, Body Battery, HRV, activities, heart rate)
  - Time-based queries (HR/stress/BB at specific times)
  - Extended metrics (training readiness, body composition, SPO2)
  - Activity file downloads and analysis
- Updated README with Claude Desktop quick start
- Added `mcp` to requirements.txt

**Now you can use this skill with:**
- ✅ Clawdbot (original)
- ✅ Claude Desktop (new!)
- ✅ Claude Code / VS Code extension (new!)
- ✅ Any MCP-compatible client (new!)

## v1.1.5 (2026-01-25)

### Metadata
- Expanded ClawdHub description with conversational examples and "talk to your data" messaging
- Showcases real use cases: "what was my fastest speed?", activity analysis, recovery tracking

## v1.1.3 (2026-01-25)

### Documentation
- Updated Version Info section in SKILL.md with correct author and all dependencies

## v1.1.2 (2026-01-25)

### Metadata
- Updated description to highlight v1.1+ features (time queries, 20+ metrics, FIT/GPX analysis)
- Changed author to "EversonL & Claude"

## v1.1.1 (2026-01-25)

### Documentation
- Updated metadata with new dependencies (fitparse, gpxpy)

## v1.1.0 (2026-01-25)

### 🚀 Major Features

**Time-Based Queries**
- New `garmin_query.py` script for time-based questions
- Ask "what was my heart rate at 3pm?" and get instant answers
- Supports heart rate, stress, Body Battery, steps
- Flexible time parsing (12/24 hour formats)

**Extended Metrics** (`garmin_data_extended.py`)
- Training readiness & training status
- Body composition (weight, body fat %, muscle mass, BMI)
- Weight tracking over time
- SPO2 (blood oxygen saturation)
- Detailed respiration data
- Intraday steps, floors climbed
- Intensity minutes (vigorous/moderate activity)
- Hydration tracking
- Time-series stress data
- Max metrics (VO2 max, fitness age, endurance/hill scores)
- Intraday heart rate (all samples)

**Activity File Analysis** (`garmin_activity_files.py`)
- Download FIT/GPX/TCX files from activities
- Parse FIT files for GPS, elevation, HR, cadence, power
- Parse GPX files for route visualization
- Query data at specific distances ("what was my elevation at mile 2?")
- Query data at specific times during activities
- Comprehensive activity analysis & statistics
- Support for advanced use cases (route mapping, pace analysis, elevation profiles)

**Documentation**
- New `references/extended_capabilities.md` with comprehensive usage examples
- Updated dependencies (fitparse, gpxpy)

## v1.0.1 (2026-01-25)

### Bug Fixes
- Fixed sleep data extraction - properly parse nested `dailySleepDTO` object from Garmin API
- Sleep time and scores now display correctly in all charts and dashboards

## v1.0.0 (2026-01-25)

### Initial Release

**Features:**
- Fetch health data from Garmin Connect (sleep, Body Battery, HRV, heart rate, activities, stress)
- Generate interactive HTML charts with Chart.js
- Science-backed health analysis framework
- Support for multiple credential configuration methods
- Automatic token refresh

**Data Available:**
- Sleep: duration, stages (deep/light/REM), scores, HRV during sleep
- Body Battery: Garmin's recovery metric (0-100)
- HRV: nightly heart rate variability with baseline tracking
- Heart Rate: resting, max, min throughout the day
- Activities: workouts with calories, duration, heart rate, GPS data
- Stress: all-day stress levels based on HRV analysis

**Charts:**
- Sleep analysis (hours + scores)
- Body Battery recovery (color-coded by level)
- HRV & Resting Heart Rate trends
- Activities summary (by type with calories)
- Full dashboard combining all metrics

**Configuration:**
- UI-configurable via Clawdbot config (`skills.entries.garmin-health-analysis.env`)
- Local config.json support
- Command-line arguments
- Environment variables

**Requirements:**
- Python 3.7+
- garminconnect library (installed via pip)
- Garmin Connect account with wearable device

**Security:**
- Session tokens stored locally in `~/.clawdbot/garmin/`
- Tokens auto-refresh
- No data sent anywhere except Garmin's official servers
