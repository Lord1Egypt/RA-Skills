---
name: file-management
description: "File Management: Upload and manage files in one tool: upload_standard, upload_large, list with previews, get signed URLs, download, delete, share, update metadata, inspect access history, and extend expiration. Use when an agent needs file management, small file upload, large file upload, signed upload url generation, temporary file hosting, access history, file id, limit through AgentPMT-hosted remote tool calls. Discovery terms: file management, small file upload, large file upload."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/file-management
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/file-management"}}
---
# File Management

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Upload, list, retrieve, share, download, delete, and manage files stored in AgentPMT cloud storage. This product now owns the full file lifecycle, including signed upload URLs for files up to 10MB and for files over 10MB up to 100MB, budget-scoped file listing with preview URLs, fresh signed download URLs, direct base64 download for smaller files, password-protected sharing, metadata and tag updates, access-history inspection, and expiration extension. All file operations are scoped to the current budget for isolation and are designed to let one budget create persistent files that can be revisited across later agent runs.

## Product Instructions
### File Management

Manage the complete file lifecycle from a single tool. This includes uploading new files, listing existing files for the current budget, retrieving metadata and signed URLs, downloading content, deleting files, creating password-protected share links, auditing access history, updating metadata and tags, and extending expiration.

#### Actions

##### `upload_standard`
Generate a signed upload URL for a file up to 10MB.

Required fields:
- `content_length_bytes`: exact file size in bytes, 1 to 10,485,760

Optional fields:
- `filename`
- `content_type`
- `expiration_days` (1-7)
- `shared`
- `password_max_uses` (1-10)
- `password_max_minutes` (1-10)
- `metadata`
- `tags`

##### `upload_large`
Generate a signed upload URL for a file over 10MB and up to 100MB.

Required fields:
- `content_length_bytes`: exact file size in bytes, greater than 10,485,760 and up to 104,857,600

Optional fields:
- `filename`
- `content_type`
- `expiration_days` (1-7)
- `shared`
- `password_max_uses` (1-10)
- `password_max_minutes` (1-10)
- `metadata`
- `tags`

##### `list`
List active files for the current budget. Results are newest first and include preview URLs when available.

Optional fields:
- `tags`
- `date_from`
- `date_to`
- `limit`
- `offset`
- `url_expiration_minutes`

##### `get`
Get metadata and a fresh signed download URL for a file.

Required fields:
- `file_id`

Optional fields:
- `url_expiration_minutes`

##### `download`
Download base64 content for files up to 5MB, or get a signed URL for larger files.

Required fields:
- `file_id`

Optional fields:
- `return_content`
- `url_expiration_minutes`

##### `delete`
Delete a file permanently.

Required fields:
- `file_id`

##### `share`
Create or refresh a password-protected public share link.

Required fields:
- `file_id`

Optional fields:
- `password_max_uses`
- `password_max_minutes`

##### `access_history`
View share access history for a file.

Required fields:
- `file_id`

Optional fields:
- `limit`

##### `update_metadata`
Update metadata and tags on a file.

Required fields:
- `file_id`

Optional fields:
- `metadata`
- `tags`
- `add_tags`
- `remove_tags`

##### `extend_expiration`
Extend expiration by 7 days.

Required fields:
- `file_id`

#### Notes
- Upload actions return a signed `upload_url`; you must then PUT the file bytes to that URL using the returned headers.
- `list` is budget-scoped and includes preview URLs when the file type supports preview.
- Signed URLs can be requested for up to 7 days.
- `download` with `return_content: true` is limited to files 5MB or smaller.
- Share passwords are always auto-generated.
- `extend_expiration` adds 7 days each time it is called.

## When To Use
- Use this skill for `File Management` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: file management, small file upload, large file upload, signed upload url generation, temporary file hosting, access history, file id, limit.
- Supported action names: `access_history`, `delete`, `download`, `extend_expiration`, `get`, `list`, `share`, `update_metadata`, `upload_large`, `upload_standard`.

