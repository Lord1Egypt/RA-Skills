---
name: data-generator-programming-and-web
description: "Data Generator - Programming and Web: Generate random data: UUIDs (v1/v4), strings, integers, hex, bytes, passwords, API keys, JWT secrets, colors, emails, IPs, Lorem Ipsum, timestamps. Use when an agent needs data generator programming and web, data generator programming and web, uuid generation, unique identifier creation, uuid v4 random, uuid v1 timestamp, api key, length through AgentPMT-hosted remote tool calls. Discovery terms: data generator programming and web, uuid generation."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/data-generator-programming-and-web
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/data-generator-programming-and-web"}}
---
# Data Generator - Programming and Web

## Freshness
Last updated: `2026-06-11`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Versatile data generation utility that produces random values, unique identifiers, secure credentials, and placeholder content. It supports UUID generation in both version 4 (random) and version 1 (timestamp-based) formats, making it easy to create unique identifiers for databases, distributed systems, and tracking purposes. The tool includes comprehensive random data generation capabilities including strings with customizable character sets, integers within specified ranges, hexadecimal values, raw bytes, hex color codes, fake email addresses, and random IPv4 addresses. For security-focused applications, Generators creates cryptographically secure passwords with configurable complexity rules, URL-safe API keys with optional prefixes, and high-entropy JWT secrets suitable for token signing. Content creators and developers can generate Lorem Ipsum placeholder text by word count, sentence count, or paragraph count. The tool also provides current timestamps in both Unix epoch and ISO 8601 formats. All security-sensitive outputs use cryptographically secure random number generation to ensure unpredictability and safety for production use.

## Product Instructions
### Data Generator - Programming and Web

Generate random data for development, testing, and prototyping: UUIDs, random strings, passwords, API keys, lorem ipsum text, timestamps, and more.

---

#### Actions

##### uuid-v4
Generate a random UUID version 4.

**Required fields:** none

**Example:**
```json
{ "action": "uuid-v4" }
```

---

##### uuid-v1
Generate a UUID version 1 (timestamp-style).

**Required fields:** none

**Example:**
```json
{ "action": "uuid-v1" }
```

---

##### random-string
Generate a random string of a given length and character set.

**Required fields:**
- `length` (integer, 1-1000) — number of characters

**Optional fields:**
- `charset` (string) — one of `alphanumeric` (default), `alpha`, `numeric`, `ascii`, `hex`

**Example:**
```json
{ "action": "random-string", "length": 24, "charset": "ascii" }
```

---

##### random-number
Generate a random integer within a range.

**Required fields:** none

**Optional fields:**
- `min_value` (integer, default 0) — lower bound
- `max_value` (integer, default 100) — upper bound

**Example:**
```json
{ "action": "random-number", "min_value": 1, "max_value": 1000 }
```

---

##### random-hex
Generate a random hexadecimal string.

**Required fields:**
- `length` (integer, 1-64) — number of hex characters

**Example:**
```json
{ "action": "random-hex", "length": 32 }
```

---

##### random-bytes
Generate random bytes returned as a hexadecimal string.

**Required fields:**
- `length` (integer, 1-1024) — number of bytes

**Example:**
```json
{ "action": "random-bytes", "length": 16 }
```

---

##### random-color
Generate a random hex color code (e.g., `#a3f1c2`).

**Required fields:** none

**Example:**
```json
{ "action": "random-color" }
```

---

##### random-email
Generate a random test email address using example domains.

**Required fields:** none

**Example:**
```json
{ "action": "random-email" }
```

---

##### random-ipv4
Generate a random IPv4 address.

**Required fields:** none

**Example:**
```json
{ "action": "random-ipv4" }
```

---

##### password
Generate a secure random password with configurable character types.

**Required fields:**
- `length` (integer, 4-128) — password length

**Optional fields:**
- `include_uppercase` (boolean, default true)
- `include_lowercase` (boolean, default true)
- `include_numbers` (boolean, default true)
- `include_symbols` (boolean, default true)

At least one character type must be enabled.

**Example — 20-character password, no symbols:**
```json
{ "action": "password", "length": 20, "include_symbols": false }
```

---

##### api-key
Generate a URL-safe API key with an optional prefix.

**Required fields:**
- `length` (integer, 16-128) — key length (excluding prefix)

**Optional fields:**
- `prefix` (string, default "") — prefix prepended to the key (e.g., `sk_`, `pk_test_`)

**Example:**
```json
{ "action": "api-key", "length": 40, "prefix": "sk_live_" }
```

---

##### jwt-secret
Generate a secure JWT signing secret.

**Required fields:** none

**Optional fields:**
- `length` (integer, min 32, default 64) — secret length

**Example:**
```json
{ "action": "jwt-secret", "length": 128 }
```

---

##### lorem-ipsum
Generate Lorem Ipsum placeholder text. Priority: words > sentences > paragraphs.

**Required fields:** none

**Optional fields:**
- `words` (integer) — return exactly this many words (overrides sentences/paragraphs)
- `sentences` (integer) — return this many sentences (overrides paragraphs)
- `paragraphs` (integer, default 1) — return this many paragraphs

**Example — 3 sentences:**
```json
{ "action": "lorem-ipsum", "sentences": 3 }
```

