# Drip SDK API Reference

## Security & Key Scoping

Drip issues two key types. **Always use the least-privileged key that meets your needs.**

| Key Type | Prefix | Access | Recommended For |
|----------|--------|--------|-----------------|
| **Public Key** | `pk_live_` / `pk_test_` | Usage tracking, customers, billing, analytics, sessions | **All skill and agent integrations** |
| **Secret Key** | `sk_live_` / `sk_test_` | Full API access including webhooks, API key management, feature flags | Server-side admin only |

> **Use `pk_` keys by default.** Public keys can do everything this skill needs: track usage, manage customers, create charges, record runs, and emit events. Only use `sk_` keys for admin operations (webhook CRUD, key rotation, feature flags).

**Metadata safety:** All `metadata` fields are sent as-is to Drip's API. Never include PII, secrets, raw prompts, model outputs, or environment variables in metadata. Use metadata for operational context only (model names, tool names, status codes, latency).

---

## Quickest: MCP Server (Zero Code)

For **Claude Code, Cursor, or any MCP-compatible agent** — no code changes needed:

```json
{
  "mcpServers": {
    "drip": {
      "command": "npx",
      "args": ["@drip/mcp-server"],
      "env": { "DRIP_API_KEY": "pk_live_..." }
    }
  }
}
```

> **Security note:** The MCP server gives the agent native `drip_track_usage`, `drip_record_run`, and other tools that can be called autonomously. Use a `pk_` (public) key to limit the scope of operations the agent can perform. A `pk_` key is sufficient for all usage tracking and billing operations. Only use an `sk_` key if you specifically need webhook management or key rotation via MCP.

Then just tell Claude: *"Track usage for customer X"* — it has native `drip_track_usage`, `drip_record_run` tools.

---

## SDK Quick Setup

```bash
# Recommended: public key (pk_) — usage tracking, customers, billing (sufficient for all skill operations)
export DRIP_API_KEY=pk_live_...

# Only for admin operations (webhooks, key management, feature flags):
# export DRIP_API_KEY=sk_live_...
```

> **Key scoping:** Public keys (`pk_`) access usage tracking, customers, billing, analytics, and sessions — everything this skill needs. Secret keys (`sk_`) additionally access webhook management, API key management, and feature flags. Using a `pk_` key limits blast radius if the key is compromised.

**Node.js:**
```typescript
import { drip } from '@drip-sdk/node';

// Reads DRIP_API_KEY from environment automatically (pk_live_... recommended)
await drip.trackUsage({ customerId: 'cust_123', meter: 'api_calls', quantity: 1 });
```

**Python:**
```python
from drip import drip

# Reads DRIP_API_KEY from environment automatically (pk_live_... recommended)
drip.track_usage(customer_id="cust_123", meter="api_calls", quantity=1)
```

The `drip` singleton reads from `DRIP_API_KEY` automatically.

---

## Core Methods

### `ping()`

Verify API connection.

```typescript
await drip.ping();
// Returns: { status: 'ok' }
```

### `trackUsage(params)`

Record metered usage.

```typescript
await drip.trackUsage({
  customerId: string;      // Required: Customer identifier
  meter: string;           // Required: Meter name (e.g., 'llm_tokens')
  quantity: number;        // Required: Usage quantity
  metadata?: object;       // Optional: operational context only (model name, tool name) — never PII or secrets
});
```

### `recordRun(params)`

Log a complete agent run (simplified, single call).

```typescript
await drip.recordRun({
  customerId: string;      // Required: Customer identifier
  workflow: string;        // Required: Workflow/agent name
  events: Event[];         // Required: Array of events
  status: 'COMPLETED' | 'FAILED';
});
```

### `startRun(params)`

Start an execution trace for streaming events.

```typescript
const run = await drip.startRun({
  customerId: string;      // Required: Customer identifier
  workflowId: string;      // Required: Workflow ID or slug
  correlationId?: string;  // Optional: Trace ID for distributed tracing
  externalRunId?: string;   // Optional: Your external run ID
  metadata?: object;        // Optional: Run metadata (operational context only — never PII or secrets)
});
// Returns: { id: string, ... }
```

