---
name: agentpmt-workflow-creator
description: "AgentPMT Workflow Creator: Build and manage multi-step AI agent workflows (skill chains) that orchestrate tools, prompts, loops, and human notifications into reusable DAG pipelines. Use when an agent needs agentpmt workflow creator, build custom ai agent workflows, automate multi step business processes, chain tools together into reusable pipelines, create no code automation workflows, add showcase example, skill id, showcase example through AgentPMT-hosted remote tool calls."
version: 1.0.1
homepage: https://www.agentpmt.com/marketplace/agentpmt-workflow-creator
compatibility: "Requires AgentPMT internal handler access through the external marketplace API. Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/agentpmt-workflow-creator"}}
---
# AgentPMT Workflow Creator

## Freshness
Last updated: `2026-06-29`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Design, build, and publish specialized AI agent workflows that orchestrate complex multi-step automation across 170+ integrated tools. The AgentPMT Workflow Creator lets you chain together tool calls, AI reasoning steps, iterative loops, conditional branching, and human approval gates into reusable directed acyclic graph (DAG) pipelines. Build anything from simple 3-step automations to sophisticated 15-step business process pipelines that span OCR document processing, CRM updates, financial reconciliation, content generation, data analysis, notification delivery, and more. Each workflow is version-controlled, publishable, and remixable -- start from scratch or fork an existing public workflow and customize it. No code required. Define what each node does, connect them with edges, and the agent runtime handles execution, data flow between steps, and error handling. Workflows support tool nodes (execute any AgentPMT marketplace tool), prompt nodes (AI reasoning and data transformation), for_each nodes (batch processing over collections), and notify_human nodes (approval gates for high-stakes decisions). Publish workflows as reusable skills that any agent can discover and run, complete with industry tagging, time-saved estimates, and showcase examples.

## Product Instructions
### AgentPMT Workflow Creator -- Agent Instructions

#### Required First Step
Call `get_instructions` before creating or updating workflows. Then use `fetch_tools` to get real tool `product_id` and `product_name` values before adding tool nodes.

#### Core Actions
- `get_instructions` -- Retrieve this workflow authoring guide.
- `fetch_tools` -- Search available tools for workflow `tool` nodes.
- `search_public` -- Check existing public workflows before building from scratch.
- `validate` -- Dry-run validate `nodes` and `edges` without persisting. Use this before `create_new`, `update_existing`, and `publish` when changing graph structure.
- `create_new` -- Create a private or public workflow draft.
- `fetch_existing` -- Fetch your workflows or one workflow by `skill_id`.
- `update_existing` -- Update metadata, nodes, or edges for an existing draft.
- `publish` -- Create a versioned executable snapshot.
- `remix` -- Fork a public workflow into a private editable copy.
- `delete` -- Delete a workflow you own.
- `add_showcase_example` / `remove_showcase_example` -- Manage workflow demos.
- `fetch_industry_tags` -- List valid industry tags.

#### Workflow Graph Contract
Persisted workflow nodes are not React Flow nodes. Do not put node configuration inside `data`. Put each node's configuration at the node root under the key matching its node type.

##### Tool Node
Use tool ids and names from `fetch_tools`.

```json
{
  "id": "calculate",
  "type": "tool",
  "label": "Calculate Result",
  "tool": {
    "product_id": "689df4ac8ee2d1dd79e9035b",
    "product_name": "Complex Mathematics Engine",
    "parameters": "{\"action\":\"calculate\",\"expression\":\"2+2\"}",
    "instructions": "Run the calculation and return the numeric result."
  }
}
```

Rules: `tool.product_id` must be an accessible active product ObjectId. `tool.product_name` must be non-empty for agent writes and publish. `tool.parameters`, when present, must be a JSON string.

##### Prompt Node
Freeform prompt:

```json
{
  "id": "summarize",
  "type": "prompt",
  "label": "Summarize Result",
  "prompt": {
    "mode": "freeform",
    "text": "Summarize the calculation result for the user."
  }
}
```

Structured prompt:

```json
{
  "id": "classify",
  "type": "prompt",
  "label": "Classify Expense",
  "prompt": {
    "mode": "structured",
    "goal": "Classify each expense into a reporting category.",
    "inputs": "Receipt vendor, date, amount, and line item text.",
    "outputs": "A category label and short rationale.",
    "constraints": "Use only approved accounting categories."
  }
}
```

Rules: freeform prompts require non-empty `prompt.text` for agent writes and publish. Structured prompts require non-empty `goal` and at least one of `inputs` or `outputs`.

