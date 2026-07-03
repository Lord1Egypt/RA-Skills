---
name: binary-to-from-file-converter
description: "Binary To/From File Converter: Convert between base64, hex, and binary. Use when an agent needs binary to/from file converter, binary to from file converter, encoding image or document uploads for api transmission in multi agent pipelines, decoding base64 email attachments and converting them to downloadable files, analyzing binary file signatures by converting file headers to hexadecimal for format detection, preparing binary payloads for webhook integrations that require hex or base64."
version: 1.0.1
homepage: https://www.agentpmt.com/marketplace/binary-to-from-file-converter
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/binary-to-from-file-converter"}}
---
# Binary To/From File Converter

## Freshness
Last updated: `2026-06-29`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Versatile data transformation utility that enables seamless conversion between various binary encoding formats and file storage operations. This function supports six core conversion actions: base64-to-hex, hex-to-base64, base64-to-binary, binary-to-base64, file-to-base64, and base64-to-file. For encoding transformations, users simply provide an input string in the source format and receive the converted output along with metadata such as byte size. The file-based operations integrate with cloud storage, allowing users to either extract base64-encoded content from existing stored files or create new files from base64 data with customizable filenames, MIME types, and expiration periods ranging from one to seven days. The function handles files up to 10MB for inline base64 returns and automatically generates signed URLs for secure file access. With built-in validation for all encoding formats and budget-based access controls, the File Binary Converter provides a reliable foundation for any workflow requiring binary data manipulation or format interoperability.

## Product Instructions
### Binary To/From File Converter

Convert data between base64, hexadecimal, and binary string representations, and convert files to/from base64 encoding.

#### Actions

##### base64-to-hex
Convert a base64-encoded string to hexadecimal.

**Required fields:**
- `action`: `"base64-to-hex"`
- `input`: Base64-encoded string

**Example:**
```json
{
  "action": "base64-to-hex",
  "input": "SGVsbG8gV29ybGQ="
}
```
Returns: `{ "encoding": "hex", "hex": "48656c6c6f20576f726c64", "size_bytes": 11 }`

---

##### hex-to-base64
Convert a hexadecimal string to base64 encoding.

**Required fields:**
- `action`: `"hex-to-base64"`
- `input`: Hexadecimal string (even number of characters, 0-9 and a-f)

**Example:**
```json
{
  "action": "hex-to-base64",
  "input": "48656c6c6f20576f726c64"
}
```
Returns: `{ "encoding": "base64", "base64": "SGVsbG8gV29ybGQ=", "size_bytes": 11 }`

---

##### base64-to-binary
Convert a base64-encoded string to a binary (0s and 1s) string representation.

**Required fields:**
- `action`: `"base64-to-binary"`
- `input`: Base64-encoded string

**Example:**
```json
{
  "action": "base64-to-binary",
  "input": "SGk="
}
```
Returns: `{ "encoding": "binary", "binary": "01001000 01101001", "size_bytes": 2 }`

---

##### binary-to-base64
Convert a binary string (0s and 1s) back to base64 encoding.

**Required fields:**
- `action`: `"binary-to-base64"`
- `input`: Binary string of 0s and 1s (length must be a multiple of 8; spaces between bytes are allowed)

**Example:**
```json
{
  "action": "binary-to-base64",
  "input": "01001000 01101001"
}
```
Returns: `{ "encoding": "base64", "base64": "SGk=", "size_bytes": 2 }`

---

##### file-to-base64
Read a previously uploaded file and return its contents as a base64-encoded string.

**Required fields:**
- `action`: `"file-to-base64"`
- `file_id`: The file ID of an uploaded file

**Example:**
```json
{
  "action": "file-to-base64",
  "file_id": "abc123def456"
}
```
Returns: `{ "file_id": "abc123def456", "filename": "report.pdf", "content_type": "application/pdf", "size_bytes": 4096, "base64": "..." }`

---

##### base64-to-file
Decode a base64 string and save it as a file in cloud storage.

**Required fields:**
- `action`: `"base64-to-file"`
- `input`: Base64-encoded file content
- `filename`: Name for the created file (e.g., `"output.png"`)

**Optional fields:**
- `content_type`: MIME type for the file (default: `"application/octet-stream"`). Use the appropriate type, e.g., `"image/png"`, `"application/pdf"`.
- `expiration_days`: Number of days until the file expires, 1-7 (default: 7)

