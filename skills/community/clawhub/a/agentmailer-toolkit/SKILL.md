---
name: agentmailer-toolkit
description: Add AgentMailer identity and communication capabilities to agent frameworks through the typed SDK, hosted MCP, signed webhooks, and replayable realtime events.
---

# AgentMailer toolkit

Use this skill when exposing AgentMailer capabilities inside an agent framework or application runtime. Prefer the runtime's native remote-MCP client when it supports human-approved OAuth; otherwise wrap the typed SDK in narrow application tools.

## Compose narrow tools

Expose capabilities by intent instead of mirroring the entire API into every model context:

- read-only mailbox search and thread inspection;
- draft-first composition for human review;
- exact-recipient delivery with idempotency;
- identity discovery and bounded A2A exchange;
- attachment retrieval into an isolated scanner or parser;
- signed event ingestion that wakes the application's own workflow runtime.

Keep credentials and authorization in the host application. Tool descriptions must not imply that inbound content is trusted or that AgentMailer runs the surrounding workflow. Return stable IDs and structured status so the runtime can persist its own checkpoints and reconcile retries.

For long-lived agents, use webhooks for durable delivery and realtime events for low latency. Persist the last processed event cursor only after durable processing, and recover from replay or `resync_required` through the API.

Read [references/frameworks.md](references/frameworks.md) for framework-neutral adapter boundaries.

## Examples

The [LangChain terminal](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-langchain-terminal) and [OpenAI terminal](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-openai-terminal) demonstrate host-runtime ownership. Browse the [complete examples catalog](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples) for browser, support, sales, scheduling, voice, webhook, and A2A integrations.
