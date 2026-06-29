---
name: bcms-content
description: >
  Run BCMS content operations from the command line. A thin CLI (wrapping the official
  @thebcms/client SDK) for agents to create, update, delete, and list entries and upload
  media using a single API key — the same three-part key used for the BCMS MCP. Use this
  for scripted, deterministic content tasks in terminals, CI, and agent workflows.
---

# BCMS Content CLI

**Canonical copy:** edit this file at `ai/skills/bcms-content/SKILL.md`. The Claude Code and Cursor plugins package the same file via symlinks under `ai/providers/*/plugin/skills/bcms-content/`.

This skill ships a small executable CLI (`cli/bcms.mjs`) for **content operations**: create / update / delete / list entries and upload media. It wraps the official **`@thebcms/client`** SDK so entry `meta` is converted to the raw props the backend expects (raw REST calls do not do this).

For content **modeling**, SDK usage in application code, framework integrations, and the MCP server, use the companion **`bcms`** skill. Use this `bcms-content` skill when you want to *run a command and get a result* rather than write app code.

**Setup guide:** [thebcms.com/agents](https://thebcms.com/agents) — MCP connection, skill install, and CLI examples.

## Setup (once)

1. **Install dependencies** in this skill folder (it has its own `package.json` with one dependency):

```bash
npm install
```

2. **Provide an API key** — the same three-part key (`keyId.secret.instanceId`) used for the BCMS MCP. The key must have content permissions for the templates/media you target.

```bash
export BCMS_API_KEY="keyId.secret.instanceId"
# Optional, only for self-hosted / custom app origins:
export BCMS_API_ORIGIN="https://app.thebcms.com"
```

> The MCP key and the SDK/CLI API key are the **same credential**. A key that works for MCP works here, as long as it has the right per-template/media scopes (see `references/permissions.md`).

## Running commands

After `npm install`, run either form:

```bash
node cli/bcms.mjs <command> [args] [flags]
npx bcms-content <command> [args] [flags]
```

Run `node cli/bcms.mjs help` for inline usage.

## Commands

| Command | Purpose |
|---------|---------|
| `create-entry <template> --data '<json>'` | Create an entry in a template (by id or name) |
| `update-entry <entryId> --template <t> --data '<json>'` | Update an entry; stdout returns the **full parsed entry** after the update |
| `delete-entry <entryId> --template <t>` | Delete an entry (irreversible — confirm the id first) |
| `list-entries <template>` | List entry ids for a template (discovery before update/delete) |
| `upload-media <filePath> [--parent <dirId>]` | Upload a file to the media library |

Common flags: `--data '<json>'` (inline) or `--data-file <path>` (from file), `--lng <code>` (default `en`), `--status <id>`, `--template <idOrName>`, `--parent <dirId>`.

All commands print a short status line followed by JSON to stdout. `create-entry` and `update-entry` return the **full parsed entry** (`meta`, `content`, `statuses`, `_id`, etc.) so agents see the complete state after the operation. Other commands return a smaller payload (e.g. media `_id`).

## `--data` shape

Single language, controlled by `--lng` (default `en`):

```jsonc
{
  "meta": { "title": "Hello world", "slug": "hello-world" },  // prop name -> value
  "content": "First paragraph.\n\nSecond paragraph."          // optional
}
```

- **`meta`** keys are the template's property names. Include all **required** props on create. On `update-entry`, partial `--data.meta` is **merged with the existing entry** for the target `--lng` before the API call — omitted keys are preserved, provided keys overwrite. The CLI always sends the complete merged `meta` for that language.
- **`content`** is optional. Pass a **plain string** (blank lines split paragraphs) for simple text, or a raw **`EntryContentNode[]`** array for rich text (headings, lists, media, widgets). On `update-entry`, if `content` is omitted the existing content nodes for that language are preserved and sent in full; if provided, content is replaced.

Rich-text node shape (Tiptap-style trees):

```jsonc
[
  { "type": "heading", "attrs": { "level": 2 }, "content": [{ "type": "text", "text": "Section" }] },
  { "type": "paragraph", "content": [{ "type": "text", "text": "Body text." }] }
]
```

## Examples

```bash
# Create a blog post (plain-text body)
node cli/bcms.mjs create-entry blog \
  --data '{"meta":{"title":"Hello","slug":"hello"},"content":"My first post."}'

# Update only the title (body is preserved; stdout is the full entry JSON)
node cli/bcms.mjs update-entry 663f0a... --template blog \
  --data '{"meta":{"title":"Hello (edited)"}}'

# List entries to find ids
node cli/bcms.mjs list-entries blog

# Delete an entry
node cli/bcms.mjs delete-entry 663f0a... --template blog

# Upload media into a folder
node cli/bcms.mjs upload-media ./hero.png --parent 6640bb...

# Read create data from a file (good for rich content)
node cli/bcms.mjs create-entry blog --data-file ./post.json
```

## CLI vs MCP vs SDK

- **This CLI** — deterministic, scriptable content ops in terminals, CI, and agent loops. One API key, no interactive login.
- **MCP tools** — best when the agent already has BCMS MCP configured; full schema-guided CRUD on entries and schema (create / read / update / **delete**), plus media and pointer-link tools. See the `bcms` skill and `references/mcp.md`.
- **`@thebcms/client` SDK** — for application code, builds, and anything beyond these commands. See the `bcms` skill.

## Safety

- **Never hard-code or commit API keys.** Use `BCMS_API_KEY` from the environment; prefer least-privilege scoped keys (`references/permissions.md`).
- **`delete-entry` is irreversible.** Confirm the id with `list-entries` first, and avoid deletes against production without checking impact.
- Use separate keys per environment (dev / staging / production).

Deeper references are bundled under `references/` (entries, media, properties, permissions, MCP). Change history: `ai/CHANGELOG.md`.
