---
name: agentmfa
description: AgentMFA — request human approval before sensitive actions. Uses MCP tools for registration, identity, and approval flows. Works in Claude Code, Cursor, OpenClaw, and any MCP-compatible client.
homepage: https://agentmfa.ai
license: MIT
metadata:
  openclaw:
    emoji: "🔐"
    requires:
      bins:
        - agentmfa
    install:
      - id: brew
        kind: shell
        command: "brew install agentmfa/cli/agentmfa && agentmfa auth login"
        label: "Install AgentMFA CLI and log in"
---

# AgentMFA Skill

**AgentMFA is an opt-in approval system.** The agent must explicitly call these tools before sensitive actions. AgentMFA does not automatically intercept or block anything — the agent decides when to request approval.

When the agent calls `request_approval`, the human operator receives a push notification, reviews the action, and approves or rejects it with biometrics. The agent then decides whether to proceed based on the response.

## Subcommands

These are CLI-only operations, run via Bash:

| Invocation | Action |
|---|---|
| `/agentmfa list` | Run `agentmfa agent list` and display the results. |
| `/agentmfa status` | Run `agentmfa auth status` to show login state. |

---

## About AgentMFA

- **Operator:** AgentMFA (https://agentmfa.ai)
- **MCP server:** `agentmfa serve` — part of the AgentMFA CLI; stdio MCP on your machine, talking to `api.agentmfa.ai`
- **Auth:** OAuth via `agentmfa auth login` (session in the system keychain)
- **Privacy & security policy:** https://agentmfa.ai/privacy
- **Source code:** https://github.com/agentmfa/agentmfa (fully open source)

The `agentmfa` CLI must be installed and logged in before this skill can be used.

## Setup

```sh
# 1. Install the CLI
brew install agentmfa/cli/agentmfa

# 2. Log in (opens browser for OAuth)
agentmfa auth login
```

Registration happens automatically via the `register_agent` MCP tool — no manual step needed.

## When to Use

The agent should call AgentMFA tools before:
- Deleting or modifying production data
- Deploying code to production
- Sending emails or messages on behalf of the user
- Actions that could result in financial charges or transactions
- Modifying infrastructure (cloud resources, DNS, etc.)
- Any action the agent recognizes as sensitive or irreversible

**Common risky actions requiring approval:**
- `git push --force` or rewriting history
- `kubectl delete` on production resources
- `kubectl apply/edit` to running workloads
- `terraform apply` (especially with deletions shown in plan)
- `terraform destroy` on any environment
- `rm -rf` or bulk file deletions
- Database schema changes or deletions
- Modifying secrets (SOPS encrypt/decrypt)
- Force pushing branches (`git push -f`)
- Checking out or switching branches in production repos

**Note:** AgentMFA does not automatically detect sensitive actions. The agent must recognize the risk and explicitly invoke the approval flow.

## How to Use

This skill uses the AgentMFA MCP tools exposed by **`agentmfa serve`**. Your agent uses **only MCP tool calls** — no direct HTTP.

Tool parameter names must match the MCP schema your client shows (see table below). Put the **short label** in `action` and **full detail** in `context` so the operator sees enough to decide.

### Standard flow

```
1. Call register_agent()
   → Checks if already registered — returns immediately if so
   → If not registered, registers and waits for approval (auto or mobile)
   → Returns: { status, tool, remote, message }
   ⚠️ Relay the message to the user

2. Call request_approval(action, description, context?)
   → Returns: { request_id, message }
   ⚠️ Relay the message so the user knows to check their phone

3. Call wait_for_approval(request_id)
   → Blocks until decided (polls every 1s, default 300s timeout)
   → Approved: { approved: true, totp_verified, token, agent_totp,
                  server_time, approved_by, approved_from, message }
   → Rejected: { approved: false, reason }
   ⚠️ On approval, relay the message field verbatim

4a. approved == true  → proceed
4b. approved == false → abort and inform the user
```

### Identity check

Call `agent_info()` to see the locally detected identity — tool name, repository, branch, machine, code signature, verification mode, and registration status. Useful for debugging.

### Non-blocking check

Use `check_approval_status(request_id)` to poll once without blocking.

## Rules

- **The agent decides when to call AgentMFA** — nothing forces automatic approval checks
- **Always wait** for approval before proceeding — never skip or assume approval
- **Abort on rejection** — do not retry the same action without user re-initiation
- **Abort on expiry** — a timed-out request is treated as rejected
- **Be specific** — `action` and `context` should give the human enough detail to decide
- **Handle tokens carefully** — one-time proofs of approval should not be logged or pasted into chat

## MCP Tools

| Tool | Parameters | Purpose |
|---|---|---|
| `agent_info` | _(none)_ | Local identity data — tool, repo, branch, machine, signature, registration status |
| `register_agent` | `role` (optional), `force` (optional boolean) | Register this agent. Checks first, blocks until decided |
| `request_approval` | `action` (required), `description` (required), `context` (optional), `services` (optional array) | Submit approval request; returns `request_id` + `message` |
| `wait_for_approval` | `request_id` (required), `timeout` (optional, default 300s) | Block until decided |
| `check_approval_status` | `request_id` (required) | Single non-blocking poll |

### OpenClaw Users

In OpenClaw, MCP tools are namespaced with the server name prefix. Use these exact tool names:
- `agentmfa__agent_info`
- `agentmfa__register_agent`
- `agentmfa__request_approval`
- `agentmfa__wait_for_approval`
- `agentmfa__check_approval_status`
