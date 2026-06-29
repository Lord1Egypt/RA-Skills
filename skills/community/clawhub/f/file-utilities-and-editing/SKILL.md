---
name: file-utilities-and-editing
description: "File Utilities and Editing: File utilities: MIME type detection, path parsing/joining, CSV to ASCII table, JSON formatting, Base64 encoding, hash generation (MD5, SHA). Use when an agent needs file utilities and editing, mime type detection, file type identification, content type lookup, extension to mime, file base64 decode, input, file base64 encode through AgentPMT-hosted remote tool calls. Discovery terms: file utilities and editing, mime type detection, file type identification."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/file-utilities-and-editing
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/file-utilities-and-editing"}}
---
# File Utilities and Editing

## Freshness
Last updated: `2026-06-11`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
A utility for file metadata operations, path manipulation, and content formatting commonly needed when working with files in automation workflows and application development. MIME type detection identifies the content type of files based on filename extensions, covering documents, images, audio, video, archives, and programming languages, while reverse lookup finds appropriate file extensions for a given MIME type. File size formatting converts byte counts into human-readable strings with automatic unit scaling from bytes through petabytes. Path manipulation functions parse file paths into components including directory, filename, name, and extension, join multiple path segments with proper separators, and normalize paths by resolving relative references and redundant separators. CSV to table conversion parses comma-separated data and formats it as an ASCII table with aligned columns for display purposes, also returning structured header and row data. JSON formatting includes pretty printing with configurable indentation for readability and minification that removes all unnecessary whitespace with size reduction statistics. Base64 encoding and decoding handles text-to-base64 conversion for data embedding and transmission. Cryptographic hash generation supports MD5, SHA-1, SHA-256, and SHA-512 algorithms for content integrity verification and fingerprinting.

## Product Instructions
### File Utilities and Editing

#### Overview
A collection of file utility operations for working with MIME types, file paths, content formatting (CSV/JSON), base64 encoding/decoding, and cryptographic hashing. Use this tool when you need to manipulate file metadata, transform data formats, or generate hashes without touching the filesystem.

#### Actions

##### `file-mime-type-detect`
Detects the MIME type of a file based on its filename/extension. Supports documents, images, audio, video, archives, and programming languages.

**Required fields:**
- `input` (string) — The filename to analyze (e.g., `report.pdf`, `photo.jpg`)

**Example:**
```json
{
  "action": "file-mime-type-detect",
  "input": "quarterly-report.xlsx"
}
```
Returns the MIME type (`application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`), file extension, and category (`application`).

---

##### `file-extension-from-mime`
Looks up the standard file extension for a given MIME type.

**Required fields:**
- `input` (string) — A MIME type string (e.g., `image/png`, `application/pdf`)

**Example:**
```json
{
  "action": "file-extension-from-mime",
  "input": "audio/mpeg"
}
```
Returns the matching extension (`.mp3`) and whether a match was found.

---

##### `file-size-format`
Converts a raw byte count into a human-readable size string (KB, MB, GB, etc.).

**Required fields:**
- `input` (string) — File size in bytes as a string (e.g., `"5242880"`)

**Example:**
```json
{
  "action": "file-size-format",
  "input": "5242880"
}
```
Returns `"5.00 MB"` along with the numeric value and unit.

---

##### `file-path-parse`
Breaks a file path into its component parts: directory, filename, name, and extension.

**Required fields:**
- `input` (string) — A file path to parse (e.g., `/home/user/documents/report.pdf`)

**Example:**
```json
{
  "action": "file-path-parse",
  "input": "/home/user/documents/report.pdf"
}
```
Returns the directory (`/home/user/documents`), filename (`report.pdf`), name (`report`), extension (`.pdf`), and whether the path is absolute.

---

##### `file-path-join`
Joins multiple path components into a single path. You can provide components as a comma-separated string in `input`, or use the `input`, `input2`, and `input3` fields for up to three components.

**Required fields:**
- `input` (string) — First path component, or a comma-separated list of all components

**Optional fields:**
- `input2` (string) — Second path component (when not using comma separation)
- `input3` (string) — Third path component (when not using comma separation)

At least 2 path components are required.

**Example (comma-separated):**
```json
{
  "action": "file-path-join",
  "input": "/home/user, documents, report.pdf"
}
```

