---
name: data-format-validation
description: "Data Format Validation: Validate data formats: JSON, email, UUID, IPv4/6, MAC, credit card (Luhn), IBAN, phone, hex color, ISBN, Base64, regex patterns. Use when an agent needs data format validation, json validation, json syntax check, json parsing error detection, email validation, validate base64, text, validate credit card through AgentPMT-hosted remote tool calls. Discovery terms: data format validation, json validation, json syntax check, json parsing error detection, email validation."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/data-format-validation
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/data-format-validation"}}
---
# Data Format Validation

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Data format validation utility that checks whether input strings conform to standard formats and specifications across a wide range of common data types. It validates JSON syntax and reports parsing errors with specific error locations, verifies email addresses against RFC-compliant patterns while extracting local and domain parts, and checks UUIDs for proper formatting with version detection. Network-related validation includes IPv4 addresses with octet range checking and private or loopback detection, IPv6 addresses with compression and link-local identification, MAC addresses in both colon and hyphen-separated formats, and URLs with scheme and domain parsing. Financial validation covers credit card numbers using the Luhn checksum algorithm with automatic card type detection for Visa, Mastercard, American Express, and Discover, as well as IBAN validation with country code extraction and BBAN parsing using the mod-97 checksum. Additional validators handle phone numbers with international format detection, hexadecimal color codes in both short and long formats with RGB value extraction, ISBN-10 and ISBN-13 with checksum verification, base64 encoding with decoded length reporting, and regex pattern syntax checking. All validators return detailed results including validity status, parsed components, and specific error messages for invalid input.

## Product Instructions
### Data Format Validation - Instructions

#### Overview
Validate data formats including emails, URLs, JSON, UUIDs, IP addresses, credit cards, phone numbers, colors, ISBNs, IBANs, MAC addresses, Base64, and regex patterns. Each action returns whether the input is valid along with format-specific details.

#### Parameters
- **action** (required): The validation action to perform.
- **text** (required): The string to validate.

---

#### Actions

##### validate-json
Validate whether a string is well-formed JSON. Also used by `validate-json-syntax`.

- **text** (required): The JSON string to check.

**Example:**
```json
{ "action": "validate-json", "text": "{\"name\": \"Alice\", \"age\": 30}" }
```
Returns: valid status, parsed type (dict, list, etc.).

---

##### validate-email
Validate an email address format (RFC 5322 simplified).

- **text** (required): The email address to validate.

**Example:**
```json
{ "action": "validate-email", "text": "user@example.com" }
```
Returns: valid status, local_part, domain.

---

##### validate-uuid
Validate a UUID string (versions 1-5, RFC 4122).

- **text** (required): The UUID to validate.

**Example:**
```json
{ "action": "validate-uuid", "text": "550e8400-e29b-41d4-a716-446655440000" }
```
Returns: valid status, version number, variant.

---

##### validate-base64
Validate whether a string is properly Base64-encoded.

- **text** (required): The Base64 string to validate.

**Example:**
```json
{ "action": "validate-base64", "text": "SGVsbG8gV29ybGQ=" }
```
Returns: valid status, decoded byte length.

---

##### validate-url
Validate a URL format (checks for scheme and domain).

- **text** (required): The URL to validate.

**Example:**
```json
{ "action": "validate-url", "text": "https://www.example.com/path?q=test#section" }
```
Returns: valid status, scheme, domain, path, has_query, has_fragment.

---

##### validate-ipv4
Validate an IPv4 address and classify it.

- **text** (required): The IPv4 address to validate.

**Example:**
```json
{ "action": "validate-ipv4", "text": "192.168.1.1" }
```
Returns: valid status, octets, is_private, is_loopback.

---

##### validate-ipv6
Validate an IPv6 address and classify it.

- **text** (required): The IPv6 address to validate.

**Example:**
```json
{ "action": "validate-ipv6", "text": "2001:0db8:85a3:0000:0000:8a2e:0370:7334" }
```
Returns: valid status, is_loopback, is_link_local, compressed.

---

##### validate-mac-address
Validate a MAC address (colon or hyphen separated).

