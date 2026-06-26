# Observability (OpenTelemetry)

> Export traces, metrics, and events from the Agent SDK to observability backends using OpenTelemetry.

The SDK works by spawning a Claude Code CLI subprocess. The CLI has built-in OpenTelemetry instrumentation. The SDK does not produce telemetry data itself but passes configuration to the CLI process.

## Three Signals

| Signal | Content | Enable |
|:---|:---|:---|
| **Metrics** | tokens, cost, session counts, lines of code, tool decision counters | `OTEL_METRICS_EXPORTER` |
| **Log events** | Structured logs of every prompt, API request, API error, tool result | `OTEL_LOGS_EXPORTER` |
| **Traces** | Spans for each interaction, model request, tool call, hook (beta) | `OTEL_TRACES_EXPORTER` + `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1` |

## Configuring Export

```typescript
const otelEnv = {
  CLAUDE_CODE_ENABLE_TELEMETRY: "1",
  CLAUDE_CODE_ENHANCED_TELEMETRY_BETA: "1",  // traces (beta)
  OTEL_TRACES_EXPORTER: "otlp",
  OTEL_METRICS_EXPORTER: "otlp",
  OTEL_LOGS_EXPORTER: "otlp",
  OTEL_EXPORTER_OTLP_PROTOCOL: "http/protobuf",
  OTEL_EXPORTER_OTLP_ENDPOINT: "http://collector.example.com:4318",
  OTEL_EXPORTER_OTLP_HEADERS: "Authorization=Bearer your-token",
};

// TypeScript: env replaces inherited environment, need to spread process.env
options: { env: { ...process.env, ...otelEnv } }

// Python: env merges onto inherited environment
options = ClaudeAgentOptions(env=otelEnv)
```

⚠️ Do NOT set `console` as an exporter value — stdio is the SDK's messaging channel.

### Short-Lived Process Flush

Default: metrics export every 60s, traces/logs every 5s. Shorten intervals:
```typescript
OTEL_METRIC_EXPORT_INTERVAL: "1000",
OTEL_LOGS_EXPORT_INTERVAL: "1000",
OTEL_TRACES_EXPORT_INTERVAL: "1000",
```

## Trace Structure

- **`claude_code.interaction`**: Single turn of the agent loop
- **`claude_code.llm_request`**: Each Claude API call, with model name, latency, token counts
- **`claude_code.tool`**: Each tool call, with sub-spans including `tool.blocked_on_user` and `tool.execution`
- **`claude_code.hook`**: Each hook execution (requires beta detailed tracing)

Sub-agent spans are nested under the parent agent's `tool` span, forming a complete delegation chain. Spans include `session.id` attribute by default.

### Linking to Your Application's Traces

The SDK automatically propagates W3C trace context to the CLI subprocess. When an active OpenTelemetry span exists in your application, the SDK injects `TRACEPARENT` and `TRACESTATE`. The CLI also forwards `TRACEPARENT` to every Bash/PowerShell command.

## Tagging Telemetry

**Service name**:
```typescript
OTEL_SERVICE_NAME: "support-triage-agent",
OTEL_RESOURCE_ATTRIBUTES: "service.version=1.4.0,deployment.environment=production",
```

**End-user attribution** (requires percent-encoding):
```typescript
OTEL_RESOURCE_ATTRIBUTES: `enduser.id=${encodeURIComponent(userId)},tenant.id=${encodeURIComponent(tenantId)}`,
```

## Sensitive Data Control

By default, the SDK does not record the content that the agent reads or writes. Optional environment variables add content to exported data (opt-in required, see Monitoring reference for detailed list).

*This document is from the English version (Chinese URL returned 404)*