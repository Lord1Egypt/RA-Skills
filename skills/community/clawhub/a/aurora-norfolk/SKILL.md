---
name: aurora-norfolk
description: produce a practical 3-day northern lights planning and live-update workflow for tim in dereham, norfolk, with alert-day escalation, north norfolk coast comparison, and conservative go or no-go decisions. use when asked to check aurora chances, build aurora alerts, compare dereham vs the coast, issue alert-night updates, or maintain a rolling northern lights watch for norfolk.
allowed-tools: web_search, http_request, calculator, file_read, file_write
---

# Aurora Norfolk

Produce a practical aurora-planning service for Tim in Dereham, Norfolk, UK.

Keep the job narrow:
- Plan for the next 3 nights.
- Compare Dereham against the North Norfolk coast.
- Escalate only when actionably better than normal background noise.
- Prefer useful decisions over dramatic language.

## Core objective

Estimate the **practical visible chance** of seeing the aurora for:
- **Dereham**
- **North Norfolk coast**

Treat the percentage as a blended viewing chance for Tim, not a pure physics probability. Combine space weather, darkness, cloud, visibility, moon penalty, and the horizon advantage of the coast.

## Data priority

Use sources in this order when available:

1. **NOAA SWPC** for aurora and geomagnetic conditions.
   - Use the short-lead OVATION aurora forecast for near-term timing.
   - Use real-time solar-wind context when describing why conditions are improving or fading.
   - Use the 3-day geomagnetic forecast for the rolling 3-day outlook.
2. **Met Office site-specific forecast data** for local sky conditions.
   - Compare Dereham with one or more North Norfolk coast points.
   - Focus on cloud and any visibility or haze proxies available.
3. **AuroraWatch UK** for UK-facing alert context and sanity checking.

If the authoritative feeds disagree, say so and lower confidence.
If a key feed is stale or unavailable, say so explicitly and reduce confidence.

## Locations

Always produce two location outcomes:
- **Dereham**
- **North Norfolk coast**

For the coastal view, prefer a place with a cleaner northern horizon and lower local light pollution than Dereham. If a specific coastal point is needed for weather lookup, pick a practical North Norfolk coastal point and stay consistent within that run.

## Decision model

Score the following components mentally and convert them into practical percentages:

### 1. Space-weather strength
Weight heavily:
- OVATION position and intensity
- Short-lead aurora forecast timing
- Geomagnetic forecast context
- Whether current conditions appear to be strengthening, holding, or fading

### 2. Sky quality
Weight heavily:
- Cloud cover during the best darkness window
- Visibility or haze signal if available
- Rain or mist that would ruin a viewing attempt

### 3. Darkness and moon penalty
Consider:
- Whether the best aurora timing lines up with full darkness
- Whether moonlight materially reduces faint visibility

### 4. Location advantage
Apply:
- Coastal bonus for a cleaner northern horizon
- Inland penalty for Dereham relative to the coast when conditions are otherwise similar

## Status thresholds

Set status from the **coast chance**:
- **no_watch**: under 20%
- **watchlist**: 20% to 34%
- **alert_day**: 35% to 54%
- **high_alert**: 55% or higher

These thresholds are operating rules for this workflow, not scientific absolutes.

## Travel recommendation rules

Use only one action:
- **stand_down**
- **watch**
- **go_local**
- **go_coast**

Apply these rules:
- Do **not** recommend travel on weak or noisy signals.
- Prefer **watch** when conditions are uncertain or marginal.
- Use **go_local** only when Dereham is meaningfully viable without a strong coast advantage.
- Use **go_coast** only when the coast beats Dereham by about 15 percentage points or more, or when the northern-horizon advantage is clearly decisive.
- If cloud is poor almost everywhere, prefer **stand_down** even when space weather is elevated.

## Communication modes

Choose the output mode that matches the request or automation stage.

### A. 3-day outlook
Use for the daily planning run.

Return a compact 3-night table with:
- date or night label
- dereham chance
- coast chance
- status
- confidence
- short note

Then add:
- best candidate night
- whether any night qualifies as **alert_day** or **high_alert**
- next scheduled check time

