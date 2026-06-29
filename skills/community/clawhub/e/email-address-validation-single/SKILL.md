---
name: email-address-validation-single
description: "Email Address Validation - Single: Verify single email: syntax, DNS/MX lookup, SMTP mailbox check (without sending). Detects disposable, role-based, spam traps. Use when an agent needs email address validation single, email address validation single, form validation for user registration and signups, cleaning email lists before campaigns, reducing bounce rates for email marketing, preventing fake account creation, verify, email through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/email-address-validation-single
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/email-address-validation-single"}}
---
# Email Address Validation - Single

## Freshness
Last updated: `2026-06-23`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Verify the validity and deliverability of individual email addresses. The verification process performs multiple checks including syntax validation, DNS and MX record lookup to confirm the domain can receive mail, and SMTP-level verification that connects to the recipient's mail server to check if the specific mailbox exists—all without sending an actual email. Additional checks detect disposable and temporary email providers, identify role-based addresses like info@ or support@, recognize known spam traps, and reference historical bounce data. Returns verification status (valid, invalid, disposable, catchall, or unknown), flags for potential issues, suggested corrections for typos, and optional metadata including address parsing details.

## Product Instructions
### Email Address Validation - Single

Verify individual email addresses for deliverability and validity. Returns detailed results including whether the email is valid, invalid, disposable, or a catch-all, along with optional address metadata and account credit balance.

#### Actions

##### verify

Validate a single email address and get a deliverability result.

**Required Fields:**
- `action` (string): `"verify"`
- `email` (string): The email address to verify

**Optional Fields:**
- `address_info` (boolean, default: `true`): Include additional address metadata (e.g., free email provider, role account detection)
- `credits_info` (boolean, default: `true`): Include remaining credit balance in the response
- `timeout` (integer, default: `10`, range: 1-30): Request timeout in seconds

**Example - Basic verification:**
```json
{
  "action": "verify",
  "email": "jane.doe@example.com"
}
```

**Example - Verification without extra metadata:**
```json
{
  "action": "verify",
  "email": "support@company.org",
  "address_info": false,
  "credits_info": false
}
```

**Example - Verification with extended timeout:**
```json
{
  "action": "verify",
  "email": "user@slow-mail-server.net",
  "timeout": 25
}
```

#### Response Fields

- `email`: The email address that was checked
- `result`: Verification result (e.g., "valid", "invalid", "disposable", "catchall", "unknown")
- `flags`: Array of flags providing additional context about the address
- `suggested_correction`: A suggested spelling correction if a typo is detected (or null)
- `execution_time`: Time taken to verify the address in milliseconds
- `address_info` (when enabled): Additional metadata about the address such as whether it is a free provider or role account
- `credits_info` (when enabled): Remaining verification credits on the account

#### Common Workflows

1. **Pre-send email validation**: Verify an email address before sending a message to reduce bounces.
2. **Form input validation**: Check an email submitted through a signup or contact form for deliverability.
3. **CRM data hygiene**: Spot-check individual contacts in a CRM to confirm addresses are still valid.
4. **Typo detection**: Use the `suggested_correction` field to catch common misspellings (e.g., "gmial.com" -> "gmail.com").

#### Important Notes

- Each verification consumes one credit.
- Results are real-time checks against the mail server; transient server issues may return "unknown".
- For verifying large batches of emails, use the bulk email verification product instead.
- The `timeout` parameter controls how long to wait for the remote mail server to respond. Increase it for servers known to be slow.

## When To Use
- Use this skill for `Email Address Validation - Single` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: email address validation   single, email address validation single, form validation for user registration and signups, cleaning email lists before campaigns, reducing bounce rates for email marketing, preventing fake account creation, verify, email.
- Supported action names: `verify`.

## Use Cases
- Form validation for user registration and signups
- cleaning email lists before campaigns
- reducing bounce rates for email marketing
- preventing fake account creation
- validating customer contact information at point of entry
- detecting typos and suggesting corrections
- lead qualification and CRM data hygiene
- checkout flow email verification for e-commerce.

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `verify` (action slug: `verify`): Verify a single email address for deliverability and validity. Performs syntax validation, DNS/MX record lookup, and SMTP-level mailbox verification without sending an email. Price: `5` credits. Parameters: `address_info`, `credits_info`, `email`, `timeout`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "email-address-validation-single"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "email-address-validation-single"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "email-address-validation-single"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "email-address-validation-single"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "email-address-validation-single"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "email-address-validation-single"
  }
}
```

## Call This Tool
Product slug: `email-address-validation-single`

Marketplace page: https://www.agentpmt.com/marketplace/email-address-validation-single

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
    "name": "Email-Address-Validation---Single",
    "arguments": {
      "action": "verify",
      "address_info": true,
      "credits_info": true,
      "email": "user@example.com",
      "timeout": 10
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "email-address-validation-single",
  "parameters": {
    "action": "verify",
    "address_info": true,
    "credits_info": true,
    "email": "user@example.com",
    "timeout": 10
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `verify` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/email-address-validation-single
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
