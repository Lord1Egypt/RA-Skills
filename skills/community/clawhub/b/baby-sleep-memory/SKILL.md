---
name: baby-sleep-memory
description: Record overnight baby-monitor and nursery audio and turn it into a searchable sleep log — cry events with time, duration, and intensity, feed times, wake windows, and settling method — then recall patterns across nights to find what is actually changing. Who pays and why: pediatric sleep consultants and sleep-training services pay because parents hand them vague "baby wakes a lot" reports and the consultant wastes paid sessions re-deriving a baseline instead of prescribing a fix. Pilot price: $149 one-time for a 14-day sleep-log pilot on one family's nursery audio. Use when a sleep consultant, doula, or new parent needs objective, recallable infant sleep and cry history across nights. Requires a BlueColumn API key (bc_live_*).
---

# Baby Sleep & Cry Memory — BlueColumn Skill

A parent cannot log what happens at 3:40 AM, and a consultant cannot coach what they cannot see. This skill turns overnight nursery and baby-monitor audio into an indexed sleep log — every cry event, feed, and wake window with a timestamp and intensity — and lets you recall patterns across nights instead of relying on a sleep-deprived parent's memory.

## Setup

Get a free key at https://bluecolumn.ai/login (no card). Keys look like `bc_live_*`. Base URL: `https://api.bluecolumn.ai`.

## Store the night's audio

Send the monitor recording; BlueColumn transcribes and indexes the events as structured sleep-log entries.

```bash
curl -X POST https://api.bluecolumn.ai/remember \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://example.com/nursery/2026-10-03-overnight.mp3",
    "text": "SLEEP LOG — infant=Theo (5mo), night of 10-03. Bedtime 19:10, asleep 19:25. Cry event 23:40 (2m, low intensity, self-settled). Feed 01:15 (12 min). Cry event 03:50 (6m, high intensity, settled by rocking 4m). Wake window 03:50-04:10. Woke 06:20 for day. Notes: last feed was 20:30, room 22C, white noise on.",
    "title": "sleep-log - Theo 5mo - 2026-10-03"
  }'
```

## Find patterns across nights

Ask what changed, not just what happened.

```bash
curl -X POST https://api.bluecolumn.ai/recall \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"q": "For Theo over the last 7 nights, has the 03:50 night waking gotten earlier or longer, and what settling method followed each one?"}'
```

## Log a one-off observation

Capture a single detail the audio cannot show — illness, travel, a schedule change.

```bash
curl -X POST https://api.bluecolumn.ai/note \
  -H "Authorization: Bearer $BLUECOLUMN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"text": "Theo: started sleep training 10-04 (extinction, 5m check-ins). Expect short-term regression; do not flag as a new pattern until 3 nights of data.", "tags": ["sleep-log", "theo-5mo", "training"]}'
```

## Workflow

1. **Each morning** — store the overnight monitor audio with a structured summary (bedtime, cry events with time/duration/intensity, feeds, wake windows, settling method).
2. **Before a consult** — recall the last 7-14 nights to establish the baseline and spot the trend.
3. **After changes** — log interventions (method, schedule, environment) so recall can separate cause from coincidence.
4. **Report** — recall produces a per-night + trend summary the consultant can hand the parent as an objective log.

## Billing

If the API returns `402` or `429`, read `topup_url` / `upgrade_url` from the error body and surface that link to the user — do not retry.

## Docs

API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags` (not `content`/`query`/`note`).
