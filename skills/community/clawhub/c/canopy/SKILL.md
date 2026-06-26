---
name: canopy
description: |
  Canopy treasury wallet for AI agents — make policy-gated USD payments on-chain (Base), auto-pay paywalled APIs (x402 / MPP), and discover paid services. Every payment passes through the agent's policy: spend cap, recipient/service allowlist, and approval threshold. Payments above the threshold return pending_approval and wait for a human; payments outside the cap or allowlist return denied. Install only if your agent needs to spend org funds. Connect with the least-privileged agent + policy available, verify recipient and amount before each canopy_pay, and never auto-approve on the user's behalf.
  Requires a Canopy account at https://www.trycanopy.ai. After install, configure the canopy MCP server with your CANOPY_API_KEY and CANOPY_AGENT_ID from the dashboard.
metadata:
  author: canopy
  version: "1.0.0"
  homepage: "https://www.trycanopy.ai"
  openclaw:
    requires:
      env:
        - CANOPY_API_KEY
        - CANOPY_AGENT_ID
---

# Canopy

Canopy is a treasury wallet + per-agent policy gate. An org funds a treasury once, attaches a policy to each agent (spend cap, allowlist, approval threshold), and gives the agent the `canopy_*` MCP tools below. Canopy enforces the policy on every payment.

## Setup

After installing this skill, register the Canopy MCP server with OpenClaw. Replace the placeholders with your own values from the [Canopy dashboard](https://www.trycanopy.ai/dashboard/agents) (Connect agent → Credentials):

```bash
openclaw mcp set canopy '{
  "url": "https://mcp.trycanopy.ai/mcp",
  "transport": "streamable-http",
  "headers": {
    "Authorization": "Bearer YOUR_CANOPY_API_KEY",
    "X-Canopy-Agent-Id": "YOUR_CANOPY_AGENT_ID"
  }
}'
```

Or edit `openclaw.json` directly:

```json
{
  "mcpServers": {
    "canopy": {
      "url": "https://mcp.trycanopy.ai/mcp",
      "transport": "streamable-http",
      "headers": {
        "Authorization": "Bearer YOUR_CANOPY_API_KEY",
        "X-Canopy-Agent-Id": "YOUR_CANOPY_AGENT_ID"
      }
    }
  }
}
```

Restart OpenClaw. The `canopy_*` tools become available immediately.

Verify with `canopy_ping` — it returns the resolved agent + org and a latency number.

## Triggers

Use Canopy when the user mentions:

- "pay", "transfer", "send $X to <address>"
- "approve" / "deny" a pending payment
- "budget", "spend cap", "remaining budget"
- "paid API", "x402", "402 paywall"
- "find a paid service for …", "discover services"
- "agent wallet", "treasury"

## Available tools

| Tool | Purpose |
|------|---------|
| `canopy_pay` | Send a USD payment to an address. Subject to policy. Returns one of three outcomes (see below). |
| `canopy_preview` | Dry-run policy evaluation without signing or charging. Same shape as `canopy_pay` plus `dryRun: true`. |
| `canopy_check_url` | Probe an x402 / MPP URL and return the parsed offer plus a policy verdict. Cached 60s per (org, url). |
| `canopy_discover_services` | List paid services the agent can call. Filter by `category` and `query`. |
| `canopy_get_approval_status` | Poll the current state of a pending approval. |
| `canopy_wait_for_approval` | Block until an approval is decided, max 60s. Use polling for longer waits. |
| `canopy_approve` | Mark a pending approval as approved. Use only when the user has explicitly said yes in chat. |
| `canopy_deny` | Mark a pending approval as denied. Use only when the user has explicitly said no in chat. |
| `canopy_get_budget` | Cap snapshot for the current rolling period (`capUsd`, `spentUsd`, `remainingUsd`, `periodResetsAt`). |
| `canopy_ping` | Verify the API key + agent. Returns agent and org details plus latency. |

## Outcome model — `canopy_pay`, `canopy_preview`, `canopy_check_url`

These tools never throw on policy. They always return a structured value with one of three `status` values:

### `allowed`
Payment went through (or would go through, for `_preview` / `_check_url`).
Surface `txHash` (Base block-explorer hash) and `costUsd` to the user.

### `pending_approval`
Payment exceeded the agent's approval threshold. Fields you should use:
- `approvalId` — pass to `canopy_approve` / `canopy_deny` / `canopy_wait_for_approval` / `canopy_get_approval_status`.
- `recipientName`, `recipientAddress`, `amountUsd`, `agentName`, `expiresAt` — render these to the user when asking.
- `chatApprovalEnabled` — if `false`, calling `canopy_approve` / `canopy_deny` will fail. Tell the user to approve in the dashboard, optionally `canopy_wait_for_approval` to block.

If `chatApprovalEnabled === true`: ask the user "Approve $X to RecipientName?" then call `canopy_approve(approval_id)` or `canopy_deny(approval_id)` based on their reply.

### `denied`
Policy blocked it (cap exceeded, recipient/service not on allowlist, etc.). Surface the `reason` to the user. Do NOT retry with smaller amounts to evade the cap.

HTTP and network failures still throw normally — wrap calls in try/except as you would any tool call.

## Safety rules

- **Always show the user `recipientName` + `amountUsd` before calling `canopy_approve`.** Approvals exist precisely so a human sees the transaction details before money moves. Echoing them back confirms intent.
- **Default to `canopy_preview` when the amount is dynamic or untrusted.** Same shape as `canopy_pay`, no funds move. Use the verdict to decide whether to proceed.
- **Never auto-approve.** `canopy_approve` and `canopy_deny` are for handling explicit user replies in chat, not for the LLM to bypass the human-in-the-loop.
- **Don't chunk a denied payment into smaller payments.** If a `denied` outcome cites the spend cap, surface the cap to the user; suggest they raise it in the dashboard rather than working around it.
- **Don't reference `txHash` until `status === "allowed"`.** It's null in other outcomes.
- **Don't tight-loop `canopy_get_approval_status`.** Use `canopy_wait_for_approval` (60s max) or accept that the dashboard owns the decision.

## Quick examples

**User:** "Pay 50 cents to 0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97"
→ `canopy_pay({ to: "0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97", amountUsd: 0.50 })`. Surface `txHash` if `allowed`.

**User:** "How much do I have left to spend today?"
→ `canopy_get_budget()`. Render `remainingUsd` and `periodResetsAt`.

**User:** "Find paid orderbook data feeds"
→ `canopy_discover_services({ category: "data", query: "orderbook" })`. List services with `policyAllowed: true` first; mention any with `policyAllowed: false` only if the user asks why.

**User:** "Is paying https://feed.example/depth allowed?"
→ `canopy_check_url({ url: "https://feed.example/depth" })`. Return the verdict + amount + recipient name.

**User (after a previous `pending_approval`):** "Yes, approve it"
→ Confirm the recipient and amount you previously surfaced. Then `canopy_approve({ approval_id: <approvalId> })`.

## Resources

- [Canopy dashboard](https://www.trycanopy.ai)
- [MCP tools reference](https://www.trycanopy.ai/documentation/reference/mcp-tools)
- [Payment outcomes](https://www.trycanopy.ai/documentation/concepts/payment-outcomes)
- [Policies](https://www.trycanopy.ai/documentation/concepts/policies)
- [x402 protocol](https://www.trycanopy.ai/documentation/concepts/x402)
- [Connect MCP hosts](https://www.trycanopy.ai/documentation/connect/mcp)
