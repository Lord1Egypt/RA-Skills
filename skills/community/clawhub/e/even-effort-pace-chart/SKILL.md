---
name: even-effort-pace-chart
display_name: 体感一致配速表
display_name_en: Even-Effort Pace Chart
description: "Convert GPX/KML routes or recorded FIT tracks into even-effort trail running pace charts, or compare FIT activities with checkpoint plans and segment elapsed times. Use for race pacing, SVG pace tables, or post-race actual-versus-plan comparisons. Independent implementation inspired by the even-effort pacing approach from 耐力学社. Repository: https://github.com/yihouzenmeban/trail-running-pace"
description_zh: "基于耐力学社体感一致配速思路的独立实现。把 GPX/KML 路线或 FIT 轨迹转换成按检查点分段的体感一致越野配速表，或把 FIT 活动与检查点方案对照，查看累计差距、分段耗时与地形差异。适用于赛前配速规划、SVG 配速表输出与赛后实际对照。仓库地址：https://github.com/yihouzenmeban/trail-running-pace"
description_en: "Convert GPX/KML routes or recorded FIT tracks into even-effort trail running pace charts, or compare FIT activities with checkpoint plans and segment elapsed times. Use for race pacing, SVG pace tables, or post-race actual-versus-plan comparisons. Independent implementation inspired by the even-effort pacing approach from 耐力学社. Repository: https://github.com/yihouzenmeban/trail-running-pace"
version: 1.0.3
agent_created: true
---

# Even-Effort Pace Chart Skills

Resolve script paths relative to this file's directory, regardless of the user's working directory. Both workflows share the existing route processing and pacing model; do not duplicate or retune the model for an activity comparison.

Apply **current explicit request > selected configuration > script defaults**. Use a minimal configuration with the requested target, explicit overrides, and confirmed route selections. Omit unspecified fields; preserve valid zeros and `false`. Do not inherit settings from unrelated charts or examples, fill defaults with `null`/empty strings, or ask about optional fields with usable defaults.

## Choose the workflow

- **Pace chart:** use `scripts/pace_chart.py` and the steps below. Python 3.10+ and the standard library suffice for GPX/KML; FIT routes need the optional dependency described in the configuration reference.
- **Post-race actual-versus-plan comparison:** use `scripts/compare_activity.py` and follow Chinese [activity comparison](references/comparison.md) or English [activity comparison](references/comparison.en.md), instead of the pace-chart export steps below. `inspect`/`generate` are offline with an optional FIT dependency; `list`/`fetch` access Garmin only when retrieval is requested. Reuse the supplied configuration, preserve exact requested targets, and resolve ambiguous actual passages before generation. This workflow defaults to comparison SVG, not a pace chart; time labels describe the recorded activity as ahead/behind or faster/slower (positive plan-minus-actual means ahead/faster). Terrain labels show repository-more/less; JSON deltas retain plan-minus-actual values.

Read configuration/model references only when needed for model or route choices: Chinese [configuration](references/configuration.md) / [model](references/model.md), English [configuration](references/configuration.en.md) / [model](references/model.en.md). Activity-only requests do not require loading the entire model reference or retrieving online data.

## Pre-race pace charts

Default output is SVG, with segment pace in parentheses and a local 06:00 start. A supplied start time changes `start_time` only. Select `secondary_display: "arrival_time"` or `"equivalent_pace"` only when requested or already selected in the supplied configuration. Legacy `pace_basis: "equivalent"` still selects equivalent pace when `secondary_display` is absent.

### Inspect the route first

```bash
python3 <skill-dir>/scripts/pace_chart.py inspect <route-file>
```

Read the inspection JSON. Prefer embedded CPs, preserve their names and numbering, and use the returned candidate IDs. Start/finish rows are added automatically. Ask for manual names and cumulative distances only when embedded CPs are absent or unusable.

Review `diagnostics` and warnings for elevation corrections, poor positioning metadata, and distance sensitivity. Trial simplification does not prove drift; never enable `distance_tolerance_m` without an explicit request or selected configuration. Pass the selected processing options to inspection as well as generation, and recheck CP positions after changing distance processing.

Resolve ambiguous inputs before generation:

- Multiple routes: obtain the intended 1-based `track_index`; separate lines are not joined.
- Unrecognized station names: confirm `cp_selection`, rather than treating every landmark as a CP.
- Loops/crossings or offsets over 100 m: confirm the route occurrence with a processed-route `distance_km` override, or confirm `allow_off_route`; do not silently choose the nearest projection.
- KML missing/ground-clamped altitude mode: verify supplied heights before `inspect --use-kml-altitudes` and `use_kml_altitudes: true`. Never fill missing heights with zero. See configuration for supported KML modes and geometry.
- FIT or single-FIT ZIP as the route: preserve recorded distance and use record elevations, with `distance_tolerance_m: 0`. Supply manual CPs on that distance axis; reuse confirmed passages from an existing comparison to map its stations when available. See configuration for FIT validation and duplicate-distance handling. Keep recomputed route ascent distinct from Garmin lap/session totals.

### Set targets and assumptions

