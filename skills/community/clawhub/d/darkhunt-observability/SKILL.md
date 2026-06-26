# Darkhunt Observability

See what your OpenClaw agent actually does. No more black box.

This plugin sends real-time telemetry to Darkhunt Observability so you can see every agent run as a trace — what the agent decided, which tools it called, how long each step took, and how much it cost.

## What you get

- Full conversation traces so you see every step your agent takes: LLM calls, tool executions, and message flow as a connected timeline
- Tool visibility — which tools were called, what arguments were passed, whether they succeeded or failed
- User attribution — see which user triggered each conversation
- Multi-agent support — traces stay isolated per session, even with concurrent agents
- Cost tracking — know exactly how much each conversation costs, broken down by model call
- Token usage — input, output, cache read, and cache creation tokens per generation
- Performance timing — duration of every step, time-to-first-token for LLM responses

## Setup

Setup takes 2 minutes:

1. Install the plugin
2. Run `openclaw tracehub setup`
3. Restart the gateway

The wizard walks you through connecting to Darkhunt — just paste your API key and workspace ID.

## Commands

```bash
openclaw tracehub setup    # Interactive setup wizard
openclaw tracehub status   # Show current configuration and status
openclaw tracehub config   # Show raw plugin config as JSON
```

## Privacy & Data Control

3 payload modes control what data leaves your environment:

- **metadata** (default) — structural data only: model name, token counts, cost, duration, tool names, success/failure. No conversation content is exported.
- **debug** — metadata + truncated content (500 chars). Useful for troubleshooting.
- **full** — includes conversation content subject to size limits (4 KB per field, 64 KB per span). Only use if you trust the destination endpoint.

## Notes

- Free tier available at https://darkhunt.ai
- Exports via OTLP/protobuf (works with any OpenTelemetry-compatible backend)
- Never crashes your agent — all export errors are caught and logged
