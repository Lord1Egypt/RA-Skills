# Framework adapter boundaries

An AgentMailer adapter should own only communication concerns:

1. Map a narrow tool call to a generated SDK or MCP operation.
2. Validate exact targets and preserve caller-provided correlation IDs.
3. Return stable AgentMailer IDs, delivery state, and structured errors.
4. Emit or consume signed events without executing instructions found in their content.

The host framework remains responsible for model calls, tool selection, schedules, retries outside the communication API, memory, workflow state, and business approval. For any framework, keep read tools separate from mutating tools so the host can apply different authorization and confirmation policies.