**Example (separate fields):**
```json
{
  "action": "file-path-join",
  "input": "/home/user",
  "input2": "documents",
  "input3": "report.pdf"
}
```
Returns the joined and normalized path (`/home/user/documents/report.pdf`).

---

##### `file-path-normalize`
Cleans up a messy file path by resolving `..`, `.`, and redundant separators.

**Required fields:**
- `input` (string) — A file path to normalize (e.g., `/home/user/../user/./documents//file.txt`)

**Example:**
```json
{
  "action": "file-path-normalize",
  "input": "/home/user/../user/./documents//file.txt"
}
```
Returns the cleaned path (`/home/user/documents/file.txt`).

---

##### `file-csv-to-table`
Parses CSV content and renders it as a formatted ASCII table. The first row is treated as headers.

**Required fields:**
- `input` (string) — CSV content as a string

**Example:**
```json
{
  "action": "file-csv-to-table",
  "input": "Name,Age,City\nAlice,30,New York\nBob,25,London\nCarol,35,Tokyo"
}
```
Returns the row count, column count, headers list, a formatted ASCII table, and the parsed data as structured arrays.

---

##### `file-json-pretty-print`
Formats a compact JSON string with indentation for readability.

**Required fields:**
- `input` (string) — A valid JSON string

**Optional fields:**
- `indent` (integer, default: 2) — Number of spaces per indentation level (0-8)

**Example:**
```json
{
  "action": "file-json-pretty-print",
  "input": "{\"name\":\"Alice\",\"age\":30,\"address\":{\"city\":\"New York\",\"zip\":\"10001\"}}",
  "indent": 4
}
```
Returns the formatted JSON string along with original and formatted lengths.

---

##### `file-json-minify`
Removes all unnecessary whitespace from a JSON string to produce the most compact representation.

**Required fields:**
- `input` (string) — A valid JSON string (can include whitespace/indentation)

**Example:**
```json
{
  "action": "file-json-minify",
  "input": "{\n  \"name\": \"Alice\",\n  \"age\": 30\n}"
}
```
Returns the minified JSON, original and minified lengths, and the percentage reduction in size.

---

##### `file-base64-encode`
Encodes a text string to base64 using UTF-8 encoding.

**Required fields:**
- `input` (string) — The text to encode

**Example:**
```json
{
  "action": "file-base64-encode",
  "input": "Hello, World! This is a secret message."
}
```
Returns the base64-encoded string along with original and encoded lengths.

---

##### `file-base64-decode`
Decodes a base64 string back to UTF-8 text.

**Required fields:**
- `input` (string) — A valid base64-encoded string

**Example:**
```json
{
  "action": "file-base64-decode",
  "input": "SGVsbG8sIFdvcmxkISBUaGlzIGlzIGEgc2VjcmV0IG1lc3NhZ2Uu"
}
```
Returns the decoded text along with encoded and decoded lengths.

---

##### `file-hash-generate`
Generates a cryptographic hash of the provided text content.

**Required fields:**
- `input` (string) — The content to hash

**Optional fields:**
- `hash_algorithm` (string, default: `"sha256"`) — Algorithm to use: `md5`, `sha1`, `sha256`, or `sha512`

**Example:**
```json
{
  "action": "file-hash-generate",
  "input": "This is the content of my document that I want to verify.",
  "hash_algorithm": "sha256"
}
```
Returns the hex-encoded hash digest, the algorithm used, content length, and hash length.

#### Common Workflows

##### Workflow 1: Validate and format incoming data
1. Use `file-mime-type-detect` with a received filename to confirm the file type
2. Use `file-size-format` to display the file size in a readable format
3. If the content is JSON, use `file-json-pretty-print` to format it for review

##### Workflow 2: Content integrity verification
1. Use `file-base64-decode` to decode a received base64 payload
2. Use `file-hash-generate` to compute a SHA-256 hash of the decoded content
3. Compare the hash against an expected value to verify integrity

##### Workflow 3: Build and normalize file paths
1. Use `file-path-join` to combine directory and filename components
2. Use `file-path-normalize` to clean up the resulting path
3. Use `file-path-parse` to extract individual components for further processing

