---
name: agentmailer-inbox
description: Create, inspect, update, or deactivate a human-approved AgentMailer identity with a unique @agentmailer.ai address through MCP.
---

# AgentMailer Inbox

Use this skill when a user wants to create an agent identity or manage the inbox and unique `handle@agentmailer.ai` address attached to an existing identity.

## Workflow

1. Call `auth_me`. Inbox creation requires a trusted, human-approved identity with `inboxes:create`.
2. Call `list_inboxes` before creating a new inbox when an existing identity might satisfy the request.
3. For creation, clarify the intended display name and requested address only when they materially affect the result. Omitting the username lets AgentMailer generate a deterministic address.
4. Use a stable, task-specific `idempotencyKey` for `create_inbox` so a retry cannot create a duplicate.
5. Verify that the returned address uses `@agentmailer.ai`, then return the identity's unique handle, inbox ID, address, display name, and relevant metadata.
6. Use `update_inbox` for display name, metadata, or client correlation changes.

If `auth_me` reports an unverified identity or creation returns `human_approval_required`, stop and follow the signup sequence at `https://api.agentmailer.ai/llms.txt`. Do not substitute another domain or bypass human approval.

`delete_inbox` deactivates the mailbox and reserves its handle. Before calling it, identify the exact inbox, explain that effect, and obtain explicit confirmation in the current conversation.

Read [references/inbox-tools.md](references/inbox-tools.md) when choosing tool inputs or handling permissions.

## Examples

Start with the [AgentMailer quickstart](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-quickstart) for inbox discovery and the [human-approved signup example](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples/agentmailer-human-approved-signup) for the first-time identity ceremony. Browse the [complete examples catalog](https://github.com/aadi-labs/agentmailer-plugins/tree/main/examples) for inbox-backed application workflows.
