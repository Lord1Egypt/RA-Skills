---
name: data-format-encoder
description: "Data Format Encoder: Encode/decode text: Base64, URL encoding, HTML entities, JSON escaping, hex, binary, ROT13, Unicode escapes. Use when an agent needs data format encoder, base64 encoding, base64 decoding, binary to text encoding, data url creation, encode base64 decode, text, encode base64 encode through AgentPMT-hosted remote tool calls. Discovery terms: data format encoder, base64 encoding, base64 decoding, binary to text encoding, data url creation, encode base64 decode, text."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/data-format-encoder
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/data-format-encoder"}}
---
# Data Format Encoder

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
A text transformation utility that converts strings between various encoding formats commonly used in web development, data transmission, and programming. It provides bidirectional base64 encoding and decoding for binary-to-text representation used in data URLs, API payloads, and email attachments. URL encoding applies percent-encoding for safe transmission of special characters in query strings and path segments, while URL decoding reverses the process for parsing incoming requests. HTML entity encoding escapes special characters like angle brackets, ampersands, and quotes for safe inclusion in HTML documents, preventing XSS vulnerabilities and rendering issues. JSON string escaping handles special characters including newlines, tabs, backslashes, and quotes for embedding text within JSON structures. Hexadecimal conversion transforms text to and from hex representation for debugging, cryptographic applications, and low-level data inspection. Binary encoding produces space-separated 8-bit representations for educational purposes and bit-level analysis. ROT13 applies the classic letter substitution cipher that shifts characters by 13 positions, useful for simple text obfuscation. Unicode escape sequences convert non-ASCII characters to backslash-u notation for source code compatibility and cross-platform text handling. All operations include metadata about input and output lengths.

## Product Instructions
### Data Format Encoder

Encode, decode, escape, and convert text between multiple data formats including Base64, URL encoding, HTML entities, JSON, hexadecimal, binary, ROT13, and Unicode.

#### Actions

##### encode-base64-encode
Encode plain text to Base64 format.

**Required fields:** `text` - the plain text to encode

**Example:**
```json
{
  "action": "encode-base64-encode",
  "text": "Hello world!"
}
```
Returns the Base64-encoded string (e.g., `SGVsbG8gd29ybGQh`).

---

##### encode-base64-decode
Decode a Base64-encoded string back to plain text.

**Required fields:** `text` - the Base64-encoded string

**Example:**
```json
{
  "action": "encode-base64-decode",
  "text": "SGVsbG8gd29ybGQh"
}
```

---

##### encode-url-encode
Percent-encode text for safe use in URLs.

**Required fields:** `text` - the text to URL-encode

**Example:**
```json
{
  "action": "encode-url-encode",
  "text": "hello world & goodbye"
}
```
Returns `hello%20world%20%26%20goodbye`.

---

##### encode-url-decode
Decode a percent-encoded (URL-encoded) string back to plain text.

**Required fields:** `text` - the URL-encoded string

**Example:**
```json
{
  "action": "encode-url-decode",
  "text": "hello%20world%20%26%20goodbye"
}
```

---

##### encode-html-entity-encode
Escape special HTML characters (e.g., `<`, `>`, `&`, `"`) into HTML entities.

**Required fields:** `text` - the text containing HTML characters

**Example:**
```json
{
  "action": "encode-html-entity-encode",
  "text": "<div class=\"main\">Hello & welcome</div>"
}
```
Returns `&lt;div class=&quot;main&quot;&gt;Hello &amp; welcome&lt;/div&gt;`.

---

##### encode-html-entity-decode
Convert HTML entities back to their original characters.

**Required fields:** `text` - the HTML-entity-encoded string

**Example:**
```json
{
  "action": "encode-html-entity-decode",
  "text": "&lt;p&gt;Hello &amp; welcome&lt;/p&gt;"
}
```

---

##### encode-escape-json
Escape special characters in text for safe embedding inside JSON strings (e.g., newlines, tabs, quotes).

**Required fields:** `text` - the text to JSON-escape

