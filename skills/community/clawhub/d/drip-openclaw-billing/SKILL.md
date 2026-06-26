---
name: drip-openclaw-billing
description: Add usage metering and billing telemetry to OpenClaw agents using Drip. Use when you need per-run cost attribution, tool-call usage tracking, and customer-level billing visibility.
license: MIT
compatibility: OpenClaw runtime + Drip API. Supports Node.js and Python integrations.
credentials:
  primary: DRIP_API_KEY
  alternate: OPENCLAW_IDENTITY_TOKEN
requiredEnvVars:
  - name: DRIP_API_KEY
    description: Drip API key for /v1 telemetry APIs (recommended default path).
    required: false
  - name: OPENCLAW_IDENTITY_TOKEN
    description: OpenClaw identity token for /openclaw endpoints.
    required: false
  - name: DRIP_BASE_URL
    description: Optional API base URL (default https://api.drippay.dev).
    required: false
  - name: DRIP_WORKFLOW_ID
    description: Workflow ID for run lifecycle telemetry.
    required: false
metadata:
  author: lucas-309
  publisher: lucas-309
  version: "1.1.1"
  securityModel: "least-privilege telemetry keys, sanitized metadata, no raw prompt/output/PII"
---

# Drip OpenClaw Billing

Instrument OpenClaw agents with Drip for **run timelines**, **tool-call usage metering**, and **customer-level billing attribution**.

## Install (copy/paste)

```bash
clawhub install drip-openclaw-billing
```

> Use slug only in CLI (`drip-openclaw-billing`), not `owner/slug`.

## What this gives you

- Per-run billing traceability (`start_run` → events → usage → `end_run`)
- Metered usage by unit (tokens, tool calls, API calls, compute time)
- Customer/project-level cost and usage visibility in Drip
- Idempotent writes for retry-safe telemetry

## Integration paths

1. **Recommended**: `DRIP_API_KEY` with `/v1/*` endpoints for full billing + telemetry control.
2. **Lightweight**: `OPENCLAW_IDENTITY_TOKEN` with `/openclaw/*` endpoints.

## Security rules

- Use least-privilege runtime keys (prefer scoped telemetry key).
- Never send raw prompts, raw model outputs, credentials, or PII.
- Send sanitized metadata only (hash content fields like `queryHash` when needed).
- Emit stable idempotency keys for all writes.
- Validate payload schemas in staging before production rollout.

## Quickstart (Node.js)

```ts
import { OpenClawBilling } from '@drip-sdk/node/openclaw';

const billing = new OpenClawBilling({
  apiKey: process.env.DRIP_API_KEY,
  customerId: 'cus_123',
  workflowId: process.env.DRIP_WORKFLOW_ID ?? 'wf_openclaw',
});

await billing.withRun({ externalRunId: 'openclaw_req_456' }, async ({ runId }) => {
  await billing.withToolCall({ runId, provider: 'brave', endpoint: '/res/v1/web/search' }, async () => {
    // tool execution
  });
});
```

## Quickstart (Python)

```py
from drip import Drip
import os

client = Drip(api_key=os.environ['DRIP_API_KEY'])
run = client.start_run(customer_id='cus_123', workflow_id='wf_openclaw', external_run_id='openclaw_req_456')
client.emit_event(run_id=run.id, event_type='tool.call', quantity=1, metadata={'provider': 'brave'})
client.track_usage(customer_id='cus_123', meter='brave_api_calls', quantity=1, metadata={'runId': run.id})
client.end_run(run.id, status='COMPLETED')
```

## Load detailed API docs

See `references/API.md` for:
- endpoint shapes
- run/event/usage lifecycle
- pricing units and rate-limit notes
- error handling patterns
