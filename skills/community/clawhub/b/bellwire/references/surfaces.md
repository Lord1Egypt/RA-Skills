# Bellwire live Surfaces

- [Rules and command](#rules-and-command)
- [`stats`](#stats)
- [`metrics`](#metrics)
- [`progress`](#progress)
- [`segmented_progress`](#segmented_progress)
- [`alert`](#alert)
- [`timer`](#timer)
- [`status`](#status)
- [`checklist`](#checklist)
- [`trend`](#trend)
- [Agent-requested Live Activities](#agent-requested-live-activities)

## Rules and command

Live Surfaces are mutable, agent-defined cards. Use a stable lowercase key so
later calls update the same card instead of creating duplicates.

For production application code, call the same `PUT` endpoint with the
project-scoped `BELLWIRE_INGEST_TOKEN`. Reserve `BELLWIRE_AGENT_TOKEN` for the
management CLI and configuration work.

```bash
node <skill-dir>/scripts/bellwire.mjs upsert-surface \
  --project <project-id> \
  --key sales-today \
  --file surface.json
```

Every Surface requires `type` and `title`; `subtitle` and an `open_url` action
are optional. Bellwire renders only the native types below and never executes
code from a Surface payload.

## `stats`

Use for already-computed business values. Supports 1-8 metrics. Values may be
strings or numbers.

```json
{
  "type": "stats",
  "title": "Sales",
  "subtitle": "Today",
  "metrics": [
    { "label": "Revenue", "value": "¥2,430", "color": "green" },
    { "label": "Orders", "value": 37, "color": "blue" }
  ]
}
```

## `metrics`

Use for 1-4 numeric operational measurements. Each metric may include `unit`.

```json
{
  "type": "metrics",
  "title": "API health",
  "metrics": [
    { "label": "CPU", "value": 18, "unit": "%", "color": "cyan" },
    { "label": "Memory", "value": 42, "unit": "%", "color": "purple" }
  ]
}
```

## `progress`

Send either `percentage` from 0-100, or `value` with a positive `upperLimit`.

```json
{ "type": "progress", "title": "Search reindex", "percentage": 68 }
```

## `segmented_progress`

Use 1-12 steps and a `currentStep` from zero through the step count.

```json
{
  "type": "segmented_progress",
  "title": "Production deploy",
  "numberOfSteps": 5,
  "currentStep": 3,
  "stepLabel": "Running migrations"
}
```

## `alert`

Use for an important current state. `icon.symbol` accepts an SF Symbol name.

```json
{
  "type": "alert",
  "title": "Approval needed",
  "message": "Send the follow-up to Brightlane?",
  "icon": { "symbol": "sparkles", "color": "yellow" },
  "badge": { "title": "Agent", "color": "green" }
}
```

## `timer`

Use `durationSeconds` from 1 second through 7 days. Set `countsDown` to false
for elapsed runtime.

```json
{ "type": "timer", "title": "Benchmark", "durationSeconds": 300, "countsDown": true }
```

## `status`

Use for a durable semantic state rather than an urgent alert. `state` must be
`neutral`, `running`, `success`, `warning`, `critical`, or `paused`. The native
client owns the state color and icon; `label` is an optional short override.

```json
{
  "type": "status",
  "title": "Production API",
  "subtitle": "All regions are serving traffic",
  "state": "success",
  "label": "Operational"
}
```

## `checklist`

Use for a read-only Agent workflow with 1-8 stable items. Item states are
`pending`, `running`, `completed`, `failed`, and `skipped`. Reuse item IDs so
updates preserve identity and ordering.

```json
{
  "type": "checklist",
  "title": "Production release",
  "items": [
    { "id": "build", "title": "Build", "state": "completed" },
    { "id": "deploy", "title": "Deploy", "detail": "Cloudflare Worker", "state": "running" },
    { "id": "smoke", "title": "Smoke test", "state": "pending" }
  ]
}
```

## `trend`

Use for one ordered series of 2-30 finite points. Bellwire compares the first
and last point. `goal` is `up`, `down`, or `neutral`, allowing the client to
show whether the movement is favorable without guessing the metric's meaning.

```json
{
  "type": "trend",
  "title": "API latency",
  "points": [
    { "label": "09:00", "value": 142 },
    { "label": "10:00", "value": 128 },
    { "label": "11:00", "value": 119 }
  ],
  "goal": "down",
  "displayValue": "119 ms",
  "unit": "ms"
}
```

Supported colors are `lime`, `green`, `cyan`, `blue`, `purple`, `magenta`,
`red`, `orange`, `yellow`, and `gray`.

## Agent-requested Live Activities

Add an explicit top-level `liveActivity` directive when the Surface represents
a bounded running session. Omit it for ordinary cards. Keep `sessionId` stable
for every update in one run, then publish `state: "ended"` when the run finishes.

```json
{
  "type": "status",
  "title": "Deploying production",
  "state": "running",
  "liveActivity": { "sessionId": "deploy-20260807", "state": "active" }
}
```

Bellwire starts these only after the user enables Automatic Live Activities.
Hosted projects use ActivityKit push delivery. Private projects start locally
while the app is in the foreground and never register their Activity token with
Bellwire Cloud. Bellwire allows one Agent activity per project, up to three per
device, and sessions end when the Agent publishes `ended` or after eight hours.