**Example:**
```json
{
  "action": "encode-escape-json",
  "text": "Line 1\nLine 2\tTabbed \"quoted\""
}
```
Returns `Line 1\\nLine 2\\tTabbed \\\"quoted\\\"`.

---

##### encode-unescape-json
Convert JSON-escaped sequences back to their original characters.

**Required fields:** `text` - the JSON-escaped string

**Example:**
```json
{
  "action": "encode-unescape-json",
  "text": "Line 1\\nLine 2\\tTabbed \\\"quoted\\\""
}
```

---

##### encode-text-to-hex
Convert text to its hexadecimal byte representation.

**Required fields:** `text` - the plain text to convert

**Example:**
```json
{
  "action": "encode-text-to-hex",
  "text": "Hello"
}
```
Returns `48656c6c6f`.

---

##### encode-hex-to-text
Convert a hexadecimal string back to plain text. Spaces, colons, and hyphens between hex bytes are automatically removed.

**Required fields:** `text` - the hexadecimal string

**Example:**
```json
{
  "action": "encode-hex-to-text",
  "text": "48 65 6c 6c 6f"
}
```

---

##### encode-text-to-binary
Convert text to its 8-bit binary representation (space-separated bytes).

**Required fields:** `text` - the plain text to convert

**Example:**
```json
{
  "action": "encode-text-to-binary",
  "text": "Hi"
}
```
Returns `01001000 01101001`.

---

##### encode-binary-to-text
Convert an 8-bit binary string back to plain text. The binary string length must be a multiple of 8 bits.

**Required fields:** `text` - the binary string (spaces between bytes are optional)

**Example:**
```json
{
  "action": "encode-binary-to-text",
  "text": "01001000 01101001"
}
```

---

##### encode-rot13-encode
Apply the ROT13 substitution cipher to text. ROT13 is its own inverse -- apply it again to decode.

**Required fields:** `text` - the text to encode/decode

**Example:**
```json
{
  "action": "encode-rot13-encode",
  "text": "Hello World"
}
```
Returns `Uryyb Jbeyq`. Applying ROT13 again to the result returns the original text.

---

##### encode-unicode-escape
Convert Unicode characters to their escape sequences (e.g., `\uXXXX`).

**Required fields:** `text` - the text containing Unicode characters

**Example:**
```json
{
  "action": "encode-unicode-escape",
  "text": "Caf\u00e9 \u2603"
}
```

---

##### encode-unicode-unescape
Convert Unicode escape sequences back to their original characters.

**Required fields:** `text` - the string containing `\uXXXX` escape sequences

**Example:**
```json
{
  "action": "encode-unicode-unescape",
  "text": "Caf\\u00e9 \\u2603"
}
```

---

#### Common Workflows

- **Prepare text for a URL query parameter:** Use `encode-url-encode` to safely encode user input before appending it to a URL.
- **Embed user content in HTML:** Use `encode-html-entity-encode` to prevent XSS or rendering issues when inserting text into HTML.
- **Store or transmit binary data as text:** Use `encode-base64-encode` to convert binary content to a text-safe format, and `encode-base64-decode` to restore it.
- **Inspect raw byte values:** Use `encode-text-to-hex` or `encode-text-to-binary` to see the byte-level representation of any string.
- **Simple text obfuscation:** Use `encode-rot13-encode` to lightly obscure text (e.g., hiding spoilers). Apply it twice to get the original back.

#### Important Notes

- All actions require the `text` field except `get_instructions`.
- Decoding actions will return an error if the input is not valid for the expected format (e.g., invalid Base64, non-hex characters, binary string not a multiple of 8 bits).
- Hex decoding automatically strips spaces, colons, and hyphens, so formats like `48:65:6c:6c:6f` or `48-65-6c-6c-6f` are accepted.
- ROT13 only rotates ASCII letters; digits, punctuation, and non-ASCII characters pass through unchanged.
- All text processing uses UTF-8 encoding.

