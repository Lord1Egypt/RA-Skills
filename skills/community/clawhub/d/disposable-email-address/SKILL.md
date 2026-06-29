---
name: disposable-email-address
description: "Disposable Email Address: Create temporary email addresses (24h expiration), check inboxes, and list active addresses. Shared across agents on same budget. Use when an agent needs disposable email address, ai agent account signups, service registration, receiving verification links, automated testing workflows, check, email, create through AgentPMT-hosted remote tool calls. Discovery terms: disposable email address, ai agent account signups, service registration, receiving verification links."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/disposable-email-address
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/disposable-email-address"}}
---
# Disposable Email Address

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
The Temporary Email Service provides disposable email addresses for AI agents to use for account signups and verification workflows. It supports three actions: Create a new temporary email address (24-hour expiration), Check an inbox for messages, List all active email addresses for the authenticated user

For creating and monitoring a temporary, disposable email address inbox. It is designed for AI agents to use for tasks like service registrations and receiving verification links without using a permanent email. Allows cross communication between all agents on the same budget - any one can check the inbox

## Product Instructions
### Disposable Email Address

Create temporary, disposable email addresses and check their inboxes. Useful for account signups, verification flows, and receiving one-time codes without exposing a real email address.

#### Actions

##### create

Create a new temporary disposable email address. Addresses are valid for 24 hours.

**Required fields:** None

**Optional fields:**
- `username` (string) - Preferred username for the email address. If omitted, a random username is generated.

**Example:**
```json
{
  "action": "create",
  "username": "myagent"
}
```

**Response includes:** email address, created_at timestamp, expires_at timestamp.

---

##### check

Check the inbox of a previously created email address and retrieve all messages with full content.

**Required fields:**
- `email` (string) - The email address to check. Must be an address you previously created with the `create` action.

**Optional fields:** None

**Example:**
```json
{
  "action": "check",
  "email": "myagent@guerrillamail.com"
}
```

**Response includes:** email address, message_count, and a messages array. Each message contains from, subject, body, and received_at.

---

##### fetch

List all active (non-expired) email addresses belonging to the current user, along with time remaining for each.

**Required fields:** None

**Optional fields:** None

**Example:**
```json
{
  "action": "fetch"
}
```

**Response includes:** count and an emails array. Each entry contains email, created_at, expires_at, and time_remaining_hours.

---

#### Common Workflows

##### Sign up for a service and verify the email
1. Use `create` to generate a disposable email address.
2. Use that email address to sign up for the target service.
3. Use `check` with the email address to retrieve the verification code or confirmation link.

##### Manage multiple temporary addresses
1. Use `create` multiple times to generate different addresses for different purposes.
2. Use `fetch` to see all your active addresses and how much time remains on each.
3. Use `check` on any specific address to read its messages.

#### Important Notes

- Email addresses expire after **24 hours** from creation.
- You can only check inboxes for email addresses you created yourself.
- If no `username` is provided during creation, a random one is assigned automatically.
- Messages are returned with full content including sender, subject, and body.
- Expired email addresses cannot be checked and will not appear in `fetch` results.

## When To Use
- Use this skill for `Disposable Email Address` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: disposable email address, ai agent account signups, service registration, receiving verification links, automated testing workflows, check, email, create.
- Supported action names: `check`, `create`, `fetch`.

## Use Cases
- AI Agent Account Signups
- Service Registration
- Receiving Verification Links
- Automated Testing Workflows
- Temporary Communications Channel
- Data Privacy Protection
- Automated Account Creation
- Reading Verification Emails
- Processing Inbound Messages
- Automated Software Testing
- Extracting Data from Emails
- Parsing One-Time Passwords (OTPs)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `3`.
x402 availability: not enabled for this product.

- `check` (action slug: `check`): Check the inbox of a previously created email address and retrieve all messages with full content including sender, subject, body, and received timestamp. Price: `15` credits. Parameters: `email`.
- `create` (action slug: `create`): Create a new temporary disposable email address with a 24-hour expiration. Returns the email address, creation time, and expiration time. Price: `15` credits. Parameters: `username`.
- `fetch` (action slug: `fetch`): List all active (non-expired) email addresses belonging to the current user, along with creation time, expiration time, and hours remaining for each. Price: `15` credits. Parameters: none.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "disposable-email-address"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "disposable-email-address"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "disposable-email-address"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "disposable-email-address"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "disposable-email-address"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "disposable-email-address"
  }
}
```

## Call This Tool
Product slug: `disposable-email-address`

Marketplace page: https://www.agentpmt.com/marketplace/disposable-email-address

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
    "name": "Disposable-Email-Address",
    "arguments": {
      "action": "check",
      "email": "user@example.com"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "disposable-email-address",
  "parameters": {
    "action": "check",
    "email": "user@example.com"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `check` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/disposable-email-address
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
