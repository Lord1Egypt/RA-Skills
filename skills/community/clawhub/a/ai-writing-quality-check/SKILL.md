---
name: ai-writing-quality-check
description: "AI Writing Quality Check: Scan writing content for banned phrases and return a normalized response for rewrite loops. Use when an agent needs ai writing quality check, pre publish quality checks for marketing copy, headline and cta rewrite loops, social post phrase compliance checks, blog and article draft quality gating, check for banned phrases, content through AgentPMT-hosted remote tool calls. Discovery terms: ai writing quality check, pre publish quality checks for marketing copy."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/ai-writing-quality-check
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/ai-writing-quality-check"}}
---
# AI Writing Quality Check

## Freshness
Last updated: `2026-06-24`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Catch banned phrases, and overused AI clichés in draft copy before you ship it - built for iterative rewrite loops inside AI content workflows. Point this tool at a headline, CTA, social post, email, landing page, or long-form blog and get back field-level correction targets: the exact matched phrase, its character index, surrounding context, and the reason it was flagged. Agents can take those corrections, rewrite inline, and re-run the check until the copy passes - no vague "improve this" feedback, no guessing. Ideal for marketing ops, content teams, SEO writers, brand compliance reviewers, and any AI copywriting pipeline that needs a deterministic, repeatable quality gate.

## Product Instructions
### AI Writing Quality Check

Use this tool to scan writing and return exact correction targets for rewrite loops.

#### Actions

##### get_instructions
Returns this documentation.

##### check_for_banned_phrases
Checks content for banned phrases and returns normalized correction guidance.

Parameters:
- `content` (required): writing content to check.

#### Example

```json
{
  "action": "check_for_banned_phrases",
  "content": "Our customers love us. Ask our AI."
}
```

#### Rewrite Loop
1. Run `check_for_banned_phrases` with content.
2. If `passed` is `true`, publish.
3. If `passed` is `false`, rewrite each entry in `corrections`.
4. Run `check_for_banned_phrases` again until `passed` is `true`.

## When To Use
- Use this skill for `AI Writing Quality Check` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: ai writing quality check, pre publish quality checks for marketing copy, headline and cta rewrite loops, social post phrase compliance checks, blog and article draft quality gating, check for banned phrases, content.
- Supported action names: `check_for_banned_phrases`.

## Use Cases
- Pre-publish quality checks for marketing copy
- Headline and CTA rewrite loops
- Social post phrase compliance checks
- Blog and article draft quality gating
- Email subject line banned-phrase screening
- Landing page hero copy sanity checks
- Product description compliance review
- Ad copy phrase-list enforcement
- Brand voice guardrails for AI copywriters
- Automated copy review inside multi-step agent workflows
- SEO draft cleanup before publishing
- AI cliché detection in long-form content
- Field-level correction feedback for content editors
- Consistent enforcement of organization-wide banned-phrase policy
- Repeatable copy quality gates in content approval workflows

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 action routes are enabled and listed in `./schema.md`.

- `check_for_banned_phrases` (action slug: `check-for-banned-phrases`): Check writing for banned phrases and return correction targets tied to the content field. Price: `5` credits. Parameters: `content`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "ai-writing-quality-check"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "ai-writing-quality-check"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "ai-writing-quality-check"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "ai-writing-quality-check"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "ai-writing-quality-check"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "ai-writing-quality-check"
  }
}
```

## Call This Tool
Product slug: `ai-writing-quality-check`

Marketplace page: https://www.agentpmt.com/marketplace/ai-writing-quality-check

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- No-account AgentAddress/x402 route: first use `../agentpmt-no-account-agentaddress-x402` for the canonical payment and wallet setup instructions.
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
- No-account AgentAddress/x402 setup: ../agentpmt-no-account-agentaddress-x402
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402
  - OpenClaw install: `openclaw skills install agentpmt-no-account-agentaddress-x402`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-no-account-agentaddress-x402`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
npx skills add AgentPMT/agent-skills --skill agentpmt-no-account-agentaddress-x402
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AI-Writing-Quality-Check",
    "arguments": {
      "action": "check_for_banned_phrases",
      "content": "Draft marketing copy to check for banned phrases."
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "ai-writing-quality-check",
  "parameters": {
    "action": "check_for_banned_phrases",
    "content": "Draft marketing copy to check for banned phrases."
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `check_for_banned_phrases` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- No-account AgentAddress/x402 setup: ../agentpmt-no-account-agentaddress-x402 (ClawHub: `agentpmt-no-account-agentaddress-x402`, page: https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-no-account-agentaddress-x402`)
- Marketplace product: https://www.agentpmt.com/marketplace/ai-writing-quality-check
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