## When To Use
- Use this skill for `Data Format Encoder` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: data format encoder, base64 encoding, base64 decoding, binary to text encoding, data url creation, encode base64 decode, text, encode base64 encode.
- Supported action names: `encode-base64-decode`, `encode-base64-encode`, `encode-binary-to-text`, `encode-escape-json`, `encode-hex-to-text`, `encode-html-entity-decode`, `encode-html-entity-encode`, `encode-rot13-encode`, `encode-text-to-binary`, `encode-text-to-hex`, `encode-unescape-json`, `encode-unicode-escape`, `encode-unicode-unescape`, `encode-url-decode`, `encode-url-encode`.

## Use Cases
- Base64 encoding
- base64 decoding
- binary to text encoding
- data URL creation
- API payload encoding
- file content encoding
- image base64 conversion
- URL encoding
- percent encoding
- query string encoding
- URL parameter escaping
- special character encoding
- URL decoding
- query string parsing
- percent decoding
- HTML entity encoding

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `15`.
x402 availability: not enabled for this product.

- `encode-base64-decode` (action slug: `encode-base64-decode`): Decode a Base64-encoded string back to plain text. Price: `5` credits. Parameters: `text`.
- `encode-base64-encode` (action slug: `encode-base64-encode`): Encode plain text to Base64 format. Price: `5` credits. Parameters: `text`.
- `encode-binary-to-text` (action slug: `encode-binary-to-text`): Convert an 8-bit binary string back to plain text. The binary string length must be a multiple of 8 bits. Price: `5` credits. Parameters: `text`.
- `encode-escape-json` (action slug: `encode-escape-json`): Escape special characters in text for safe embedding inside JSON strings (newlines, tabs, quotes, backslashes). Price: `5` credits. Parameters: `text`.
- `encode-hex-to-text` (action slug: `encode-hex-to-text`): Convert a hexadecimal string back to plain text. Spaces, colons, and hyphens between hex bytes are automatically removed. Price: `5` credits. Parameters: `text`.
- `encode-html-entity-decode` (action slug: `encode-html-entity-decode`): Convert HTML entities back to their original characters. Price: `5` credits. Parameters: `text`.
- `encode-html-entity-encode` (action slug: `encode-html-entity-encode`): Escape special HTML characters into HTML entities (e.g., < becomes &lt;). Price: `5` credits. Parameters: `text`.
- `encode-rot13-encode` (action slug: `encode-rot13-encode`): Apply the ROT13 substitution cipher to text. ROT13 is its own inverse — apply it again to decode. Price: `5` credits. Parameters: `text`.
- `encode-text-to-binary` (action slug: `encode-text-to-binary`): Convert text to its 8-bit binary representation (space-separated bytes). Price: `5` credits. Parameters: `text`.
- `encode-text-to-hex` (action slug: `encode-text-to-hex`): Convert text to its hexadecimal byte representation. Price: `5` credits. Parameters: `text`.
- `encode-unescape-json` (action slug: `encode-unescape-json`): Convert JSON-escaped sequences back to their original characters. Price: `5` credits. Parameters: `text`.
- `encode-unicode-escape` (action slug: `encode-unicode-escape`): Convert Unicode characters to their escape sequences (\uXXXX format). Price: `5` credits. Parameters: `text`.
- `encode-unicode-unescape` (action slug: `encode-unicode-unescape`): Convert Unicode escape sequences back to their original characters. Price: `5` credits. Parameters: `text`.
- `encode-url-decode` (action slug: `encode-url-decode`): Decode a percent-encoded (URL-encoded) string back to plain text. Price: `5` credits. Parameters: `text`.
- `encode-url-encode` (action slug: `encode-url-encode`): Percent-encode text for safe use in URLs (query strings, path segments). Price: `5` credits. Parameters: `text`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "data-format-encoder"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "data-format-encoder"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "data-format-encoder"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "data-format-encoder"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "data-format-encoder"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "data-format-encoder"
  }
}
```

## Call This Tool
Product slug: `data-format-encoder`

Marketplace page: https://www.agentpmt.com/marketplace/data-format-encoder

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
    "name": "Data-Format-Encoder",
    "arguments": {
      "action": "encode-base64-decode",
      "text": "example text"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "data-format-encoder",
  "parameters": {
    "action": "encode-base64-decode",
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
- If `encode-base64-decode` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/data-format-encoder
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
