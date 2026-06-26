---
name: dyagil-marathon-clip
description: Render a 30-second vertical (1080x1920) running-recap video from per-workout data using Remotion + ffmpeg + royalty-free music. Use when the user wants a Strava/Garmin-style weekly recap clip, a workout video for Stories/Twitter/WhatsApp, or wants to share their marathon-training progress as a short shareable MP4.
version: 1.0.0
license: MIT
author: dyagil
---

# Marathon Clip — Weekly Running Recap

> This skill is tuned for a specific personal data source (a local SQLite DB populated from Garmin Connect). The Remotion + ffmpeg pipeline and the visual composition are fully reusable — fork the data-extraction step and point it at your own source (Strava API, Apple Health export, CSV, etc.).

Render a 30-second 9:16 video summarizing the last week (or N days) of running activity. The output is a Stories-ready MP4 with animated stats, per-run bars, a stroke-animated GPS map, and royalty-free background music.

## When to Use

Use this skill when the request matches:
- "Make a clip of this week's runs"
- "Weekly running summary video" / "Marathon recap"
- "Strava-style story" / "Stories video of my runs"

Do **not** use this for:
- Non-running activities (strength, swim) — needs a different template.
- Generic video generation without per-workout data — use a general-purpose Remotion toolkit instead.

## What It Does

Pulls the last N days of `type='run'` workouts from a local SQLite DB (`<project>/data/sahi.db` by default), downloads GPX tracks via the Garmin Connect API, writes both to JSON, and renders **six animated sequence types**:

1. **Intro** (4s) — Animated title with athlete name + period.
2. **Big Stats** (9s) — Count-up animations for km / hours / kcal / runs.
3. **Map Scenes** (4s each) — One per run with GPS: animated stroke-dash polyline, pulsing runner marker along the path, start/finish markers, per-run footer.
4. **Trends** (8s) — Side-by-side comparison vs the prior week with arrows (▲ better / ▼ worse), an overall verdict (CRUSHING IT / STEADY / RECOVERY / EASIER WEEK), and per-metric deltas in %.
5. **Runs Breakdown** (8s) — Average pace + horizontal bars per run.
6. **Outro** (5s) — Closing card with totals.

Total length: typically 30–60s depending on number of runs with GPS data.
A fade-in/fade-out royalty-free track plays through (`public/music.mp3`).

## Run It

```bash
~/bin/marathon-clip                  # last 7 days, default music, → out/marathon-week.mp4
~/bin/marathon-clip --days 14
~/bin/marathon-clip --out /tmp/x.mp4
~/bin/marathon-clip --no-music
~/bin/marathon-clip --music other.mp3
~/bin/marathon-clip --send-telegram   # render and post to Telegram (requires openclaw CLI)
```

Default project location: `<workspace>/projects/sahi-video/`.

### Manual weekly invocation

```bash
bash <skills-dir>/marathon-clip/scripts/weekly.sh
```

Always renders the **previous Monday→Sunday** window regardless of when invoked, and writes `out/weekly-YYYY-MM-DD.mp4`. The last line of stdout is `MARATHON_CLIP_OUT=<absolute path>`.

### Automated weekly delivery (optional)

If you use the OpenClaw cron system, register a job to run `scripts/weekly.sh` every Monday 09:00 in your timezone. Manage it via:

```bash
openclaw cron list
openclaw cron show <id>
openclaw cron enable <id> / disable <id>
openclaw cron run <id>      # fire now (test)
```

The cron payload is a system event addressed to the main agent session; the agent runs `weekly.sh` and posts the resulting MP4.

## Customization Knobs

### Visual style
Edit `<project>/src/MarathonClip.tsx`:
- **Colors:** the green gradient lives in `Background` (~line 40). Replace with brand colors.
- **Logo:** `Logo` component (top right).
- **Layout:** each sequence is its own component (`Intro`, `BigStats`, `RunsBreakdown`, `Outro`).

### Music
Drop an mp3 into `<project>/public/` and pass `--music your-file.mp3`. To trim/fade a new track:

```bash
ffmpeg -y -i source.mp3 -ss 0 -t 30 \
  -af "afade=t=in:st=0:d=0.5,afade=t=out:st=28.5:d=1.5" \
  -ac 2 -ar 44100 -b:a 192k music.mp3
```

### Map / GPS
Map scenes are pure SVG with custom lat/lon projection (longitude scaled by `cos(meanLat)` for correctness). No tile loading, no external map service — fully headless. The polyline animates via `stroke-dasharray` + `stroke-dashoffset` for the drawing effect, with a pulsing marker following the head of the line.

To regenerate just the tracks without re-rendering: `node scripts/build-tracks.cjs --days 7`.

### Data source
The extractor (`scripts/build-data.cjs`) runs:

```sql
SELECT local_date, duration_min, distance_km, calories, notes
FROM workouts
WHERE type='run' AND local_date >= date('now','-7 day')
ORDER BY local_date ASC
```

**Adapting this skill:** rewrite `build-data.cjs` to query your own data source (Strava, Apple Health export, CSV). It must produce a `data.json` with this shape:

```json
{
  "athlete": "Name",
  "period": "May 8 – May 15",
  "totals": {"km": 42.1, "hours": 4.2, "kcal": 3100, "runs": 5},
  "runs": [
    {"date": "2026-05-09", "km": 8.2, "pace": "5:12/km", "calories": 620, "gpx": "...optional polyline data..."}
  ],
  "prev": { "...same shape, previous week..." }
}
```

## Dependencies

- **Node.js** + `npm` (Remotion v4)
- **ffmpeg** (music trim/fade)
- **Chrome Headless Shell** — auto-installed by Remotion on first render
- **Linux libs** for headless Chrome: `libnss3 libatk1.0-0 libgbm1 libxdamage1`

If anything's missing, a sibling `remotion-server` skill has `scripts/setup.sh` that installs the apt deps.

## Render Time + Cost

- ~70–90 seconds on a 2-core VPS at `concurrency=2`.
- Output size: ~3 MB MP4 (H.264 + AAC stereo).
- No external API calls during render — everything local.

## Delivery (OpenClaw note)

⚠️ Some chat delivery channels only accept files under `~/.openclaw/media/outbound/`. Files under `<project>/out/` won't deliver. `weekly.sh` already copies the final MP4 to the outbound dir with a UUID. Use the `MARATHON_CLIP_DELIVER` env line (not `MARATHON_CLIP_OUT`) when assembling the `MEDIA:` line for chat delivery.

## Troubleshooting

- **"no such table: activities"** — the schema uses `workouts`, not `activities`. Adjust your `build-data.cjs` query.
- **Music doesn't play** — Remotion v4 needs `staticFile()` and the file must be in `public/`. Use the `Audio` component, not `<audio>`.
- **"Cannot find module 'zod'"** — run `npm install zod` in the project root.
- **Render hangs at "Spinning up browser"** — first run only, downloading Chrome Headless Shell (~200 MB).
- **Empty data** — check the date filter; if no runs synced recently the output will be empty. Trigger your data sync first.

## Files

```
<skills-dir>/marathon-clip/
  SKILL.md
  scripts/
    build-data.cjs      ← SQL → data.json (customize for your data source)
    render.sh           ← end-to-end pipeline
  references/
    musical-sources.md  ← curated list of CC/PD music sources

<project>/sahi-video/
  src/                  ← Remotion composition
  public/music.mp3      ← 30s royalty-free track
  data.json             ← generated each run
  out/                  ← rendered MP4s

~/bin/marathon-clip     ← symlink to scripts/render.sh
```