Obtain the finish target if missing. Interpret equivalent duration expressions consistently (for example, 300 minutes is `05:00`). A `target` expands to five columns with 30-minute spacing; `target_step_minutes` changes the interval. Use `targets` for an exact list, including a request for only one column. Ask when the requested targets or number of columns conflict. When replacing a selected configuration's list with a new central target, remove old `targets`; otherwise the script keeps list precedence and warns. If expansion gives nonpositive durations, obtain an explicit list or interval.

Targets include station rests, which default to zero. Map a requested station's rest or cutoff to its inspected candidate ID in `checkpoint_overrides`. Do not invent cutoffs or a race date. Cutoffs are elapsed durations; confirm start/date/rollover when converting clock cutoffs. Missing cutoffs stay unchecked and are omitted from station cells. For manual official-distance mismatches, confirm before using `distance_alignment: "scale"`; see configuration for the threshold and schema.

For example, “生成体感一致配速表，目标完赛时间 5 小时，相邻方案间隔 30 分钟，出发时间早上六点” maps to:

```json
{
  "target": "05:00",
  "target_step_minutes": 30,
  "start_time": "06:00"
}
```

This keeps the default pace display and SVG export. Ascent defaults to no window averaging (`ascent_smoothing_m: 0`), applying a 10 m peak/valley reversal threshold directly to cleaned source elevation vertices. Display smoothing is independent. An explicit positive `ascent_smoothing_m` enables ascent averaging. Consult the model for filtering choices and the explicit `window` alternative. Interpolation adds no measurement accuracy; never tune filters or rescale climbs solely to force a platform's total or claim equivalence to RunArt.Net.

### Plan water when requested

The default `water_mode: "distance"` is offline and compares equivalent-distance demand. If the user asks to customize their water plan but the intended approach is unclear, ask what they want before generating; do not substitute a default comparison or a blank chart for a requested personalized recommendation. If they request water based on weather or personal needs, follow the time-based workflow even if they do not say "time-based", unless they explicitly choose another method.

For a personalized plan, proactively ask for missing race date and start time when needed for weather, personal drinking experience, carrying capacity, and station water availability. Reuse information already provided. If the user does not know their drinking rate, ask about training intake records or sweat rate and explain that this tool cannot infer a personal rate from weather. If they want help estimating, discuss an evidence-based candidate or range with its assumptions and uncertainty, then obtain their confirmation before using it. Do not invent or silently assume a rate, per-leg overrides, weather, or buffer; do not present a personalized amount without a confirmed rate.

Select `water_mode: "time"` for a time-based or personalized request, or when present in the selected configuration. Its outgoing-leg water is `(moving hours + buffer minutes / 60) * confirmed personal rate in ml/h`; station rest is excluded, the buffer applies to each leg, and the finish is zero. For multiple displayed targets, obtain `water_target` matching one of them; an explicit one-element `targets` list needs no separate selection.

For automatic weather, obtain the actual local race date and time in `start_time` and the IANA zone in `water_timezone`. Explain that each leg's midpoint coordinates are sent to Open-Meteo; its free API is for non-commercial use. Run `generate` as below. When stdout returns `status: "needs_water_confirmation"`, no chart has been written: present the leg forecasts and their retrieval time, ask the user to confirm them and supply their personal `water_ml_per_hour` and any desired buffer or departure-station rate overrides. Forecast values are temperature in °C, relative humidity in %, wind speed in km/h, and precipitation probability in %. Copy the entire returned `water_weather` object into the configuration, set its `confirmed` to `true` only after confirmation, and run `generate` again. A matching confirmed snapshot is reused without another request; remove it to obtain an updated preview. Changes to route, target, start, zone, or station schedule require a new preview.

Forecasts cover at most 16 days and can be unavailable or incomplete. If automatic weather is unsuitable, obtain user-confirmed conditions and use `"water_weather": {"source": "manual", "confirmed": true, "description": "..."}` with the confirmed rate; this path needs no network, race date, or time zone. Weather informs the user's choice; the script does not apply an automatic weather multiplier. Confirm that the next stations actually supply water and that the runner's carrying capacity is adequate; if either is unknown, say so, and if a station has no water, account for the next actual refill separately. Forecasts and estimates are not guarantees of conditions or hydration needs.

### Generate and verify

Write the selected assumptions to a JSON file, then run:

```bash
python3 <skill-dir>/scripts/pace_chart.py generate <route-file> \
  --config <race.json> --output-dir <output-dir>
```

When the user specifies exports (`svg`, `html`, `csv`, `json`), set `output_formats` to exactly those formats, overriding any different selection in an existing configuration. Otherwise preserve the selected configuration or default to SVG. Existing selected files require another directory or authorized `--overwrite`. Use the script's native renderers; they implement the table style, cutoff visibility, and metadata.

Before running, compare the configuration with the request. If the user asks to review or approve it first, present the intended parameters and wait for confirmation before running `generate` or writing outputs. After success, read stdout `summary`: effective `parameters`, `target_source`, `targets_seconds`, route statistics, ordered `checkpoints`, and `verification`. Confirm finish targets/rest checks, review cutoff failures and warnings, and compare exported files with the request. For presentation-sensitive changes, render locally and inspect station names and target columns.

Deliver output paths, route statistics, targets, and material assumptions in the user's language; chart labels remain Chinese. Explain whether next-leg water is an equivalent-distance comparison or a time estimate based on the user's confirmed rate and weather. Do not assess fitness from a route alone.