##### for_each Node
Use `for_each` for iteration instead of graph cycles. Child nodes must set `parentId` to the for_each node id and must be reached by a loop edge from that parent.

```json
{
  "id": "each-item",
  "type": "for_each",
  "label": "For Each Item",
  "for_each": {
    "item_alias": "item",
    "instructions": "Run the child steps once for each item in the collection."
  }
}
```

Child prompt example:

```json
{
  "id": "process-item",
  "type": "prompt",
  "label": "Process Item",
  "parentId": "each-item",
  "prompt": {
    "mode": "freeform",
    "text": "Process the current item."
  }
}
```

Required for_each edges:

```json
[
  { "id": "loop-edge", "from": "each-item", "to": "process-item", "sourceHandle": "loop" },
  { "id": "next-edge", "from": "each-item", "to": "after-loop", "sourceHandle": "next" }
]
```

Rules: for_each outgoing handles are only `loop` and `next`. A parented child is invalid unless there is a loop edge from its for_each parent to that child.

##### Branch Node
Use branch nodes for conditional paths. Outgoing handles must be `path_1`, `path_2`, or `path_<index>`.

```json
{
  "id": "choose-path",
  "type": "branch",
  "label": "Choose Path",
  "branch": {
    "description": "Select the next path based on the analysis result.",
    "option_count": 2,
    "options": {
      "path_1": { "name": "Approved", "description": "Proceed automatically." },
      "path_2": { "name": "Review", "description": "Ask a human to review." }
    }
  }
}
```

##### Merge Node
Use merge nodes to join branch paths.

```json
{
  "id": "merge-paths",
  "type": "merge",
  "label": "Merge Paths",
  "merge": {}
}
```

##### notify_human Node
Use only when human approval, credentials, budget, or judgment is genuinely required.

```json
{
  "id": "ask-human",
  "type": "notify_human",
  "label": "Request Approval",
  "notify_human": {
    "request_type": "other",
    "request": "Please review and approve the generated report before delivery."
  }
}
```

Allowed `request_type` values: `add_funds`, `enable_tool`, `enable_workflow`, `credential_setup`, `other`.

#### Edge Contract
Edges connect node ids with `from` and `to`. Optional handles are `sourceHandle` and `targetHandle`.

```json
{ "id": "edge-1", "from": "calculate", "to": "summarize" }
```

Rules:
- All edge endpoints must reference existing node ids.
- Graphs must be acyclic; use `for_each` for iteration.
- Duplicate edges with the same `from`, `to`, and `sourceHandle` are invalid.
- Only branch and for_each nodes may have multiple outgoing edges.
- Edge `condition` is only allowed on branch edges.

#### Position Fields
Canvas-created workflows may include node `position` fields when fetched. Agent-authored payloads should omit `position` unless passing through fetched nodes unchanged. In `agent_write` validation, `position` is accepted for compatibility and removed from the canonical stored graph. Browser draft validation and publish snapshots may retain positions for rendering.

#### Validation Modes
Use `validate` before persisting graph changes.

```json
{
  "action": "validate",
  "validation_mode": "agent_write",
  "nodes": [ ... ],
  "edges": [ ... ]
}
```

Modes:
- `agent_write` -- Use before `create_new` or `update_existing`. Accepts existing fetched positions and canonicalizes them away.
- `draft_structure` -- Browser/editor draft validation.
- `publish_executable` -- Publish-time validation. Requires at least one tool node and complete executable payloads.

#### Recommended Build Flow
1. `get_instructions`.
2. `fetch_tools` for each external capability needed.
3. `search_public` to avoid rebuilding existing workflows.
4. Draft root-level `nodes` and `edges` using the contract above.
5. Call `validate` with `validation_mode: "agent_write"`.
6. Call `create_new` or `update_existing` only after validation passes.
7. Call `fetch_existing` to confirm stored graph shape.
8. Call `publish` only when the graph should become an executable versioned snapshot.

#### Common Mistakes to Avoid
- Do not send `{ "type": "tool", "data": { ... } }`.
- Do not send `{ "type": "prompt", "data": { "prompt": "..." } }`.
- Do not put `product_id` or `product_name` directly on a node; put them under `tool`.
- Do not create cycles for loops; use `for_each` with `loop` and `next` edges.
- Do not invent product ids. Use `fetch_tools`.
- Do not publish malformed drafts to test validation. Use `validate` first.