### B. Change alert
Use only when something materially changed.

Trigger a change alert when any of these happen:
- a night enters or leaves **alert_day** or **high_alert**
- coast chance changes by 10 percentage points or more
- action changes
- best window shifts by 60 minutes or more

Keep the message short:
- what changed
- old value to new value
- why it changed
- new action

### C. Alert-day brief
Use on any **alert_day** or **high_alert** night.

Return:
- dereham chance
- coast chance
- confidence
- best window in local time
- camera-only vs likely by-eye judgment
- 2 to 4 short reasons
- action
- next check time

### D. Live-night update
Use during the active viewing period.

Think in 15-minute checks but communicate in **30-minute viewing windows**.
Send a live-night update only when:
- a good window is opening,
- the action changed,
- the coast chance moved by 10 points or more,
- the chance collapsed and the user should stop waiting or not travel.

Return:
- current dereham chance
- current coast chance
- best next 30-minute window
- confidence
- 2 to 3 short reasons
- action
- next check time

## Output rules

Always:
- Use **Europe/London** local time.
- Use percentages for Dereham and coast.
- State **confidence** as low, medium, or high.
- Say whether the likely outcome is **camera-only**, **possible by eye**, or **good by-eye chance**.
- Be calm and plain.
- Explain uncertainty honestly.

Never:
- Present long scientific dumps.
- Recommend driving for weak yellow-noise type conditions.
- Pretend day-3 precision is as strong as same-night nowcasting.
- Spam repeated tiny updates.

## Default message templates

### 3-day outlook template

Use this structure unless a different format is explicitly requested:

```text
Aurora Norfolk — 3-night outlook

| Night | Dereham | Coast | Status | Confidence | Note |
| --- | ---: | ---: | --- | --- | --- |
| Tonight | 12% | 19% | no_watch | medium | weak activity, cloud risk |
| Tomorrow | 24% | 37% | alert_day | medium | better coast horizon and clearer sky |
| Day 3 | 18% | 28% | watchlist | low | setup possible but uncertain |

Best candidate: Tomorrow
Action now: watch
Next check: 17:30
```

### Change alert template

```text
Aurora update: Tomorrow moved from watchlist to alert_day.
Coast chance rose from 31% to 43%.
Best window shifted to 22:30–00:00.
Reason: stronger geomagnetic outlook and improved coast cloud forecast.
Action: watch.
```

### Alert-day brief template

```text
Aurora Norfolk — tonight

Dereham chance: 22%
North Norfolk coast chance: 41%
Confidence: medium
Best window: 22:30–00:00
Likely outcome: possible by eye on the coast, weaker inland

Why:
- aurora guidance is elevated enough for southern visibility
- cloud is thinner on the coast than inland
- timing lines up with full darkness

Action: go_coast
Next check: 21:15
```

### Live-night template

```text
22:00 update

Dereham: 18%
North Norfolk coast: 46%
Best next window: 22:30–23:00
Confidence: medium
Why:
- short-lead aurora guidance remains supportive
- coast cloud is still thinner than inland
- conditions are holding rather than strengthening

Action: go_coast
Next check: 22:15
```

## Workflow

Follow this order:

1. Determine the relevant local-night period in Europe/London time.
2. Read the most authoritative aurora guidance available for the requested horizon.
3. Read local sky conditions for Dereham and a North Norfolk coast comparison point.
4. Convert the combined picture into practical percentages.
5. Choose status from the coast chance.
6. Choose one action only.
7. Use the correct communication mode.
8. Suppress noise unless a material change threshold was met.

## Setup notes for OpenClaw

When this skill is used inside OpenClaw:
- Prefer a dedicated aurora agent rather than a general assistant.
- Keep the agent temperature low.
- Use cron for the repeating checks.
- Run a daily planning check in the morning.
- Run an evening brief on alert days.
- Run 15-minute live checks only on alert nights.

Read `{baseDir}/references/openclaw-setup.md` when installation or cron examples are needed.
Read `{baseDir}/references/source-checklist.md` when deciding what data to collect.
Read `{baseDir}/references/message-rules.md` when shaping notifications.
