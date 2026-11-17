---
name: agentpmt-audit-logs
description: "AgentPMT Audit Logs: Look back over this account's own activity, read-only. Search and read past chat sessions, pull a full chat transcript together with the tool calls that happened inside it, list tool-call history filtered. Use when an agent needs agentpmt audit logs, summarize what your agents did this week, review a past chat conversation and the tool calls inside it, audit tool call history by tool, status, get chat review, agent group id, scope through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/agentpmt-audit-logs
compatibility: "Requires AgentPMT internal handler access through the external marketplace API. Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/agentpmt-audit-logs"}}
---
# AgentPMT Audit Logs

## Freshness
Last updated: `2026-07-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Give your agents a memory of everything they have done. Pull up past chat conversations, review every tool your agents have run, and look back over finished and scheduled workflow runs, all on demand and in plain language. Ask "what did my agents work on this weekend?" or "why did that workflow fail?" and get a clear, sourced answer drawn straight from your own activity history. It is the easiest way to keep oversight of autonomous agents, debug a run that went sideways, put together an end-of-week summary, and keep a trustworthy record of what was done and when.

## When To Use
- Use this skill for `AgentPMT Audit Logs` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: agentpmt audit logs, summarize what your agents did this week, review a past chat conversation and the tool calls inside it, audit tool call history by tool, status, get chat review, agent group id, scope.
- Supported action names: `get_chat_review`, `get_instructions`, `get_workflow_run`, `get_workflow_schedule`, `list_agent_groups`, `list_chat_sessions`, `list_tool_calls`, `list_workflow_runs`, `list_workflow_schedules`.

## Use Cases
- Summarize what your agents did this week
- Review a past chat conversation and the tool calls inside it
- Audit tool-call history by tool
- status
- and date
- Investigate why a workflow run failed
- Check recent and upcoming scheduled workflow runs
- Build an activity report for oversight
- Trace a single tool's usage history
- Keep a read-only audit trail of agent actions

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `9`.
x402 availability: not enabled for this product.

- `get_chat_review` (action slug: `get-chat-review`): Fetch a bounded chat transcript page and correlated tool calls. Parameters: `activity_limit`, `activity_offset`, `agent_group_id`, `message_limit`, `message_offset_from_end`, `scope`, `session_id`.
- `get_instructions` (action slug: `get-instructions`): Explain how to read chat history, tool calls, workflow runs, and scheduled workflows. Parameters: none.
- `get_workflow_run` (action slug: `get-workflow-run`): Fetch one prior workflow run result by ID. Parameters: `agent_group_id`, `run_id`, `scope`.
- `get_workflow_schedule` (action slug: `get-workflow-schedule`): Fetch one scheduled workflow by ID. Parameters: `agent_group_id`, `schedule_id`, `scope`.
- `list_agent_groups` (action slug: `list-agent-groups`): List the agent groups this user can read. Parameters: `limit`, `offset`.
- `list_chat_sessions` (action slug: `list-chat-sessions`): List chat sessions for the current or selected agent group. Parameters: `agent_group_id`, `from_date`, `limit`, `offset`, `query`, `scope`, `status`, `to_date`.
- `list_tool_calls` (action slug: `list-tool-calls`): List safe, read-only tool call activity for authorized agent groups. Parameters: `action_name`, `agent_group_id`, `from_date`, `limit`, `offset`, `product_id`, `response_status`, `scope`, plus 2 more.
- `list_workflow_runs` (action slug: `list-workflow-runs`): List prior workflow run results for authorized agent groups. Parameters: `agent_group_id`, `from_date`, `limit`, `offset`, `schedule_id`, `scope`, `status`, `to_date`, plus 2 more.
- `list_workflow_schedules` (action slug: `list-workflow-schedules`): List scheduled workflows for authorized agent groups. Parameters: `agent_group_id`, `due_from`, `due_to`, `execution_mode`, `limit`, `offset`, `query`, `scope`, plus 2 more.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "agentpmt-audit-logs"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "agentpmt-audit-logs"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "agentpmt-audit-logs"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "agentpmt-audit-logs"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "agentpmt-audit-logs"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "agentpmt-audit-logs"
  }
}
```

## Call This Tool
Product slug: `agentpmt-audit-logs`

Marketplace page: https://www.agentpmt.com/marketplace/agentpmt-audit-logs

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Audit-Logs",
    "arguments": {
      "action": "get_chat_review",
      "activity_limit": 100,
      "activity_offset": 0,
      "agent_group_id": "example agent group id",
      "message_limit": 100,
      "message_offset_from_end": 0,
      "scope": "current_agent_group",
      "session_id": "example session id"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "agentpmt-audit-logs",
  "parameters": {
    "action": "get_chat_review",
    "activity_limit": 100,
    "activity_offset": 0,
    "agent_group_id": "example agent group id",
    "message_limit": 100,
    "message_offset_from_end": 0,
    "scope": "current_agent_group",
    "session_id": "example session id"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `get_chat_review` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/agentpmt-audit-logs
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
