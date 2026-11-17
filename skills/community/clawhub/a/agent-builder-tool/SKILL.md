---
name: agent-builder-tool
description: "Agent Builder Tool: Create, configure, publish, and manage custom AI agents end to end. create_new drafts a private agent, optionally as a remix of any agent you can view. Use when an agent needs agent builder tool, build a custom ai agent without writing code, turn a job description into a working ai agent, equip an agent with crm inbox calendar and messaging tools, attach multi step workflows to an agent, add product, agent id, product id through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/agent-builder-tool
compatibility: "Requires AgentPMT internal handler access through the external marketplace API. Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/agent-builder-tool"}}
---
# Agent Builder Tool

## Freshness
Last updated: `2026-08-01`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Build your own AI agent in a conversation. Describe the job you want done and this AI agent builder creates the agent, gives it the tools and workflows it needs, writes its operating instructions, and puts it live under its own name and link. Start from a blank agent or branch off one that already works, then keep shaping it in plain language: connect a CRM, an inbox, a calendar, a phone line, research and data tools, or an entire multi step workflow, and attach your own context documents so it answers with your pricing, your policies, and your voice instead of generic advice. Preview the agent in a live chat, publish it when it is ready, hand it to your team, and spin up new agents for other roles while the original keeps running untouched. No code, no framework, and no prompt engineering background required. If you can explain the job to a new hire, you can build the AI agent that does it.

## Product Instructions
Agent Builder Tool creates and manages custom AI agents: lifecycle, composition (tools and workflows), context documents, and showcase chat previews.

#### Response field allowlist (read this first)
Responses use a strict allowlist. `system_prompt` and `chat_model` are writable but are **never returned** by any action, including `fetch_existing`. Keep your own copy of a system prompt if you need to read it back or edit it incrementally.

#### Actions

##### create_new
Create a private draft agent.
- `name` (required; omitting it returns `AGENT_CREATE_NAME_REQUIRED`)
- `description`, `chat_model`, `context_document_ids`
- `remixed_from_agent_id`, `remixed_from_agent_name` to create the draft as a remix of a source you can view
- When `remixed_from_agent_id` is supplied, the source composition is authoritative: accessible tools, workflows, Agent Context documents, a non-empty system prompt, and an available chat model are cloned. Caller-supplied `chat_model` and `context_document_ids` are ignored on that path.

##### update_existing
Update fields on an agent you own.
- `agent_id` (required)
- `name`, `description`, `status` (`draft` | `active` | `archived`), `chat_model`, `system_prompt`, `context_document_ids`
- Prefer the dedicated `publish` and `archive` actions over setting `status` directly

##### fetch_existing
List your agents (most recently updated first) or fetch one by id or slug.
- `agent_id` to fetch one; `query`, `limit` (1-100), `skip` to list
- Unreadable or missing agents return `AGENT_FETCH_NOT_FOUND` (existence is masked)

##### search_public
Browse active public agents. `query`, `limit`, `skip`. Only agents that are active AND public AND unarchived appear here.

##### publish
`agent_id`. Moves a draft to active. The first publish stamps `published_at` and promotes `draft_slug` to the public `slug` (clearing `draft_slug`); later publishes keep both. Publishing does **not** make an agent public: `visibility` stays `private` and the agent will not appear in `search_public`. Public visibility is driven by the admin-only `is_template` flag.