**Example:**
```json
{
  "action": "base64-to-file",
  "input": "iVBORw0KGgo...",
  "filename": "screenshot.png",
  "content_type": "image/png",
  "expiration_days": 3
}
```
Returns: `{ "file_id": "...", "filename": "screenshot.png", "content_type": "image/png", "size_bytes": 2048, "signed_url": "https://...", "signed_url_expires_in": "..." }`

---

#### Common Workflows

1. **Encode a file for transmission**: Use `file-to-base64` to get a file's base64 content, then share or embed it.
2. **Reconstruct a file from base64 data**: Use `base64-to-file` to decode received base64 data back into a downloadable file.
3. **Inspect binary content**: Chain `file-to-base64` then `base64-to-hex` or `base64-to-binary` to view raw byte contents of a file.
4. **Convert between encodings**: Use any combination of the encoding actions to translate between base64, hex, and binary formats.

#### Important Notes

- File size limit for `file-to-base64` is 10 MB. Larger files cannot be returned inline.
- Binary strings must have a length that is a multiple of 8 (one complete byte per group). Spaces between byte groups are allowed.
- Hex strings must have an even number of characters.
- Files created with `base64-to-file` are stored in cloud storage and expire after the specified number of days (default 7).
- The `signed_url` returned by `base64-to-file` provides a temporary download link for the created file.

## When To Use
- Use this skill for `Binary To/From File Converter` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: binary to/from file converter, binary to from file converter, encoding image or document uploads for api transmission in multi agent pipelines, decoding base64 email attachments and converting them to downloadable files, analyzing binary file signatures by converting file headers to hexadecimal for format detection, preparing binary payloads for webhook integrations that require hex or base64 encoding, base64 to binary, input.
- Supported action names: `base64-to-binary`, `base64-to-file`, `base64-to-hex`, `binary-to-base64`, `file-to-base64`, `hex-to-base64`.

## Use Cases
- Encoding image or document uploads for API transmission in multi-agent pipelines
- decoding base64 email attachments and converting them to downloadable files
- analyzing binary file signatures by converting file headers to hexadecimal for format detection
- preparing binary payloads for webhook integrations that require hex or base64 encoding
- converting cryptographic hashes between hex and base64 for cross-system compatibility
- extracting and re-encoding embedded binary assets from JSON or XML data feeds
- building file export workflows that package generated content into downloadable cloud-stored files
- debugging binary protocols by converting raw data to human-readable binary strings
- migrating encoded data between systems with different encoding standards
- creating temporary secure file links from base64 data for sharing in automated notification workflows

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `6`.
x402 availability: not enabled for this product.

- `base64-to-binary` (action slug: `base64-to-binary`): Convert a base64-encoded string to a binary (0s and 1s) string representation. Price: `10` credits. Parameters: `input`.
- `base64-to-file` (action slug: `base64-to-file`): Decode a base64 string and save it as a file in cloud storage with a signed download URL. Price: `10` credits. Parameters: `content_type`, `expiration_days`, `filename`, `input`, `store_file`.
- `base64-to-hex` (action slug: `base64-to-hex`): Convert a base64-encoded string to hexadecimal representation. Price: `10` credits. Parameters: `input`.
- `binary-to-base64` (action slug: `binary-to-base64`): Convert a binary string (0s and 1s) back to base64 encoding. Price: `10` credits. Parameters: `input`.
- `file-to-base64` (action slug: `file-to-base64`): Read a previously uploaded file from cloud storage and return its contents as a base64-encoded string. Maximum file size is 10MB. Price: `10` credits. Parameters: `file_id`.
- `hex-to-base64` (action slug: `hex-to-base64`): Convert a hexadecimal string to base64 encoding. Price: `10` credits. Parameters: `input`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "binary-to-from-file-converter"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "binary-to-from-file-converter"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "binary-to-from-file-converter"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "binary-to-from-file-converter"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "binary-to-from-file-converter"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "binary-to-from-file-converter"
  }
}
```

## Call This Tool
Product slug: `binary-to-from-file-converter`

Marketplace page: https://www.agentpmt.com/marketplace/binary-to-from-file-converter

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
    "name": "Binary-ToFrom-File-Converter",
    "arguments": {
      "action": "base64-to-binary",
      "input": "example input"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "binary-to-from-file-converter",
  "parameters": {
    "action": "base64-to-binary",
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
- If `base64-to-binary` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/binary-to-from-file-converter
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