- **text** (required): The MAC address to validate.

**Example:**
```json
{ "action": "validate-mac-address", "text": "00:1A:2B:3C:4D:5E" }
```
Returns: valid status, format (colon/hyphen-separated), octets, canonical form.

---

##### validate-credit-card
Validate a credit card number using the Luhn algorithm and detect card type.

- **text** (required): The card number (spaces and hyphens are stripped automatically).

**Example:**
```json
{ "action": "validate-credit-card", "text": "4111 1111 1111 1111" }
```
Returns: valid status, card_type (Visa, Mastercard, Amex, Discover), length, last_four.

---

##### validate-phone
Validate a phone number format (10-15 digits, optional international prefix).

- **text** (required): The phone number to validate (parentheses, spaces, hyphens, dots are stripped).

**Example:**
```json
{ "action": "validate-phone", "text": "+1 (555) 123-4567" }
```
Returns: valid status, international flag, digit_count, formatted number.

---

##### validate-hex-color
Validate a hex color code (#RGB or #RRGGBB).

- **text** (required): The hex color string to validate.

**Example:**
```json
{ "action": "validate-hex-color", "text": "#FF5733" }
```
Returns: valid status, format (short/long), RGB values or expanded form.

---

##### validate-isbn
Validate an ISBN-10 or ISBN-13 (with checksum verification).

- **text** (required): The ISBN to validate (hyphens and spaces are stripped).

**Example:**
```json
{ "action": "validate-isbn", "text": "978-0-306-40615-7" }
```
Returns: valid status, format (ISBN-10 or ISBN-13), cleaned ISBN.

---

##### validate-iban
Validate an International Bank Account Number (mod-97 checksum).

- **text** (required): The IBAN to validate (spaces are stripped).

**Example:**
```json
{ "action": "validate-iban", "text": "GB29 NWBK 6016 1331 9268 19" }
```
Returns: valid status, country_code, check_digits, BBAN.

---

##### validate-regex
Validate whether a string is a compilable regular expression.

- **text** (required): The regex pattern to validate.

**Example:**
```json
{ "action": "validate-regex", "text": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+$" }
```
Returns: valid status. If invalid, returns the specific regex error.

---

##### validate-json-syntax
Alias for `validate-json`. Validates whether a string is well-formed JSON.

- **text** (required): The JSON string to check.

**Example:**
```json
{ "action": "validate-json-syntax", "text": "[1, 2, 3]" }
```

---

#### Common Workflows

1. **Data ingestion pipeline**: Use `validate-json` to check incoming payloads, `validate-email` for contact fields, and `validate-url` for link fields before processing.
2. **Network configuration audit**: Combine `validate-ipv4`, `validate-ipv6`, and `validate-mac-address` to verify device configuration data.
3. **E-commerce checkout**: Use `validate-credit-card` to pre-check card numbers, `validate-email` for customer email, and `validate-phone` for contact number.
4. **Book catalog management**: Use `validate-isbn` to verify book identifiers during import.
5. **Financial data validation**: Use `validate-iban` to verify bank account numbers in international transactions.

#### Important Notes
- All actions require the `text` parameter.
- Whitespace, hyphens, and common separators are automatically stripped where appropriate (credit cards, phone numbers, ISBNs, IBANs, MAC addresses).
- Credit card validation uses the Luhn algorithm and detects Visa, Mastercard, American Express, and Discover.
- UUID validation supports versions 1 through 5.
- Phone validation accepts 10-15 digit numbers with optional international (+) prefix.
- IBAN validation uses the mod-97 checksum per ISO 13616.
- Every response includes a `valid` boolean and a descriptive `message`.

## When To Use
- Use this skill for `Data Format Validation` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: data format validation, json validation, json syntax check, json parsing error detection, email validation, validate base64, text, validate credit card.
- Supported action names: `validate-base64`, `validate-credit-card`, `validate-email`, `validate-hex-color`, `validate-iban`, `validate-ipv4`, `validate-ipv6`, `validate-isbn`, `validate-json`, `validate-json-syntax`, `validate-mac-address`, `validate-phone`, `validate-regex`, `validate-url`, `validate-uuid`.

## Use Cases
- JSON validation
- JSON syntax check
- JSON parsing error detection
- email validation
- email format verification
- RFC email check
- UUID validation
- UUID version detection
- UUID format check
- base64 validation
- base64 encoding check
- base64 decode verification
- URL validation
- URL format check
- URL parsing
- domain extraction

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `15`.
x402 availability: not enabled for this product.

- `validate-base64` (action slug: `validate-base64`): Validate whether a string is properly Base64-encoded. Returns valid status and decoded byte length. Price: `5` credits. Parameters: `text`.
- `validate-credit-card` (action slug: `validate-credit-card`): Validate a credit card number using the Luhn algorithm. Detects card type (Visa, Mastercard, Amex, Discover). Spaces and hyphens are stripped. Price: `5` credits. Parameters: `text`.
- `validate-email` (action slug: `validate-email`): Validate an email address format (RFC 5322 simplified). Returns valid status, local_part, and domain. Price: `5` credits. Parameters: `text`.
- `validate-hex-color` (action slug: `validate-hex-color`): Validate a hexadecimal color code (#RGB or #RRGGBB). Returns valid status, format, and RGB values or expanded form. Price: `5` credits. Parameters: `text`.
- `validate-iban` (action slug: `validate-iban`): Validate an International Bank Account Number (mod-97 checksum). Spaces are stripped. Returns country_code, check_digits, BBAN. Price: `5` credits. Parameters: `text`.
- `validate-ipv4` (action slug: `validate-ipv4`): Validate an IPv4 address and classify it. Returns valid status, octets, is_private, is_loopback. Price: `5` credits. Parameters: `text`.
- `validate-ipv6` (action slug: `validate-ipv6`): Validate an IPv6 address and classify it. Returns valid status, is_loopback, is_link_local, compressed flag. Price: `5` credits. Parameters: `text`.
- `validate-isbn` (action slug: `validate-isbn`): Validate an ISBN-10 or ISBN-13 with checksum verification. Hyphens and spaces are stripped. Price: `5` credits. Parameters: `text`.
- `validate-json` (action slug: `validate-json`): Validate whether a string is well-formed JSON. Returns valid status and parsed type. Price: `5` credits. Parameters: `text`.
- `validate-json-syntax` (action slug: `validate-json-syntax`): Alias for validate-json. Validates whether a string is well-formed JSON. Price: `5` credits. Parameters: `text`.
- `validate-mac-address` (action slug: `validate-mac-address`): Validate a MAC address (colon or hyphen separated). Returns valid status, format, octets, canonical form. Price: `5` credits. Parameters: `text`.
- `validate-phone` (action slug: `validate-phone`): Validate a phone number format (10-15 digits, optional international prefix). Parentheses, spaces, hyphens, dots are stripped. Price: `5` credits. Parameters: `text`.
- `validate-regex` (action slug: `validate-regex`): Validate whether a string is a compilable regular expression. Returns valid status and specific regex error if invalid. Price: `5` credits. Parameters: `text`.
- `validate-url` (action slug: `validate-url`): Validate a URL format (checks for scheme and domain). Returns valid status, scheme, domain, path, query and fragment flags. Price: `5` credits. Parameters: `text`.
- `validate-uuid` (action slug: `validate-uuid`): Validate a UUID string (versions 1-5, RFC 4122). Returns valid status, version, and variant. Price: `5` credits. Parameters: `text`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "data-format-validation"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "data-format-validation"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "data-format-validation"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "data-format-validation"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "data-format-validation"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "data-format-validation"
  }
}
```

## Call This Tool
Product slug: `data-format-validation`

Marketplace page: https://www.agentpmt.com/marketplace/data-format-validation

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
    "name": "Data-Format-Validation",
    "arguments": {
      "action": "validate-base64",
      "text": "example text"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "data-format-validation",
  "parameters": {
    "action": "validate-base64",
    "text": "example text"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `validate-base64` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/data-format-validation
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