**Example — 50 words:**
```json
{ "action": "lorem-ipsum", "words": 50 }
```

---

##### timestamp
Return the current Unix timestamp (seconds since epoch).

**Required fields:** none

**Example:**
```json
{ "action": "timestamp" }
```

---

##### iso-date
Return the current date and time in ISO 8601 format.

**Required fields:** none

**Example:**
```json
{ "action": "iso-date" }
```

---

#### Common Workflows

1. **Seed a test database** — Use `uuid-v4` for IDs, `random-email` for user emails, `password` for hashed credentials, and `lorem-ipsum` for filler text.
2. **Generate API credentials** — Use `api-key` with a prefix like `sk_test_` and `jwt-secret` for signing tokens.
3. **Create mock network data** — Combine `random-ipv4`, `random-hex` (for MAC-style addresses), and `timestamp` for log entries.
4. **UI/design prototyping** — Use `random-color` for palette generation and `lorem-ipsum` for placeholder copy.

#### Important Notes

- All security-related generators (`password`, `api-key`, `jwt-secret`) use cryptographically secure random sources.
- Generated emails use example/test domains and are safe for testing (will not reach real inboxes).
- The `random-bytes` action returns bytes encoded as a hexadecimal string (2 hex chars per byte).
- For `lorem-ipsum`, specifying `words` takes priority over `sentences`, which takes priority over `paragraphs`.

## When To Use
- Use this skill for `Data Generator - Programming and Web` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: data generator   programming and web, data generator programming and web, uuid generation, unique identifier creation, uuid v4 random, uuid v1 timestamp, api key, length.
- Supported action names: `api-key`, `iso-date`, `jwt-secret`, `lorem-ipsum`, `password`, `random-bytes`, `random-color`, `random-email`, `random-hex`, `random-ipv4`, `random-number`, `random-string`, `timestamp`, `uuid-v1`, `uuid-v4`.

## Use Cases
- UUID generation
- unique identifier creation
- UUID v4 random
- UUID v1 timestamp
- random string generator
- random number generator
- random integer range
- hexadecimal string generation
- random bytes generation
- hex color code generator
- random color picker
- fake email generator
- test email address
- random IPv4 address
- mock IP generator
- secure password generator

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `15`.
x402 availability: not enabled for this product.

- `api-key` (action slug: `api-key`): Generate a URL-safe API key with an optional prefix. Price: `5` credits. Parameters: `length`, `prefix`.
- `iso-date` (action slug: `iso-date`): Return the current date and time in ISO 8601 format. Price: `5` credits. Parameters: none.
- `jwt-secret` (action slug: `jwt-secret`): Generate a secure JWT signing secret. Price: `5` credits. Parameters: `length`.
- `lorem-ipsum` (action slug: `lorem-ipsum`): Generate Lorem Ipsum placeholder text. Priority: words > sentences > paragraphs. Price: `5` credits. Parameters: `paragraphs`, `sentences`, `words`.
- `password` (action slug: `password`): Generate a secure random password with configurable character types. Price: `5` credits. Parameters: `include_lowercase`, `include_numbers`, `include_symbols`, `include_uppercase`, `length`.
- `random-bytes` (action slug: `random-bytes`): Generate random bytes returned as a hexadecimal string. Price: `5` credits. Parameters: `length`.
- `random-color` (action slug: `random-color`): Generate a random hex color code (e.g., #a3f1c2). Price: `5` credits. Parameters: none.
- `random-email` (action slug: `random-email`): Generate a random test email address using example domains. Price: `5` credits. Parameters: none.
- `random-hex` (action slug: `random-hex`): Generate a random hexadecimal string. Price: `5` credits. Parameters: `length`.
- `random-ipv4` (action slug: `random-ipv4`): Generate a random IPv4 address. Price: `5` credits. Parameters: none.
- `random-number` (action slug: `random-number`): Generate a random integer within a specified range. Price: `5` credits. Parameters: `max_value`, `min_value`.
- `random-string` (action slug: `random-string`): Generate a random string of specified length and character set. Price: `5` credits. Parameters: `charset`, `length`.
- `timestamp` (action slug: `timestamp`): Return the current Unix timestamp (seconds since epoch). Price: `5` credits. Parameters: none.
- `uuid-v1` (action slug: `uuid-v1`): Generate a UUID version 1 (timestamp-based). Price: `5` credits. Parameters: none.
- `uuid-v4` (action slug: `uuid-v4`): Generate a random UUID version 4. Price: `5` credits. Parameters: none.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "data-generator-programming-and-web"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "data-generator-programming-and-web"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "data-generator-programming-and-web"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "data-generator-programming-and-web"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "data-generator-programming-and-web"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "data-generator-programming-and-web"
  }
}
```

## Call This Tool
Product slug: `data-generator-programming-and-web`

Marketplace page: https://www.agentpmt.com/marketplace/data-generator-programming-and-web

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
    "name": "Data-Generator---Programming-and-Web",
    "arguments": {
      "action": "api-key",
      "length": 16,
      "prefix": ""
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "data-generator-programming-and-web",
  "parameters": {
    "action": "api-key",
    "length": 16,
    "prefix": ""
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `api-key` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/data-generator-programming-and-web
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