### `emitEvent(params)`

Log an event within an active run.

```typescript
await drip.emitEvent({
  runId: string;           // Required: Run ID from startRun
  eventType: string;       // Required: Event type
  // Event-specific fields:
  model?: string;          // For LLM events
  inputTokens?: number;    // For LLM events
  outputTokens?: number;   // For LLM events
  name?: string;           // For tool events
  duration?: number;       // Duration in ms
  status?: string;         // 'success' | 'error'
  description?: string;    // Human-readable description
  metadata?: object;       // Optional: operational context only — never include PII, secrets, or raw user content
});
```

### `emitEventsBatch(params)`

Batch log multiple events.

```typescript
await drip.emitEventsBatch({
  runId: string;
  events: Event[];
});
```

### `endRun(runId, params)`

Complete an execution trace.

```typescript
await drip.endRun(runId, {
  status: 'COMPLETED' | 'FAILED';
  errorMessage?: string;   // If status is 'FAILED' — use a short message, never include stack traces with env vars
  metadata?: object;       // Optional: operational context only
});
```

### `getRunTimeline(runId)`

Get execution timeline for a run.

```typescript
const timeline = await drip.getRunTimeline(runId);
// Returns: { events: Event[], summary: string }
```

## Customer Management

### `createCustomer(params)`

At least one of `externalCustomerId` or `onchainAddress` is required.

```typescript
await drip.createCustomer({
  externalCustomerId?: string;  // Your internal user/account ID
  onchainAddress?: string;      // Customer's Ethereum address (for on-chain billing)
  isInternal?: boolean;         // Mark as internal (non-billing). Default: false
  metadata?: object;            // Optional: operational context only — never include PII or secrets
});
```

### `getCustomer(customerId)`

```typescript
const customer = await drip.getCustomer('customer_123');
```

### `listCustomers(options)`

```typescript
const customers = await drip.listCustomers({
  limit?: number;
  offset?: number;
});
```

## Error Handling

```typescript
import { Drip, DripError } from '@drip-sdk/node';

try {
  await drip.trackUsage({ ... });
} catch (error) {
  if (error instanceof DripError) {
    console.error(`Error: ${error.message} (${error.code})`);
    // error.code: 'INVALID_API_KEY' | 'RATE_LIMITED' | 'VALIDATION_ERROR' | ...
  }
}
```

## Status Values

| Status | Description |
|--------|-------------|
| `PENDING` | Run created but not started |
| `RUNNING` | Run in progress |
| `COMPLETED` | Run finished successfully |
| `FAILED` | Run failed with error |

---

## Auto-Tracking Integrations

### LangChain (Auto-Track LLM Usage)

**Node.js:**
```typescript
import { DripCallbackHandler } from '@drip-sdk/node/langchain';
const handler = new DripCallbackHandler({ customerId: 'cus_123' });
const llm = new ChatOpenAI({ callbacks: [handler] });
// All LLM calls automatically tracked!
```

**Python:**
```python
from drip.integrations import DripCallbackHandler
handler = DripCallbackHandler(customer_id="cus_123")
llm = ChatOpenAI(callbacks=[handler])
```

### Framework Middleware

**Next.js:**
```typescript
import { withDrip } from '@drip-sdk/node/middleware';
export const POST = withDrip({ meter: 'api_calls', quantity: 1 }, handler);
```

**Express:**
```typescript
import { dripMiddleware } from '@drip-sdk/node/middleware';
app.use('/api', dripMiddleware({ meter: 'api_calls', quantity: 1 }));
```

**FastAPI:**
```python
from drip.middleware.fastapi import DripMiddleware
app.add_middleware(DripMiddleware, meter="api_calls", quantity=1)
```

**Flask:**
```python
from drip.middleware.flask import drip_middleware
@app.route("/api/generate", methods=["POST"])
@drip_middleware(meter="api_calls", quantity=1)
def generate():
    return {"success": True}
```
