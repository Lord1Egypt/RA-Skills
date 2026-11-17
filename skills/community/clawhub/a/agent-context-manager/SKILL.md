---
name: agent-context-manager
description: "Agent Context Manager: Manage reusable Agent Context documents -- structured. Use when an agent needs agent context manager, define a brand voice and style guide once and have every content agent follow it. store standard operating procedures so support and operations agents handle tasks consistently. keep product catalogs, pricing rules, and policy documents in one place that workflows reference at runtime. Discovery terms: agent context manager."
version: 1.0.1
homepage: https://www.agentpmt.com/marketplace/agent-context-manager
compatibility: "Requires AgentPMT internal handler access through the external marketplace API. Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/agent-context-manager"}}
---
# Agent Context Manager

## Freshness
Last updated: `2026-07-29`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Give your AI agents a single source of truth. Agent Context Manager lets you create, organize, version, and reuse the knowledge your agents and workflows rely on -- brand guidelines, standard operating procedures, product and pricing facts, tone-of-voice rules, and domain expertise -- so every agent acts on the same up-to-date information. Start from polished public templates, clone them into your private library, and edit once: every agent and workflow that references a document stays in sync automatically. Built-in version history shows exactly what changed, who changed it, and lets you roll back with confidence.

## Product Instructions
### Agent Context Manager

Agent Context Manager stores and maintains reusable **Agent Context documents** -- the persistent knowledge your AI agents and workflows draw on every time they run (brand guidelines, SOPs, product facts, tone rules, domain expertise). Maintain a document once and every agent or workflow that references it stays in sync.

#### Document fields
- **title** (required) -- short, descriptive name.
- **summary** (optional) -- one-line overview shown in lists and pickers.
- **body** (required) -- the full knowledge the agent should load. Markdown is supported.
- **tags** (optional) -- keywords for search and organization.
- **scope** -- `private` (yours to create and edit) or `public_template` (admin-managed, available for anyone to clone).

#### Actions
- **list** -- list and search readable documents. Use `scope: private` (default), `public_template`, or `all`. Supports `query`, `include_archived`, and `limit`.
- **fetch** -- retrieve one document's full body by `context_document_id`.
- **create** -- create a private document (title and body required). Creating a `public_template` requires admin access.
- **update** -- edit title, summary, body, or tags on a document you own.
- **archive** -- retire a document so it can no longer be attached, while keeping its history.
- **clone_template** -- copy a public template into your private library so you can customize it. The clone tracks the template it came from.
- **versions** -- review retained revisions (who changed what and when) so you can compare and roll back.

#### Permissions
- Any authenticated user can run every action.
- You can only modify your own private documents.
- Only admins create or edit public templates.

#### Best practices
- Keep each document focused on one topic (one for brand voice, one for return policy) so agents load only what they need.
- Start from a public template when one fits, then clone and tailor it.
- Edit the shared document rather than duplicating knowledge across workflows -- one update propagates everywhere.
- Use clear titles and tags so documents are easy to find and attach.
- Rely on version history before large edits; you can always roll back.

## When To Use
- Use this skill for `Agent Context Manager` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: agent context manager, define a brand voice and style guide once and have every content agent follow it. store standard operating procedures so support and operations agents handle tasks consistently. keep product catalogs, pricing rules, and policy documents in one place that workflows reference at runtime. onboard a new agent instantly by attaching a curated set of context documents instead of rewriting prompts. roll out a company wide change by editing a single document instead of updating every workflow that uses it. clone a vetted public template    such as a customer support playbook or editorial style guide    and tailor it to your business. audit and roll back changes to mission critical instructions using full version history., archive, context document id, expected revision, clone template.
- Supported action names: `archive`, `clone_template`, `create`, `fetch`, `get_instructions`, `list`, `request_unlock`, `restore_version`, `update`, `version_detail`, `versions`.

## Use Cases
- Define a brand voice and style guide once and have every content agent follow it. Store standard operating procedures so support and operations agents handle tasks consistently. Keep product catalogs
- pricing rules
- and policy documents in one place that workflows reference at runtime. Onboard a new agent instantly by attaching a curated set of context documents instead of rewriting prompts. Roll out a company-wide change by editing a single document instead of updating every workflow that uses it. Clone a vetted public template -- such as a customer-support playbook or editorial style guide -- and tailor it to your business. Audit and roll back changes to mission-critical instructions using full version history.

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `11`.
x402 availability: not enabled for this product.

- `archive` (action slug: `archive`): Archive an Agent Context document. Price: `0` credits. Parameters: `context_document_id`, `expected_revision`.
- `clone_template` (action slug: `clone-template`): Clone a public Agent Context template into private context. Price: `0` credits. Parameters: `context_document_id`.
- `create` (action slug: `create`): Create an Agent Context document. Price: `0` credits. Parameters: `agent_edit_approval_required`, `body`, `document_scope`, `summary`, `tags`, `title`.
- `fetch` (action slug: `fetch`): Fetch one readable Agent Context document. Price: `0` credits. Parameters: `context_document_id`.
- `get_instructions` (action slug: `get-instructions`): Return Agent Context Manager usage guidance. Price: `0` credits. Parameters: none.
- `list` (action slug: `list`): List readable Agent Context documents. Price: `0` credits. Parameters: `include_archived`, `limit`, `query`, `scope`.
- `request_unlock` (action slug: `request-unlock`): Request a temporary 30-minute edit unlock for a locked Agent Context document. Price: `0` credits. Parameters: `context_document_id`.
- `restore_version` (action slug: `restore-version`): Restore a retained Agent Context version using CAS. Price: `0` credits. Parameters: `context_document_id`, `expected_revision`, `version_id`.
- `update` (action slug: `update`): Update editable fields on an Agent Context document. Price: `0` credits. Parameters: `agent_edit_approval_required`, `body`, `context_document_id`, `expected_revision`, `summary`, `tags`, `title`.
- `version_detail` (action slug: `version-detail`): Fetch one retained Agent Context version detail with its snapshot. Price: `0` credits. Parameters: `context_document_id`, `version_id`.
- `versions` (action slug: `versions`): List retained versions for a readable Agent Context document. Price: `0` credits. Parameters: `context_document_id`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "agent-context-manager"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "agent-context-manager"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "agent-context-manager"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "agent-context-manager"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "agent-context-manager"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "agent-context-manager"
  }
}
```

## Call This Tool
Product slug: `agent-context-manager`

Marketplace page: https://www.agentpmt.com/marketplace/agent-context-manager

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
    "name": "Agent-Context-Manager",
    "arguments": {
      "action": "archive",
      "context_document_id": null,
      "expected_revision": null
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "agent-context-manager",
  "parameters": {
    "action": "archive",
    "context_document_id": null,
    "expected_revision": null
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `archive` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/agent-context-manager
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
