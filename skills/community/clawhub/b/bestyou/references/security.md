# Security & Privacy

## Data Handling

BestYou shares **processed insights only** through the MCP API. The API returns readiness scores, coaching narratives, macro summaries, and workout plans. It never returns raw HealthKit data, raw sensor readings, or raw wearable telemetry.

## API Key Security

- API keys are generated per-user inside the BestYou iOS app (More → Connected Apps → OpenClaw → Generate Key).
- Keys use Bearer token authentication in the HTTP Authorization header.
- Keys are revocable at any time from the iOS app.
- Each key is scoped to specific permissions (read:brief, read:action_plan, write:workout, write:nutrition).

## No Local Data Persistence

This skill does not store health data locally. It contains only markdown instructions for agent behavior. All health data is fetched live from the BestYou API per request and displayed in the conversation. Nothing is cached or written to disk.

## Network Operations

All API calls go through mcporter to a single endpoint: `https://mcp.bestyou.ai/mcp`. No other outbound network calls are made. The skill does not download or execute external code.

## No Shell Execution

This skill is pure markdown instructions. It contains no scripts, no executable code, and no shell commands that run automatically. Setup commands in the documentation are presented for the user to run manually.

## HealthKit Privacy

HealthKit readings (heart rate, HRV, sleep stages, steps, glucose, etc.) are processed by BestYou's 19 on-device AI agents on the iPhone. Raw HealthKit data never leaves the device. Only the processed insights and recommendations are transmitted through the API when explicitly requested by the user.
