# Security & Privacy

## Data Handling

BestYou shares **processed insights only** through the MCP API. The API returns readiness scores, coaching narratives, macro summaries, and workout plans. It never returns raw HealthKit data, raw sensor readings, or raw wearable telemetry.

## API Key Security

- API keys are generated per-user inside the BestYou iOS app (More → Connected Apps → OpenClaw → Generate Key).
- Keys use Bearer token authentication in the HTTP Authorization header.
- Keys are revocable at any time from the iOS app.
- Each key is scoped to specific permissions (read:brief, read:action_plan, write:workout, write:nutrition).

## No Local Data Persistence

This skill does not store health data locally. All health data is fetched live from the BestYou API per request and rendered as visual widgets. Nothing is cached or written to disk.

## Network Operations

All API calls go through mcporter to a single endpoint: `https://mcp.bestyou.ai/mcp`. No other outbound network calls are made. The skill does not download or execute external code.

## HTML Template Security

All HTML templates in `assets/` use **safe DOM methods** for rendering dynamic data:
- `document.createElement()` + `textContent` + `appendChild()` for building elements
- No `innerHTML` assignments with dynamic data
- No `eval()`, `Function()`, or `document.write()`
- No inline event handlers (`onclick`, `onload`, etc.)
- No external script sources
- No fetch/XMLHttpRequest calls

Templates receive data through a `window.loadData()` function and render it using safe DOM construction only.

## No Shell Execution

This skill contains markdown instructions and static HTML templates. It has no executable scripts. Setup commands in the documentation are presented for the user to run manually.

## HealthKit Privacy

HealthKit readings (heart rate, HRV, sleep stages, steps, glucose, etc.) are processed by BestYou's 19 on-device AI agents on the iPhone. Raw HealthKit data never leaves the device. Only the processed insights and recommendations are transmitted through the API when explicitly requested by the user.
