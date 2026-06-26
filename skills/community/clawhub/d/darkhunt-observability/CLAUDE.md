# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**OpenClaw telemetry plugin** (`@openclaw/tracehub-telemetry`) that sends traces to Darkhunt Observability using OpenTelemetry. Hooks into the OpenClaw plugin API to capture agent/LLM/tool lifecycle events, buffers them into spans, and exports via OTLP/protobuf.

## Commands

```bash
npm run build                              # TypeScript compile → dist/
npm test                                   # Run all tests (vitest)
npm run test:watch                         # Watch mode
npx vitest run test/payload.test.ts        # Run a single test file
./scripts/package.sh                       # Build, test, and package zip for ClawHub upload
./scripts/package.sh --no-deps             # Package without bundling node_modules
```

## Architecture

All plugin source is in `src/`. The data flow is a linear pipeline:

```
OpenClaw Hook Events → HooksAdapter → SpanBuffer → SpanBuilder → Payload Filter → Exporter
```

**Key modules:**

- **`index.ts`** — Plugin entry point. Calls `validate()` → `buildResource()` → `TraceHubExporter()` → `SpanBuffer()` → `registerHooks()`. Also registers CLI commands and optional runtime event listeners.
- **`hooks-adapter.ts`** — Registers 8 OpenClaw hooks (`message_received`, `before_agent_start`, `agent_end`, `llm_input`, `llm_output`, `before_tool_call`, `after_tool_call`, `shutdown`) and routes parsed event data into the SpanBuffer.
- **`span-buffer.ts`** — Buffers start/end event pairs keyed by `sessionKey + id`. Matches tool results from `llm_input` history back to `before_tool_call` spans. Also handles `runtime.events.onAgentEvent` for runId, tool meta, and TTFT timestamps.
- **`span-builder.ts`** — Constructs OpenTelemetry `ReadableSpan` objects from buffered state. Sets type-specific attributes (tokens/cost for generations, success/meta for tools). Applies payload mode and size limits before finalizing.
- **`payload.ts`** — Content truncation and sanitization. Three payload modes: `metadata` (no content), `debug` (truncated to char limits), `full` (byte limits, 64KB max per span). Maintains a safe-tool allowlist — unknown tool params are redacted.
- **`exporter.ts`** — Wraps `OTLPTraceExporter` with batching (default: 50 spans or 2000ms delay).
- **`types.ts`** — All TypeScript interfaces: `PluginConfig`, `PayloadMode`, buffered span types, hook event data types.
- **`cli.ts` / `setup.ts`** — CLI commands (`tracehub setup/config/status/set`) and interactive setup wizard.
- **`config.ts`** — Validates config, normalizes header shortcuts (`authorization`, `workspace_id`, `application_id`).
- **`trace-id.ts`** — Deterministic trace ID via SHA-256 of sessionId (same session = same trace).
- **`resource.ts`** — Builds OTel Resource with service metadata.

## Key Design Decisions

- **Trace ID determinism**: `SHA-256(sessionId)[:16]` ensures all spans in a session share one trace. Span IDs are random.
- **Safe-tool allowlist**: 16 built-in tool names (plus aliases like Read, Write, Bash) always show parameters; custom/unknown tool params are redacted for privacy.
- **Span pairing**: Spans require matching start+end events. Tool results are retroactively extracted from the next `llm_input` message history rather than from `after_tool_call` directly.
- **ESM only**: `"type": "module"` with ES2022 target and Node16 module resolution.

## Testing

Tests are in `test/` using Vitest. They use mocked OTel Resources and cover span lifecycle, payload truncation/sanitization, span building per type, batching, and trace ID generation. No external services needed to run tests.