## When To Use
- Use this skill for `AgentPMT Workflow Creator` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: agentpmt workflow creator, build custom ai agent workflows, automate multi step business processes, chain tools together into reusable pipelines, create no code automation workflows, add showcase example, skill id, showcase example.
- Supported action names: `add_showcase_example`, `attach_context`, `create_new`, `delete`, `detach_context`, `fetch_existing`, `fetch_industry_tags`, `fetch_tools`, `get_instructions`, `publish`, `remix`, `remove_showcase_example`, `search_public`, `update_existing`, `validate`.

## Use Cases
- Build custom AI agent workflows
- automate multi-step business processes
- chain tools together into reusable pipelines
- create no-code automation workflows
- orchestrate document processing pipelines
- build financial reconciliation workflows
- design content creation and publishing pipelines
- automate data collection and reporting
- create customer onboarding sequences
- build monitoring and alerting workflows
- remix and customize existing public workflows
- publish shareable workflow skills for the AgentPMT marketplace

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `15`.
x402 availability: not enabled for this product.

- `add_showcase_example` (action slug: `add-showcase-example`): Add a single showcase example to a workflow skill. Price: `0` credits. Parameters: `showcase_example`, `skill_id`.
- `attach_context` (action slug: `attach-context`): Attach one Agent Context document to a workflow skill draft. Price: `0` credits. Parameters: `context_document_id`, `skill_id`.
- `create_new` (action slug: `create-new`): Create a new workflow skill. Price: `0` credits. Parameters: `chat_model`, `context_document_ids`, `default_export_target`, `description`, `edges`, `industry_tags`, `mcp_server_name`, `name`, plus 5 more.
- `delete` (action slug: `delete`): Delete a workflow skill draft. Price: `0` credits. Parameters: `skill_id`.
- `detach_context` (action slug: `detach-context`): Detach one Agent Context document from a workflow skill draft. Price: `0` credits. Parameters: `context_document_id`, `skill_id`.
- `fetch_existing` (action slug: `fetch-existing`): Fetch workflow skills, optionally filtered to one skill. Price: `0` credits. Parameters: `include_published_only`, `skill_id`.
- `fetch_industry_tags` (action slug: `fetch-industry-tags`): Fetch available industry tags for workflow skills. Price: `0` credits. Parameters: `limit`, `skip`.
- `fetch_tools` (action slug: `fetch-tools`): Browse or search tools available for workflow nodes. Price: `0` credits. Parameters: `exclude_private_tools`, `limit`, `skip`, `sort_by`, `tool_search`.
- `get_instructions` (action slug: `get-instructions`): Fetch usage instructions for workflow skill management. Price: `0` credits. Parameters: none.
- `publish` (action slug: `publish`): Publish a workflow skill version. Price: `0` credits. Parameters: `skill_id`, `version_bump`.
- `remix` (action slug: `remix`): Create a remix from an existing workflow skill. Price: `0` credits. Parameters: `skill_id`.
- `remove_showcase_example` (action slug: `remove-showcase-example`): Remove a showcase example from a workflow skill by id. Price: `0` credits. Parameters: `showcase_example_id`, `skill_id`.
- `search_public` (action slug: `search-public`): Search public workflow skills. Price: `0` credits. Parameters: `categories`, `industry_tags_filter`, `limit`, `publisher`, `query`, `skip`.
- `update_existing` (action slug: `update-existing`): Update an existing workflow skill draft. Price: `0` credits. Parameters: `chat_model`, `context_document_ids`, `default_export_target`, `description`, `edges`, `industry_tags`, `mcp_server_name`, `name`, plus 4 more.
- `validate` (action slug: `validate`): Dry-run validate workflow graph nodes and edges without persisting. Price: `0` credits. Parameters: `edges`, `nodes`, `validation_mode`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "agentpmt-workflow-creator"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "agentpmt-workflow-creator"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "agentpmt-workflow-creator"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "agentpmt-workflow-creator"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "agentpmt-workflow-creator"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "agentpmt-workflow-creator"
  }
}
```

## Call This Tool
Product slug: `agentpmt-workflow-creator`

Marketplace page: https://www.agentpmt.com/marketplace/agentpmt-workflow-creator

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
    "name": "AgentPMT-Workflow-Creator",
    "arguments": {
      "action": "add_showcase_example",
      "showcase_example": null,
      "skill_id": null
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "agentpmt-workflow-creator",
  "parameters": {
    "action": "add_showcase_example",
    "showcase_example": null,
    "skill_id": null
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `add_showcase_example` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/agentpmt-workflow-creator
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
