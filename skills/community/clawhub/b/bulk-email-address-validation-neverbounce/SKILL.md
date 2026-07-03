---
name: bulk-email-address-validation-neverbounce
description: "Bulk Email Address Validation - NeverBounce: Bulk verify up to 1000 emails via NeverBounce using the user's connected NeverBounce API key. Use when an agent needs bulk email address validation neverbounce, bulk email address validation neverbounce, cleaning email marketing lists before campaigns, bulk crm data hygiene and deduplication, validating imported contact lists, preparing email lists for migration between platforms, verify, emails through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/bulk-email-address-validation-neverbounce
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/bulk-email-address-validation-neverbounce"}}
---
# Bulk Email Address Validation - NeverBounce

## Freshness
Last updated: `2026-06-23`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Verify the validity and deliverability of up to 1,000 email addresses in a single batch using the user's connected NeverBounce API key. Each email undergoes syntax validation, DNS and MX record lookup, and SMTP-level mailbox verification without sending actual emails. Additional checks detect disposable providers, role-based addresses, spam traps, and duplicates. Returns per-email verification results along with aggregate statistics including counts for valid, invalid, catchall, unknown, disposable, and duplicate addresses. For large jobs that exceed the timeout, returns a job ID for checking status later.

## Product Instructions
### Bulk Email Address Validation

Verify large batches of email addresses at once (up to 1,000 per request). The user's NeverBounce API key is connected in AgentPMT and injected automatically at runtime; do not include API keys in tool inputs.

#### Actions

##### verify

Validate a list of email addresses in bulk. The tool creates a verification job, polls for completion, and returns per-email results with summary statistics.

**Required Fields:**
- `action` — set to `"verify"`
- `emails` — array of email addresses to verify (1 to 1,000)

**Credential Required:**
- Connect a NeverBounce API Key credential in AgentPMT before running this tool.

**Optional Fields:**
- `timeout` — maximum seconds to wait for results (default: 30, range: 10-300). For large lists, increase this value.

**Example:**
```json
{
  "action": "verify",
  "emails": [
    "alice@example.com",
    "bob@invalid-domain.xyz",
    "carol@gmail.com",
    "support@company.org"
  ],
  "timeout": 60
}
```

**Response includes:**
- `job_id` — unique identifier for the verification job
- `status` — job status, such as `complete`
- `total_processed` — number of emails processed
- `results_summary` — counts by category: valid, invalid, catchall, unknown, disposable, duplicate
- `results` — per-email array with `email`, `result`, `flags`, and `suggested_correction`

**Result categories:**
- **valid** — confirmed deliverable address
- **invalid** — undeliverable address, such as bad domain or missing mailbox
- **catchall** — domain accepts all mail; individual address cannot be confirmed
- **unknown** — verification was inconclusive
- **disposable** — temporary or throwaway email address
- **duplicate** — address appeared more than once in the batch

**Timeout behavior:** If the job does not finish within the timeout window, the response returns the `job_id` and current status so you can reference it later.

#### Common Workflows

##### Clean a mailing list before a campaign
1. Collect all recipient addresses into an array.
2. Call `verify` with the list, split into batches of 1,000 if needed.
3. Remove addresses marked **invalid** or **disposable**.
4. Review **catchall** and **unknown** addresses for manual decision.

##### Validate sign-up imports
1. Export new user emails from your database.
2. Call `verify` to flag bad addresses.
3. Reach out to users with invalid emails to request corrections, using `suggested_correction` when available.

#### Important Notes

- **Batch limit:** maximum 1,000 emails per request. For larger lists, split into multiple calls.
- **Timeout guidance:** small lists under 50 typically complete within 30 seconds. Larger lists may need 60-300 seconds. If a job times out, you receive a `job_id` to check later.
- **Duplicates:** duplicate emails in the same batch are flagged in the results summary.
- **Rate / billing:** each email in the batch counts as one verification unit.

## When To Use
- Use this skill for `Bulk Email Address Validation - NeverBounce` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: bulk email address validation   neverbounce, bulk email address validation neverbounce, cleaning email marketing lists before campaigns, bulk crm data hygiene and deduplication, validating imported contact lists, preparing email lists for migration between platforms, verify, emails.
- Supported action names: `verify`.

## Use Cases
- Cleaning email marketing lists before campaigns
- bulk CRM data hygiene and deduplication
- validating imported contact lists
- preparing email lists for migration between platforms
- lead list verification before sales outreach
- newsletter subscriber list maintenance
- reducing bounce rates for high-volume senders
- pre-send verification for transactional email systems
- periodic database cleanup and validation audits.

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `1`.
x402 availability: not enabled for this product.

- `verify` (action slug: `verify`): Verify a list of email addresses in bulk (1-1000). Creates a verification job, polls for completion, and returns per-email results with summary statistics. Price: `5` credits. Parameters: `emails`, `timeout`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "bulk-email-address-validation-neverbounce"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "bulk-email-address-validation-neverbounce"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "bulk-email-address-validation-neverbounce"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "bulk-email-address-validation-neverbounce"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "bulk-email-address-validation-neverbounce"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "bulk-email-address-validation-neverbounce"
  }
}
```

## Call This Tool
Product slug: `bulk-email-address-validation-neverbounce`

Marketplace page: https://www.agentpmt.com/marketplace/bulk-email-address-validation-neverbounce

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
    "name": "Bulk-Email-Address-Validation---NeverBounce",
    "arguments": {
      "action": "verify",
      "emails": [
        "user@example.com"
      ],
      "timeout": 30
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "bulk-email-address-validation-neverbounce",
  "parameters": {
    "action": "verify",
    "emails": [
      "user@example.com"
    ],
    "timeout": 30
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
- Marketplace product: https://www.agentpmt.com/marketplace/bulk-email-address-validation-neverbounce
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
