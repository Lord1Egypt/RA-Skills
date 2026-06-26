---
name: alchemyst-mcp
description: >
  Use this skill whenever you need to store, retrieve, search, or view persistent context
  using the Alchemyst AI MCP server at mcp.getalchemystai.com/mcp/sse. Triggers include:
  requests to "remember" or "recall" information across sessions, storing documents/notes/decisions
  for later retrieval, searching project knowledge, or any task that involves reading from or
  writing to Alchemyst's context store.
---

# Alchemyst AI MCP — Context Engine

## Overview

Alchemyst AI is a **persistent context layer** for AI applications. It stores documents,
conversations, and structured knowledge externally so they can be retrieved on demand — across
sessions, tools, and environments.

The MCP server is exposed as an SSE (Server-Sent Events) endpoint:

```
https://mcp.getalchemystai.com/mcp/sse
```

Authentication is done via a **Bearer token** (your Alchemyst API key) passed as a request header.

---

## Prerequisites

| Requirement | Detail |
|---|---|
| **Alchemyst API key** | Obtain from [platform.getalchemystai.com](https://platform.getalchemystai.com) |
| **MCP-compatible client** | Claude Desktop, Cursor, VS Code + MCP extension, or custom agent |
| **Transport** | SSE (`https://mcp.getalchemystai.com/mcp/sse`) |
| **Auth header** | `Authorization: Bearer <YOUR_API_KEY>` |

---

## Claude Desktop Configuration

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "alchemyst": {
      "url": "https://mcp.getalchemystai.com/mcp/sse",
      "headers": {
        "Authorization": "Bearer YOUR_ALCHEMYST_API_KEY"
      }
    }
  }
}
```

> **Never commit your API key.** Use an environment variable or secrets manager in production.

---

## Tools

The server exposes exactly four tools:

---

### `alchemyst_ai_search_context` — Semantic Search

Search the context store using a natural-language query. Returns documents ranked by semantic
similarity.

**When to use:** Before answering a question that might rely on stored knowledge; retrieving prior
decisions, docs, or instructions without manual lookup.

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `query` | `string` | ✅ | Natural-language search query |
| `similarity_threshold` | `number` (0–1) | ✅ | Maximum similarity threshold — results at or below this score are returned |
| `minimum_similarity_threshold` | `number` (0–1) | ✅ | Floor — results below this score are excluded |
| `scope` | `"internal"` \| `"external"` | ❌ | Search scope; defaults to `"internal"` |
| `metadata` | `object` \| `null` | ❌ | Optional filter by file metadata; defaults to `null` |

**Metadata filter fields** (all required if metadata object is provided):

| Field | Type | Description |
|---|---|---|
| `fileName` | `string` | Name of file to filter by |
| `fileSize` | `number` | File size in bytes |
| `fileType` | `string` | MIME type |
| `lastModified` | `string` | ISO 8601 datetime string |
| `groupName` | `string[]` | Tag groups; defaults to `["default"]` |

> **Note:** Metadata field names use **camelCase** in the search tool (`fileName`, `fileSize`,
> `fileType`, `lastModified`, `groupName`).

#### Threshold Guidance

- `similarity_threshold: 0.8` + `minimum_similarity_threshold: 0.5` → tight, precise results
- `similarity_threshold: 0.7` + `minimum_similarity_threshold: 0.4` → broader, more permissive
- Always set `minimum_similarity_threshold` lower than `similarity_threshold`

#### Example Call

```json
{
  "query": "authentication token expiry policy",
  "similarity_threshold": 0.8,
  "minimum_similarity_threshold": 0.5,
  "scope": "internal",
  "metadata": null
}
```

---

### `alchemyst_ai_add_context` — Store Context

Add one or more documents to the Alchemyst context store.

**When to use:** Saving project requirements, architectural decisions, onboarding docs, meeting
notes, code conventions, or any knowledge you want to persist and retrieve later.

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `user_id` | `string` | ✅ | Unique identifier of the user submitting context |
| `organization_id` | `string` \| `null` | ✅ | Organization ID; pass `null` if not applicable |
| `documents` | `array` | ✅ | Array of document objects, each with a `content` string field (plus optional extra string fields) |
| `source` | `string` | ✅ | Label describing where this context came from (e.g., `"project.auth.decisions"`) |
| `context_type` | `"resource"` \| `"conversation"` \| `"instruction"` | ✅ | Type of context being stored |
| `metadata` | `object` | ✅ | File metadata — all four fields required |
| `scope` | `"internal"` \| `"external"` | ❌ | Defaults to `"internal"` |

**Metadata fields** (all required; note **snake_case** here, unlike the search tool):

| Field | Type | Description |
|---|---|---|
| `file_name` | `string` | Name of the file or document |
| `doc_type` | `string` | MIME type or document type (e.g., `"text/markdown"`) |
| `modalities` | `string[]` | Modalities present (e.g., `["text"]`, `["text", "image"]`) |
| `size` | `number` | Size in bytes |

> ⚠️ **Key naming difference:** `add_context` uses **snake_case** metadata keys (`file_name`,
> `doc_type`, `size`), while `search_context` uses **camelCase** (`fileName`, `fileType`,
> `fileSize`). Match the case to the tool you're calling.

#### Context Types

| Value | Use for |
|---|---|
| `"resource"` | Files, documents, reference material, code |
| `"conversation"` | Chat history, meeting transcripts, support threads |
| `"instruction"` | Persistent rules, conventions, agent instructions |

#### Source Naming Convention

Use dot-separated hierarchical labels. This makes auditing straightforward:

```
project.auth.decisions
team.onboarding.v2
agent.instructions.sales
```

#### Example Call

```json
{
  "user_id": "user_abc123",
  "organization_id": "org_xyz",
  "documents": [
    { "content": "All API routes use JWT auth with 15-minute token expiry." }
  ],
  "source": "project.auth.decisions",
  "context_type": "resource",
  "scope": "internal",
  "metadata": {
    "file_name": "auth-decisions.md",
    "doc_type": "text/markdown",
    "modalities": ["text"],
    "size": 64
  }
}
```

---

### `alchemyst_ai_context_mcp_view_context` — View Context Summary

Retrieve a summary of all stored context for a given user and organization.

**When to use:** Auditing what's in the context store, debugging missing context, or checking
what knowledge is available before a session.

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `user_id` | `string` | ✅ | User ID to get context for |
| `organization_id` | `string` \| `null` | ✅ | Organization ID; pass `null` if not applicable |

#### Example Call

```json
{
  "user_id": "user_abc123",
  "organization_id": "org_xyz"
}
```

---

### `alchemyst_ai_context_mcp_view_docs` — View Stored Documents

Retrieve the actual documents stored in the context store for a given user and organization.

**When to use:** Listing stored documents, verifying content was saved correctly, or browsing
available knowledge before deciding what to add.

#### Input Schema

| Field | Type | Required | Description |
|---|---|---|---|
| `user_id` | `string` | ✅ | User ID to get documents for |
| `organization_id` | `string` \| `null` | ✅ | Organization ID; pass `null` if not applicable |

#### Example Call

```json
{
  "user_id": "user_abc123",
  "organization_id": "org_xyz"
}
```

---

## Workflow Patterns

### Store → Search (basic memory pattern)

1. Call `alchemyst_ai_add_context` to store a document
2. Later, call `alchemyst_ai_search_context` with a relevant query to retrieve it
3. Inject the retrieved content into your prompt as context

### Audit before adding

1. Call `alchemyst_ai_context_mcp_view_docs` to inspect what's already stored
2. Only call `alchemyst_ai_add_context` if the knowledge isn't already present
3. This avoids duplicating context and keeps the store clean

### Pre-answer retrieval

Before answering any question that might depend on project-specific knowledge, call
`alchemyst_ai_search_context` first. Prefer doing this proactively — don't wait for the user to
explicitly ask "check the context store."

---

## Best Practices

**Always populate metadata.** The `metadata` object is required on `add_context` — populate all
four fields every time. Missing metadata degrades retrieval quality significantly.

**Chunk large documents.** Break large files into logical sections before adding. Each chunk
should be independently meaningful. Don't split mid-sentence or mid-concept.

**Version your sources.** When content evolves, use versioned source labels
(`project.arch.v1`, `project.arch.v2`) rather than re-adding to the same source. This preserves
history.

**Search before storing.** Run a search first to check whether similar content already exists
before calling `add_context`. Avoid accumulating duplicates.

**Mind the camelCase/snake_case split.** The metadata schema differs between tools — this is a
quirk of the current API. Double-check field names when building payloads:
- `add_context` → `file_name`, `doc_type`, `size` (snake_case)
- `search_context` → `fileName`, `fileType`, `fileSize` (camelCase)

**Pass `organization_id` explicitly.** Even when there's no org, pass `null` rather than
omitting the field — it's required by the schema.

---

## Error Handling

| Status | Meaning | Action |
|---|---|---|
| 400 | Bad request | Check required fields; verify `documents` is an array; check metadata schema |
| 401 | Auth failure | Verify API key; confirm header is `Authorization: Bearer <key>` |
| 403 | Permission denied | Check org/user scope permissions |
| 404 | Not found | Confirm the `user_id` or `organization_id` is valid |
| 422 | Unprocessable entity | Schema validation failed — check field types, required fields, and camelCase vs snake_case |
| 429 | Rate limit | Back off exponentially; retry after delay |
| 500+ | Server error | Retry twice with backoff; check [status.getalchemystai.com](https://status.getalchemystai.com) |

---

## Resources

- Docs: [getalchemystai.com/docs](https://getalchemystai.com/docs)
- MCP overview: [getalchemystai.com/docs/mcps/introduction](https://getalchemystai.com/docs/mcps/introduction)
- Claude Desktop setup: [getalchemystai.com/docs/mcps/claude-desktop](https://getalchemystai.com/docs/mcps/claude-desktop)
- API status: [status.getalchemystai.com](https://status.getalchemystai.com)
- Python SDK: `pip install alchemystai`
- Support: anuran@getalchemystai.com