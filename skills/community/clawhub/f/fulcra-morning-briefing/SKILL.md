---
name: fulcra-morning-briefing
description: Compose a personalized morning briefing using the latest fulcra-context skill for sleep, biometrics, calendar, activity, and weather context. Adapts tone and detail to how the human actually slept.
homepage: https://fulcradynamics.com
---

# 🌅 Fulcra Morning Briefing

Deliver a personalized morning briefing calibrated to how the human actually slept. Bad night? Keep it short and gentle. Great sleep? Go deep on the day ahead.

This is the lightweight morning workflow on top of **[fulcra-context](../fulcra-context/SKILL.md)**. Fulcra gives agents and their humans scoped, secure access to read and write real-world context and shared human/agent memory: attention, events, location, calendar, health, wearables, and other streams.

## What You'll Compose

A morning briefing that includes:
- **Sleep summary** — hours, quality, deep/REM breakdown
- **Body check** — resting heart rate, HRV (recovery signal)
- **Today's schedule** — calendar events with timing
- **Weather** — current conditions for the user's location
- **Energy-calibrated tone** — the briefing adapts to sleep quality

## Setup

### 1. The User Needs a Fulcra Account

Fulcra requires an authenticated account, not an API key. Accounts can be created through the CLI auth flow and include 5 GB of storage free forever.