##### archive
`agent_id`, optional `forward_to`.
- `forward_to` must be an internal path starting with `/` and free of `..`. Anything else, including an absolute URL, is **silently ignored**: the agent is archived and no redirects are written (`redirects_written: 0`).
- If a well-formed path fails deeper validation (pointing at the agent's own URL, or at a path that is already redirected) the call returns `AGENT_ARCHIVE_SEO_REDIRECT_FAILED` and the agent is left unarchived so it can be retried safely.
- On success the response reports `redirects_written` (one per canonical path: the slug path and the id path).

##### remix
`agent_id`, optional `name`. Creates a **new private draft** from any agent you can view and leaves the source unchanged.
- Copies every source item the new owner can access: products, workflows, Agent Context documents, a non-empty system prompt, and a still-available chat model.
- Missing, inactive, inaccessible, or unavailable items are omitted without failing an otherwise usable clone and are reported in `skipped[]` with `kind`, `id`, and `reason`.
- Showcase examples, template/publication/archive state, source URLs, and the source remix count are not copied.
- Sets `remixed_from_*` and `original_creator_*` attribution and increments the source's `remix_count`.

##### add_product / remove_product
`agent_id`, `product_id`. Attaches or detaches a tool. File Manager is appended automatically when any attached tool, or any tool inside an attached workflow, needs file storage; the response reports `file_manager_added`. Auto-attach is add-only, so File Manager stays attached after you remove the product that pulled it in. Unknown, inactive, or inaccessible products return `AGENT_COMPOSITION_PRODUCT_NOT_FOUND`.

##### add_workflow / remove_workflow
`agent_id`, `workflow_id`. Same automatic file storage behavior applies.

##### attach_context / detach_context
`agent_id`, `context_document_id`. Maximum 10 documents per agent. A malformed id returns `AGENT_CONTEXT_INVALID_ID`. Private context documents are rejected on public active agents.

##### add_showcase_example / remove_showcase_example
`agent_id` plus `showcase_example` (object) or `showcase_example_id` (string). Only one example may be featured; adding a featured example unfeatures the previous one. Duplicate ids return `AGENT_SHOWCASE_DUPLICATE_ID`; malformed examples return `AGENT_SHOWCASE_INVALID_ASSET`.

##### get_instructions
Returns this reference.

#### Showcase example shape
2 to 10 messages, at least one `user` and one `assistant`. Roles do not need to alternate. Each message needs `id`, `role`, `timestamp` (ISO 8601), and a non empty `parts` array. Use durable public URLs or a `file_id` for any media; unsigned private storage URLs are rejected.

#### Examples

```json
{"action":"create_new","name":"Deal Desk","description":"Sales follow-up agent for the Pipedrive pipeline."}
```

```json
{"action":"add_product","agent_id":"<agent_id>","product_id":"<product_id>"}
```

```json
{"action":"update_existing","agent_id":"<agent_id>","system_prompt":"Work only from records in the CRM. Never invent commitments. Every email is a draft for review."}
```

```json
{"action":"publish","agent_id":"<agent_id>"}
```

```json
{"action":"archive","agent_id":"<agent_id>","forward_to":"/agents/replacement-agent"}
```

#### Response
Actions return the affected agent payload (id, name, slug, draft_slug, status, visibility, products, workflows, context_document_ids, showcase_examples, plus computed categories and industry_tags derived from the attached products). Successful remix responses also include `skipped[]` (possibly empty). Errors return a stable `AGENT_*` error code with a usable message.

## When To Use
- Use this skill for `Agent Builder Tool` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: agent builder tool, build a custom ai agent without writing code, turn a job description into a working ai agent, equip an agent with crm inbox calendar and messaging tools, attach multi step workflows to an agent, add product, agent id, product id.
- Supported action names: `add_product`, `add_showcase_example`, `add_workflow`, `archive`, `attach_context`, `create_new`, `detach_context`, `fetch_existing`, `get_instructions`, `publish`, `remix`, `remove_product`, `remove_showcase_example`, `remove_workflow`, `search_public`, `update_existing`.

## Use Cases
- Build a custom AI agent without writing code
- Turn a job description into a working AI agent
- Equip an agent with CRM inbox calendar and messaging tools
- Attach multi step workflows to an agent
- Ground an agent in your own policies pricing and brand voice
- Publish an AI agent and share it with your team
- Remix an existing agent into a specialized version
- Add showcase chat previews to an agent listing
- Manage the agent lifecycle from draft to published to archived
- Prototype and tune agent instructions in a live chat

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`) - Use this companion skill to inspect, download, upload, and manage files referenced by this product.

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `16`.
x402 availability: not enabled for this product.

- `add_product` (action slug: `add-product`): Attach a product to the agent. Routes through file manager auto-attach. Parameters: `agent_id`, `product_id`.
- `add_showcase_example` (action slug: `add-showcase-example`): Add a chat preview example to the agent. Parameters: `agent_id`, `showcase_example`.
- `add_workflow` (action slug: `add-workflow`): Attach a workflow to the agent. Routes through file manager auto-attach. Parameters: `agent_id`, `workflow_id`.
- `archive` (action slug: `archive`): Soft-delete the agent. If forward_to is supplied, issue 301 redirects from the agent's canonical paths to that internal destination. Parameters: `agent_id`, `forward_to`.
- `attach_context` (action slug: `attach-context`): Attach an Agent Context document to the agent. Parameters: `agent_id`, `context_document_id`.
- `create_new` (action slug: `create-new`): Create a private draft agent. Parameters: `chat_model`, `context_document_ids`, `description`, `draft_slug`, `name`, `remixed_from_agent_id`, `remixed_from_agent_name`, `slug`, plus 1 more.
- `detach_context` (action slug: `detach-context`): Detach an Agent Context document from the agent. Parameters: `agent_id`, `context_document_id`.
- `fetch_existing` (action slug: `fetch-existing`): List your agents (recently updated first), or fetch one by id/slug. Parameters: `agent_id`, `limit`, `query`, `skip`.
- `get_instructions` (action slug: `get-instructions`): Return the handler reference guide. Parameters: none.
- `publish` (action slug: `publish`): Transition DRAFT to ACTIVE; stamps published_at the first time. Parameters: `agent_id`.
- `remix` (action slug: `remix`): Create a private copy of a viewable agent. Parameters: `agent_id`, `name`.
- `remove_product` (action slug: `remove-product`): Detach a product from the agent. Routes through file manager auto-attach. Parameters: `agent_id`, `product_id`.
- `remove_showcase_example` (action slug: `remove-showcase-example`): Remove a showcase example by id. Parameters: `agent_id`, `showcase_example_id`.
- `remove_workflow` (action slug: `remove-workflow`): Detach a workflow from the agent. Routes through file manager auto-attach. Parameters: `agent_id`, `workflow_id`.
- `search_public` (action slug: `search-public`): Search active public agents. Parameters: `limit`, `query`, `skip`.
- `update_existing` (action slug: `update-existing`): Update editable fields on an agent you own. is_template is admin-only. Parameters: `agent_id`, `chat_model`, `context_document_ids`, `description`, `draft_slug`, `is_template`, `name`, `slug`, plus 3 more.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "agent-builder-tool"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "agent-builder-tool"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "agent-builder-tool"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "agent-builder-tool"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "agent-builder-tool"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "agent-builder-tool"
  }
}
```

## Call This Tool
Product slug: `agent-builder-tool`

Marketplace page: https://www.agentpmt.com/marketplace/agent-builder-tool

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
    "name": "Agent-Builder-Tool",
    "arguments": {
      "action": "add_product",
      "agent_id": "example agent id",
      "product_id": "example product id"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "agent-builder-tool",
  "parameters": {
    "action": "add_product",
    "agent_id": "example agent id",
    "product_id": "example product id"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `add_product` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/agent-builder-tool
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