#### Important Notes
- All operations are stateless text transformations. This tool does not read from or write to the filesystem.
- The `input` field must always be provided as a string, even for numeric values like file sizes.
- CSV parsing treats the first row as column headers.
- JSON operations (`pretty-print` and `minify`) will return an error if the input is not valid JSON.
- Base64 encoding/decoding uses UTF-8. Binary data that is not valid UTF-8 cannot be decoded with `file-base64-decode`.
- Unknown file extensions default to the MIME type `application/octet-stream`.
- The `indent` parameter only applies to `file-json-pretty-print` and must be between 0 and 8.

## When To Use
- Use this skill for `File Utilities and Editing` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: file utilities and editing, mime type detection, file type identification, content type lookup, extension to mime, file base64 decode, input, file base64 encode.
- Supported action names: `file-base64-decode`, `file-base64-encode`, `file-csv-to-table`, `file-extension-from-mime`, `file-hash-generate`, `file-json-minify`, `file-json-pretty-print`, `file-mime-type-detect`, `file-path-join`, `file-path-normalize`, `file-path-parse`, `file-size-format`.

## Use Cases
- MIME type detection
- file type identification
- content type lookup
- extension to MIME
- MIME to extension
- file extension lookup
- file size formatting
- byte size conversion
- human readable file size
- KB MB GB formatting
- storage size display
- file path parsing
- path component extraction
- directory extraction
- filename extraction
- extension extraction

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `12`.
x402 availability: not enabled for this product.

- `file-base64-decode` (action slug: `file-base64-decode`): Decode a base64 string back to UTF-8 text. Price: `5` credits. Parameters: `input`.
- `file-base64-encode` (action slug: `file-base64-encode`): Encode a text string to base64 using UTF-8 encoding. Price: `5` credits. Parameters: `input`.
- `file-csv-to-table` (action slug: `file-csv-to-table`): Parse CSV content and render it as a formatted ASCII table. The first row is treated as headers. Price: `5` credits. Parameters: `input`.
- `file-extension-from-mime` (action slug: `file-extension-from-mime`): Look up the standard file extension for a given MIME type. Price: `5` credits. Parameters: `input`.
- `file-hash-generate` (action slug: `file-hash-generate`): Generate a cryptographic hash of the provided text content. Price: `5` credits. Parameters: `hash_algorithm`, `input`.
- `file-json-minify` (action slug: `file-json-minify`): Remove all unnecessary whitespace from a JSON string to produce the most compact representation. Price: `5` credits. Parameters: `input`.
- `file-json-pretty-print` (action slug: `file-json-pretty-print`): Format a compact JSON string with indentation for readability. Price: `5` credits. Parameters: `indent`, `input`.
- `file-mime-type-detect` (action slug: `file-mime-type-detect`): Detect the MIME type of a file based on its filename/extension. Supports documents, images, audio, video, archives, and programming languages. Price: `5` credits. Parameters: `input`.
- `file-path-join` (action slug: `file-path-join`): Join multiple path components into a single path. Provide components as a comma-separated string in input, or use input, input2, and input3 fields for up to three components. At least 2 components required. Price: `5` credits. Parameters: `input`, `input2`, `input3`.
- `file-path-normalize` (action slug: `file-path-normalize`): Clean up a file path by resolving '..', '.', and redundant separators. Price: `5` credits. Parameters: `input`.
- `file-path-parse` (action slug: `file-path-parse`): Break a file path into its component parts: directory, filename, name, and extension. Price: `5` credits. Parameters: `input`.
- `file-size-format` (action slug: `file-size-format`): Convert a raw byte count into a human-readable size string (KB, MB, GB, etc.). Price: `5` credits. Parameters: `input`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "file-utilities-and-editing"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "file-utilities-and-editing"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "file-utilities-and-editing"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "file-utilities-and-editing"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "file-utilities-and-editing"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "file-utilities-and-editing"
  }
}
```

## Call This Tool
Product slug: `file-utilities-and-editing`

Marketplace page: https://www.agentpmt.com/marketplace/file-utilities-and-editing

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
    "name": "File-Utilities-and-Editing",
    "arguments": {
      "action": "file-base64-decode",
      "input": "example input"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "file-utilities-and-editing",
  "parameters": {
    "action": "file-base64-decode",
    "input": "example input"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `file-base64-decode` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/file-utilities-and-editing
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