## Use Cases
- Small file upload
- large file upload
- signed upload URL generation
- temporary file hosting
- budget-scoped file storage
- file inventory
- file preview listing
- image preview retrieval
- get file metadata
- refresh signed URL
- download file as base64
- delete uploaded file
- create password-protected file share
- secure file delivery
- metadata tagging
- file organization

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `10`.
x402 action routes are enabled and listed in `./schema.md`.

- `access_history` (action slug: `access-history`): View password-protected share access history for a file. Price: `0` credits. Parameters: `file_id`, `limit`.
- `delete` (action slug: `delete`): Permanently delete a file from storage. Price: `0` credits. Parameters: `file_id`.
- `download` (action slug: `download`): Download file content as base64 for files up to 5MB, or return a signed URL for larger files. Price: `0` credits. Parameters: `file_id`, `return_content`, `url_expiration_minutes`.
- `extend_expiration` (action slug: `extend-expiration`): Extend a file's expiration date by 7 days from the current expiration. Price: `10` credits. Parameters: `file_id`.
- `get` (action slug: `get`): Get file metadata and a fresh signed download URL for a specific file. Price: `0` credits. Parameters: `file_id`, `url_expiration_minutes`.
- `list` (action slug: `list`): List active uploaded files for the current budget with optional filtering and pagination. Returns newest files first and includes cached preview URLs when available. Price: `0` credits. Parameters: `date_from`, `date_to`, `limit`, `offset`, `tags`, `url_expiration_minutes`.
- `share` (action slug: `share`): Create or refresh a password-protected public share link for an existing file. Price: `5` credits. Parameters: `file_id`, `password_max_minutes`, `password_max_uses`.
- `update_metadata` (action slug: `update-metadata`): Update metadata and tags on a file. Price: `5` credits. Parameters: `add_tags`, `file_id`, `metadata`, `remove_tags`, `tags`.
- `upload_large` (action slug: `upload-large`): Generate a signed upload URL for a file over 10MB and up to 100MB. After receiving the URL, perform a PUT request with the exact file bytes and returned headers. Price: `20` credits. Parameters: `content_length_bytes`, `content_type`, `expiration_days`, `filename`, `metadata`, `password_max_minutes`, `password_max_uses`, `shared`, plus 1 more.
- `upload_standard` (action slug: `upload-standard`): Generate a signed upload URL for a file up to 10MB. After receiving the URL, perform a PUT request with the exact file bytes and returned headers. Price: `10` credits. Parameters: `content_length_bytes`, `content_type`, `expiration_days`, `filename`, `metadata`, `password_max_minutes`, `password_max_uses`, `shared`, plus 1 more.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "file-management"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "file-management"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "file-management"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "file-management"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "file-management"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "file-management"
  }
}
```

## Call This Tool
Product slug: `file-management`

Marketplace page: https://www.agentpmt.com/marketplace/file-management

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- No-account x402 route: first use `../agentpmt-no-account-agentaddress-x402` to create an AgentAddress and prepare the x402 payment flow.
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
    "name": "File-Management",
    "arguments": {
      "action": "access_history",
      "file_id": "example file id",
      "limit": 1
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "file-management",
  "parameters": {
    "action": "access_history",
    "file_id": "example file id",
    "limit": 1
  }
}
```

Use the setup skill for the account connection details before making REST calls.

x402 action path: `POST https://www.agentpmt.com/api/external/tools/file-management/actions/access-history/invoke`.

x402 wallet scope:

- Direct x402 calls are scoped to the payer wallet that signs the payment authorization.
- Files created through File Manager during x402 calls are owned by that wallet scope.
- Reuse the same payer wallet for later x402 calls when listing, fetching, downloading, or passing those files between AgentPMT tools.
- File Manager files normally expire after the retention window, up to 7 days, unless the file action returns a shorter expiration.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `access_history` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- No-account AgentAddress/x402 setup: ../agentpmt-no-account-agentaddress-x402 (ClawHub: `agentpmt-no-account-agentaddress-x402`, page: https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-no-account-agentaddress-x402`)
- Marketplace product: https://www.agentpmt.com/marketplace/file-management
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
