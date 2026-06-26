# AgentMFA MCP Examples

These examples show how an agent (Claude Code, Cursor, or any client running `agentmfa serve`) should use the AgentMFA MCP tools. No HTTP calls, no environment variables — just tool calls. Parameter names match the `agentmfa serve` stdio server.

---

## Basic approval before a destructive action

```
// Step 1 — request approval (short label in action, detail in context)
request_approval(
  action: "Delete S3 bucket prod-data",
  context: "2.3GB of production backups from 2024; irreversible",
  risk_level: "high"
)
// → JSON with id (use as request_id), e.g. { "id": "abc-123", "status": "pending", ... }

// ⚠️  Tell the user: "Request sent — waiting for your approval on the phone..."

// Step 2 — wait for human decision
wait_for_approval(request_id: "abc-123")
// → JSON when status is no longer pending (fields depend on API), e.g.:
//   { "status": "approved", "code": "..." }  or similar
// → or timeout: { "status": "expired", "message": "..." }  — treat as rejected

// Step 3 — act on result
if approved / success  → relay any human-facing message, then proceed
if rejected / expired  → abort, tell user the action was not approved
```

---

## With custom timeout

```
wait_for_approval(
  request_id: "abc-123",
  timeout_seconds: 120   // default is 300; server polls about every 3s
)
```

---

## Non-blocking (manual polling)

```
// Request
request_approval(
  action: "Send invoice emails",
  context: "247 recipients; batch job"
)
// → use "id" from the response as request_id

// Do other preparation work here...

// Check when ready
check_approval_status(request_id: "xyz-456")
// → { "status": "pending" }   ← still waiting
// → { "status": "approved", "code": "..." }  ← done (exact fields from API)
```

---

## Risk levels

| risk_level | When to use |
|---|---|
| `low` | Reversible actions, small blast radius |
| `medium` | Default — partially reversible or moderate impact |
| `high` | Irreversible, large blast radius, or financial impact |