Users who want biometrics, location, calendar, and other phone-collected context can install the [Context iOS app](https://apps.apple.com/app/id1633037434) and sign in with the same account. The app uses the same free storage and is no longer subscription gated. Android is coming soon.

### 2. Install CLI Prerequisites

```bash
uv --version
jq --version
```

### 3. Authenticate via the Fulcra CLI

Run this once interactively. The user opens the returned URL, confirms the code, and approves access:

```bash
uv tool run fulcra-api auth login
```

For remote agents, do not rely on the agent host's local browser. Keep the CLI running, surface the printed device authorization URL and code to the intended user in chat through the active trusted user channel, and wait for approval. The user can approve from any browser on any device. Never send access tokens or credential files.

Credentials persist to `~/.config/fulcra/credentials.json`; the CLI refreshes access tokens as needed.

## How to Collect Data

### Preferred: Run the Collector

```bash
python3 skills/fulcra-morning-briefing/collect_briefing_data.py --location "New+York"
```

The collector loads `fulcra-context/scripts/fulcra_data_service.py` from an installed sibling skill, or from `FULCRA_CONTEXT_SCRIPTS` when set.

### Loading the Shared Service

```python
from datetime import datetime, timezone, timedelta
from fulcra_data_service import get_service

api = get_service()  # CLI-first, legacy SDK fallback
```

### Sleep Data (Last Night)

```python
now = datetime.now(timezone.utc)
start = (now - timedelta(hours=14)).isoformat()
end = now.isoformat()

samples = api.get_metric_samples(start, end, "SleepStage")
```

Sleep stage values: `0=InBed, 1=Awake, 2=Core/Light, 3=Deep, 4=REM`

**Quality heuristic:**
- **Excellent:** ≥7h sleep, ≥15% deep, ≥20% REM
- **Good:** ≥6h, decent deep/REM
- **Fair:** ≥6h but low deep (<10%) or low REM (<15%)
- **Poor:** <6h total sleep

### Heart Rate (Overnight/Recent)

```python
samples = api.get_metric_samples(
    (now - timedelta(hours=10)).isoformat(),
    now.isoformat(),
    "HeartRate"
)
values = [s['value'] for s in samples if 'value' in s]
avg_hr = sum(values) / len(values)
resting_estimate = sorted(values)[:max(1, len(values)//10)][-1]
```

### HRV (Recovery Signal)

```python
samples = api.get_metric_samples(
    (now - timedelta(hours=12)).isoformat(),
    now.isoformat(),
    "HeartRateVariabilitySDNN"
)
values = [s['value'] for s in samples if 'value' in s]
avg_hrv = sum(values) / len(values)
```

Higher HRV = better recovery. Typical range: 20-80ms (varies hugely by person).

### Calendar (Today's Events)

```python
# Adjust start hour for the user's timezone
day_start = now.replace(hour=5, minute=0, second=0, microsecond=0)  # 5 UTC ≈ midnight ET
day_end = day_start + timedelta(hours=24)

events = api.get_calendar_events(day_start.isoformat(), day_end.isoformat())
for e in events:
    print(f"{e.get('title')} — {e.get('start_time')} {'📍 ' + e['location'] if e.get('location') else ''}")
```

### Weather (via wttr.in — no API key needed)

```bash
# One-liner for current conditions
curl -s "wttr.in/YOUR_CITY?format=%l:+%c+%t+%h+%w"

# JSON format for parsing
curl -s "wttr.in/YOUR_CITY?format=j1"
```

Replace `YOUR_CITY` with the user's location (e.g., `New+York`, `London`, `San+Francisco`).

### Steps (Yesterday)

```python
samples = api.get_metric_samples(
    (now - timedelta(hours=24)).isoformat(),
    now.isoformat(),
    "StepCount"
)
total_steps = sum(s.get('value', 0) for s in samples)
```

## Composing the Briefing

This is where the magic happens. **Calibrate everything to sleep quality.**

### Poor Sleep (< 6 hours)

Keep it **short, warm, and gentle**. The user is running on fumes.

```
☁️ Morning. You got about 4.5 hours — rough one.

Resting HR is up a bit at 68. Your body's working harder today.

You've got 2 meetings — the 10am standup and 2pm review.
Consider pushing anything that isn't urgent.

52°F and cloudy. Coffee weather.

Take it easy today. 💛
```

**Rules for poor sleep briefings:**
- No exclamation marks or forced cheerfulness
- Mention only essential calendar items
- Suggest deferring non-critical tasks
- Keep under 100 words
- Gentle, supportive tone

### Fair Sleep (6-7h, low quality)

**Moderate detail, practical tone.** They're functional but not at 100%.

```
🌤 Morning — you got 6.2 hours. Not bad, but deep sleep was
only 8%, so you might feel groggy.

HR 62 avg, HRV at 38ms — your body's doing okay.

Today: standup at 10, lunch with Sarah at 12:30 (don't forget!),
and the quarterly review at 3. Might want to prep for that one
during your peak focus window this morning.

Local weather: 65°F partly cloudy, nice for a walk.

You've got this. Pace yourself.
```

### Good Sleep (7h+, solid quality)

**Full detail, upbeat, actionable.** They can handle it.

```
☀️ Good morning! Solid 7.4 hours — 18% deep, 22% REM.
Your brain did good work last night.

Resting HR 58, HRV 52ms — you're well-recovered.
Great day for the hard stuff.

📅 Today's lineup:
  • 9:30 — Team sync
  • 11:00 — 1:1 with Jamie (prep: review Q3 roadmap)
  • 12:30 — Lunch (no meetings — protect this!)
  • 3:00 — Design review (Conference Room B)
  • 5:00 — Gym? Yesterday was 4,200 steps — could use some movement.

🌤 Local weather: 72°F, sunny, 45% humidity. Beautiful day.

Let's make it count! 💪
```

### Excellent Sleep (7h+, great deep & REM)

**Detailed, enthusiastic, ambitious.** Push them to make the most of a great day.

```
🔥 Morning! 8.1 hours, 20% deep, 25% REM — textbook recovery night.
You're running on full batteries today.

HR 55, HRV 61ms — elite-tier recovery. Whatever you've been
doing, keep doing it.

📅 Packed day ahead:
  • 9:00 — Focus block (use this — you're sharp right now)
  • 10:30 — Product review with stakeholders
  • 12:00 — Lunch with the team
  • 2:00 — Workshop: Q4 planning
  • 4:30 — 1:1 with Alex (career chat — they've been crushing it)
  • Evening: 8,400 steps yesterday, maybe up the ante? Weather's perfect for it.

☀️ Local weather: 75°F, clear skies, light breeze. Perfect day.

You've got the energy — swing for the fences today!
```

## Tone Calibration Summary

| Sleep Quality | Length | Tone | Calendar Detail | Suggestions |
|---|---|---|---|---|
| Poor (<6h) | Short (~80 words) | Gentle, supportive | Essentials only | Defer, rest |
| Fair (6-7h) | Medium (~120 words) | Practical, steady | Key events + tips | Pace yourself |
| Good (7h+) | Full (~160 words) | Upbeat, actionable | All events + prep notes | Make it count |
| Excellent (7h+, great stages) | Full+ (~180 words) | Enthusiastic, ambitious | All events + opportunities | Push hard |

## CLI-First Fallback

If the collector cannot run, inspect the CLI directly and parse JSON with `jq`:

```bash
uv tool run fulcra-api --help
uv tool run fulcra-api calendar-events --help
```

## Automation

### Cron Job (Daily Briefing)

Set up a cron or scheduled task to run the briefing every morning:

```bash
# Example: 7:30 AM ET daily
30 7 * * * cd /path/to/workspace && python3 skills/fulcra-morning-briefing/collect_briefing_data.py > /tmp/briefing.json
```

Then have your agent read `/tmp/briefing.json` and compose the briefing using the tone rules above.

### Agent Heartbeat

Add to your `HEARTBEAT.md`:
```
- [ ] Morning briefing (7-9 AM, if not done today): Run skills/fulcra-morning-briefing/collect_briefing_data.py, compose briefing from verified sleep/cache + calendar/weather, deliver to the user
```

## Privacy

- **NEVER share the user's sleep, HR, HRV, calendar, or precise location data publicly.**
- In group chats, deliver only a generic status such as "your briefing is ready" unless the user explicitly approved sharing the specific category of data in that chat.
- If the user explicitly asks for a group-chat summary, keep it qualitative and minimal, for example "sleep looked solid" rather than exact hours, stages, HR, or HRV.
- Calendar event titles and locations may contain sensitive info; summarize, don't quote.
- This data is intimate. Treat it that way.

## Going Deeper: fulcra-context

This skill covers morning briefings. For **all-day biometric awareness** — stress detection, workout recovery, travel context, location awareness, and more — see the full **[fulcra-context](../fulcra-context/SKILL.md)** skill.

Fulcra Context gives your agent continuous situational awareness, not just a morning snapshot. If the user likes the briefing, that's the natural next step.

## Links

- [Fulcra Platform](https://fulcradynamics.com)
- [Context iOS App](https://apps.apple.com/app/id1633037434)
- [Developer Docs](https://fulcradynamics.github.io/developer-docs/)
- [Python Client](https://github.com/fulcradynamics/fulcra-api-python)
- [MCP Server](https://github.com/fulcradynamics/fulcra-context-mcp)
- [Discord](https://discord.com/invite/aunahVEnPU)
