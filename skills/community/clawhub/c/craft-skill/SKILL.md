---
name: craft
version: 2.0.2
description: Create and format Craft documents reliably via the Craft MCP v2 unified API (craft_write / craft_read). Triggers on any Craft document or note creation, editing, or formatting — including when building project docs, meeting notes, specs, or any structured content in Craft. Ensures correct block structure, ordering, and element syntax on the first pass.
---

# craft — Reliable Craft Document Creation (MCP v2)

## ⚠️ Production Data Warning

Craft MCP connects to a **production server with real user data**. Only perform
operations that can be safely rolled back:

- ✅ **Safe**: Reading data, creating test content you delete immediately
- ✅ **Safe**: Modifying content if you can restore it to its original state
- ✅ **Safe**: Moving blocks if you can move them back
- ❌ **Unsafe**: Permanent deletions, modifications without backup, or any
  changes you cannot reverse

Always verify rollback operations work before considering a task complete.

## The Unified Tool Model

The Craft MCP v2 server exposes **three tools**: `craft_write`, `craft_read`,
and `blocks_revert`. Everything — blocks, documents, tasks, collections,
whiteboards, comments, styling — flows through a single command string passed
to `craft_write` or `craft_read`. This is a fundamentally different model from
v1's 32+ individual tool endpoints.

## The Unified Tool Model

| Tool | Purpose | Mutates? |
|---|---|---|
| `craft_write` | Create/update/delete documents, blocks, tasks, collections, whiteboards, comments, styling | Yes |
| `craft_read` | Read documents, search, list folders/tasks/collections, explore themes/washi/Unsplash | No |
| `blocks_revert` | Undo a previous add/update/delete if blocks are unmodified | Yes |

Both `craft_write` and `craft_read` take a single `command` string argument.
Multiple commands can be batched with semicolons (`;`) in a single call —
execution stops on the first failure, but earlier commands are already applied.

**Key concept**: A document ID is the same as its root block ID. Use it
interchangeably — `documents create` returns a `rootBlockId` that is the
document's identifier for all block operations.

## The Newline Rule (unchanged from v1)

In `--markdown` arguments:

| Input | Result |
|---|---|
| `\n\n` (double newline) | **New block** — each `\n\n`-separated segment becomes its own block |
| `\n` (single newline) | **Literal characters** `\` and `n` stored in the block text |
| Actual newline (shell `$'...\n...'`) | Soft line break within the same block |

**Single `\n` never creates a new block or a soft break.** It produces visible
`\n` text. This remains the #1 cause of broken documents.

## Default Workflow: Whole-Document Creation

```
1. craft_write: "documents create --title \"My Doc\""  → rootBlockId
2. craft_write: "blocks add --id <rootBlockId> --json '[...]'"
3. craft_read:  "blocks get <rootBlockId> --format markdown"  → verify
```

### JSON vs Markdown Mode

**Always prefer JSON mode.** The v2 command parser is picky — `--markdown`
values containing emoji, `#`, backticks, or special characters cause
"Unexpected text" parse errors. JSON mode is always correct.

Use `--markdown` only for simple prose, headings, and basic lists with no
special characters.

**JSON array mode** creates multiple blocks in one call with exact type
control and preserves array order:

```json
[
  {"type":"text","textStyle":"h2","markdown":"## Section"},
  {"type":"text","listStyle":"bullet","markdown":"- Item one"},
  {"type":"code","rawCode":"print(\"hello\")","language":"python"},
  {"type":"text","listStyle":"task","markdown":"- [x] Done","taskInfo":{"state":"done"}}
]
```

## Element → Input Mapping

| Element | Markdown Input | JSON Input | Notes |
|---|---|---|---|
| Heading 1–4 | `# H1` … `#### H4` | `{"textStyle":"h1",...}` | `\n\n` before/after |
| Paragraph | Plain text | `{"type":"text","markdown":"..."}` | |
| **Bold** | `**text**` | Inline within markdown | |
| *Italic* | `*text*` | Inline within markdown | |
| ~~Strikethrough~~ | `~text~` | Inline | Craft normalizes `~~` to `~` |
| `Inline code` | `` `code` `` | Inline | |
| Bullet list | `- Item` | `{"listStyle":"bullet","markdown":"- Item"}` | One item = one block |
| Numbered list | `1. Item` | `{"listStyle":"numbered","markdown":"1. Item"}` | Craft renumbers on display |
| **Task (open)** | `- [ ] Task` | `{"listStyle":"task","markdown":"- [ ] Task","taskInfo":{"state":"todo"}}` | |
| **Task (done)** | `- [x] Task` | `{"listStyle":"task","markdown":"- [x] Task","taskInfo":{"state":"done"}}` | |
| Toggle | `+ Toggle title` | `{"listStyle":"toggle","markdown":"+ Toggle title"}` | Content = subsequent blocks with higher `indentationLevel` |
| Blockquote | `> Quoted text` | `{"decorations":["quote"]}` | |
| Callout | `<callout>Text</callout>` | `{"decorations":["callout"]}` | |
| Highlight | `==Highlighted text==` | Inline | Renders yellow by default. Custom colors via `<highlight color='name'>` — see below |
| Divider | `---` or `***` | `{"type":"line"}` | |
| Link | `[text](url)` | Inline | |
| **Code block** | ❌ Fenced ``` does NOT work | `{"type":"code","rawCode":"...","language":"python"}` | **JSON only** |
| **Image** | — | `{"type":"image","url":"https://...","altText":"...","size":"fit\|fill","width":"auto\|fullWidth"}` | Inline image block |
| **Video** | — | `{"type":"video","url":"https://...","altText":"..."}` | Inline video block |
| **File** | — | `{"type":"file","url":"https://...","fileName":"doc.pdf","blockLayout":"small\|regular\|card"}` | File attachment |
| **Drawing** | — | `{"type":"drawing","url":"https://..."}` | Hand-drawn content |
| **Table** | — | `{"type":"table"}` | Structured table |
| **Rich URL** | — | `{"type":"richUrl","url":"https://...","title":"...","layout":"small\|regular\|card"}` | Rich link preview card |
| **Card/page** | `<page><pageTitle>Title</pageTitle><content>...</content></page>` | `{"type":"text","textStyle":"card","cardLayout":"small\|square\|regular\|large"}` | Nested page or card block |

### Code Block Detail

Fenced code blocks are **not supported** in `--markdown` mode. Use JSON mode:

```json
{"type":"code","rawCode":"print(\"hello\")\nprint(\"world\")","language":"python"}
```

The canonical field is `language` (not `codeLanguage`). Supported languages:
`ada`, `bash`, `cpp`, `cs`, `css`, `dart`, `dockerfile`, `go`, `groovy`,
`haskell`, `html`, `java`, `javascript`, `json`, `julia`, `kotlin`, `lua`,
`markdown`, `matlab`, `objectivec`, `perl`, `php`, `prolog`, `plaintext`,
`python`, `r`, `ruby`, `rust`, `scala`, `shell`, `sql`, `swift`, `typescript`,
`vbnet`, `xml`, `yaml`, `math_formula`, `other`.

Within `rawCode`, `\n` produces actual newlines in the code block.

### Toggle Content

Toggle blocks use `listStyle: "toggle"`. Content inside the toggle is created
as subsequent blocks with a higher `indentationLevel` than the toggle itself:

```json
[
  {"type":"text","listStyle":"toggle","markdown":"+ Toggle title","indentationLevel":1},
  {"type":"text","markdown":"Hidden content inside toggle","indentationLevel":2}
]
```

### Nested Content

Use `indentationLevel` (range 0–5) for sub-bullets, nested tasks, and indented
content under list items:

```json
[
  {"type":"text","listStyle":"numbered","markdown":"1. First step"},
  {"type":"text","listStyle":"bullet","markdown":"- Sub-bullet","indentationLevel":2},
  {"type":"text","listStyle":"task","markdown":"- [ ] Nested task","taskInfo":{"state":"todo"},"indentationLevel":2}
]
```

## Documents

### Create

```
documents create --title "My Document" [--folder <folderId>] [--destination unsorted|templates]
```

Returns a `rootBlockId` for block operations and a Craft app link for humans.

### Resolve Craft Links

```
documents resolve-link <url>
```

Pastes a Craft doc URL into the chat? Use `resolve-link` first to get the
`rootBlockId` — do not use the URL's `documentId` directly.

## Blocks

### Add

```
blocks add --id <pageId> --markdown <text> [--position start|end]
blocks add --id <pageId> --json <json>
blocks add --siblingId <blockId> --markdown <text> [--position before|after]
blocks add --date <YYYY-MM-DD|today|yesterday|tomorrow> --markdown <text>
```

### Sibling Ordering Rule

When adding multiple siblings `after` the same block:

- ❌ **Same anchor**: Each new block inserts immediately after the anchor,
  producing **reverse order**.
- ✅ **Chain anchors**: Each new block uses the **previously added block's ID**
  as `--siblingId`.

**Exception:** JSON array mode (`--json '[{...},{...}]'`) always preserves
array order regardless of anchor.

### Update / Delete / Move

```
blocks update --id <blockId> --markdown <text>
blocks delete --id <blockId>
blocks move --id <blockId> --targetId <pageId> [--position start|end]
```

`blocks update` replaces the target block's content. To insert after updating,
use a separate `blocks add --siblingId` call.

## Tasks

```
tasks add --markdown <text> [--state todo|done|canceled] [--schedule <date>] [--deadline <date>]
tasks update --id <taskId> [--state done] [--markdown <text>]
tasks delete --id <taskId>
```

Dates: `YYYY-MM-DD`, `today`, `tomorrow`, `yesterday`.

## Collections

### Create

```
collections create --name "Tasks" --title "Task Name" --Status "select:Todo,Done" --Priority "select:Low,High" --Due "date" --Completed "boolean" --document <rootBlockId>
```

- `--title` sets the row headline column (one per collection, always text).
- Additional columns defined as `--<PropertyName> <type>[:options]`.
- Types: `text`, `number`, `boolean`, `date`, `url`, `email`, `phone`,
  `select:Opt1,Opt2`, `multiSelect:A,B,C`, `relation:targetCollectionId`.
- Type aliases: `checkbox` → `boolean`, `select` → `singleSelect`, `link` → `url`.

### Add Items

```
collections items-add --collection <collectionId> --items '<json-array>'
```

Item JSON format:

```json
[
  {
    "task_name": "Setup MCP v2",
    "properties": {
      "status": "Done",
      "priority": "High",
      "due": "2026-06-28",
      "completed": true
    }
  }
]
```

**Key rule**: The `--title` column name becomes a **snake_case** top-level key
(e.g., "Task Name" → `task_name`). All other columns go under `properties`.
Check the schema with `craft_read: "collections schema --collection <id>"`
if unsure.

### Update / Delete Items

```
collections items-update --collection <collectionId> --id <itemId> --<PropertyName> <value>
collections items-delete --collection <collectionId> --id <itemId>
```

### Views

```
collections views-create --collection <collectionId> ...
collections views-update --collection <collectionId> ...
collections views-delete --collection <collectionId> ...
collections views-set-active --collection <collectionId> ...
```

## Whiteboards

### Create

```
whiteboards create [--position '{"position":"end","pageId":"<rootBlockId>"}']
```

### Add Elements

```
whiteboards elements add --whiteboard <whiteboardId> --elements '<json-array>'
```

Elements use Excalidraw-compatible JSON:

```json
[
  {"id":"rect1","type":"rectangle","x":100,"y":100,"width":200,"height":100,"strokeColor":"#FF6B6B","backgroundColor":"#FFE0E0","strokeWidth":2},
  {"id":"text1","type":"text","x":120,"y":130,"width":160,"text":"Label","fontSize":20},
  {"id":"arrow1","type":"arrow","x":350,"y":150,"width":100,"height":0,"strokeColor":"#4ECDC4","strokeWidth":3}
]
```

### Update / Delete Elements

```
whiteboards elements update --whiteboard <whiteboardId> --elements '<json-array>'
whiteboards elements delete --whiteboard <whiteboardId> --ids <id1>,<id2>
```

## Comments

```
comments add --comments '[{"blockId":"<blockId>","content":"Comment text"}]'
```

JSON array of comment objects, each with `blockId` and `content`.

## Page Styling

Styling flags are passed on `blocks add` when adding to a page root:

```
blocks add --id <rootBlockId> --markdown "Content" \
  --theme-id soft-spring \
  --font system-rounded \
  --separator washi \
  --washi-pattern wave \
  --washi-color #FF6B6B \
  --cover-url https://images.unsplash.com/... \
  --backdrop-type gradient \
  --backdrop-colors #FF6B6B,#4ECDC4 \
  --backdrop-direction top-to-bottom
```

| Flag | Values |
|---|---|
| `--theme-id` | Use `craft_read: "blocks explore-themes --type page"` to list |
| `--font` | `system`, `serif`, `rounded`, `mono` (MCP also accepts `system-serif`, `system-rounded`, `system-mono` aliases) |
| `--separator` | `line`, `doodle`, `washi`, `none` |
| `--washi-pattern` | `wave`, `hex`, `stripe`, `dot`, etc. |
| `--washi-color` | `#RRGGBB` |
| `--backdrop-type` | `solid`, `gradient`, `image`, `pattern`, `none` |
| `--backdrop-color` | `#RRGGBB` (for solid) |
| `--backdrop-colors` | `#FF6B6B,#4ECDC4` (for gradient) |
| `--backdrop-direction` | `top-to-bottom`, `left-to-right`, etc. |
| `--backdrop-url` | Image URL (for image backdrop) |
| `--cover-url` | Hero/cover image URL |
| `--cover-crop` | JSON: `x,y,width,height` (values 0.0–1.0) |
| `--cover-attribution` | Text attribution for cover image |

Colors accept `#RRGGBB` or `"#light #dark"` for appearance-aware (light/dark mode).

### Text Alignment

Text blocks support `textAlignment`: `left` (default), `center`, `right`, `justify`.

```json
{"type":"text","textStyle":"h2","textAlignment":"center","markdown":"## Centered Heading"}
```

### Block Colors

Any block can be colored via a top-level `color` field (not inside `decorations`):

```json
{"type":"text","color":"#FF6B6B","markdown":"Red text"}
```

The `color` field accepts 7-character hex codes (`#RRGGBB`). Craft auto-adjusts
for readability and generates a dark variant automatically.

### Markdown Special Tokens

Beyond standard markdown, Craft supports these HTML-like tokens in `--markdown` mode:

| Token | Effect |
|---|---|
| `<callout>Text</callout>` | Callout/highlight block (can wrap multiple paragraphs) |
| `<caption>Text</caption>` | Caption text style |
| `<highlight>Text</highlight>` | Yellow highlight (inline) |
| `<highlight color='red'>Text</highlight>` | Custom color highlight (named colors only) |
| `<page><pageTitle>Title</pageTitle><content>...</content></page>` | Nested page/card structure |
| `[text](block://blockId)` | Block link — links to a specific block by ID |
| `[text](date://YYYY-MM-DD)` | Date link — links to a daily note |

**Highlight color names** (not hex): `yellow`, `green`, `mint`, `cyan`, `blue`,
`purple`, `pink`, `red`, `gray`, `gradient-blue`, `gradient-purple`,
`gradient-red`, `gradient-yellow`, `gradient-brown`.

### Divider Styles

Line blocks (`type: "line"`) support `lineStyle` values:
`strong`, `regular` (default), `light`, `extraLight`, `pageBreak`.

```json
{"type":"line","lineStyle":"pageBreak"}
```

## Reading & Search

```
blocks get <rootBlockId> [--depth <depth>] [--format json|markdown] [--fetchMetadata true|false]
blocks get --date today
```

- `--depth`: `-1` (all descendants, default), `0` (self only), `1` (direct children)
- `--fetchMetadata`: Returns comments, createdBy, lastModifiedBy, lastModifiedAt, createdAt

```
documents list [--location unsorted|trash|templates|daily_notes | --folder <folderId>]
folders list [--filter <regex>]
tasks list [--scope active|upcoming|inbox|logbook|document|all]
collections list [--document <rootBlockId>]
collections schema --collection <collectionId>
collections items-get --collection <collectionId>
collections views-list --collection <collectionId>
whiteboards elements get --whiteboard <whiteboardId>
images view --url <image-url>
search <query> [--location unsorted|trash|templates|daily_notes]
```

Common flags: `--offset`, `--cursor`, `--filter <regex>`, `--format json|markdown`.

### Explore Themes, Washi, Unsplash

```
blocks explore-themes --type page|fonts|code
blocks explore-washi
blocks search-unsplash <query>
```

## Batching

Multiple commands can be sent in a single `craft_write` or `craft_read` call,
separated by semicolons:

```
folders list; documents list; blocks get ABC-123 --format markdown
```

**Execution stops on the first failure.** Earlier commands are already
applied — there is no rollback. Note the partial state if a batch fails midway.

## blocks_revert (Undo)

Reverts a previous add/update/delete operation if the affected blocks have
not been modified since. Used primarily by Craft's widget UI for undo/redo,
but available programmatically:

```json
{
  "revertInfo": {
    "operation": "add",
    "blockIds": ["block-id-1"],
    "expectedStamps": {"block-id-1": "stamp-value"},
    "parentBlockId": "page-id",
    "documentId": "doc-id"
  }
}
```

Operations: `add`, `update`, `delete`. Requires `expectedStamps` matching
the block states at the time of the original operation.

## Handling Transient Upstream Errors (502 / 503 / 504)

Craft's MCP endpoint sits behind Cloudflare and intermittently returns
`502 Bad Gateway`, `503`, or `504`. These are **almost always transient**.

### Backoff policy

1. **First failure**: wait 60s (or server-provided `retry_after`), retry once.
2. **Second failure**: wait 120s, retry once more.
3. **Third failure**: stop. Report the outage and ask whether to keep waiting.

Use `exec sleep <seconds>` between retries — never a tight loop of repeated
tool calls.

### Session-safety rules

- **Never abort mid-retry.** Interrupting a sleeping retry can wedge sessions.
- **Save progress before retrying.** Note the `rootBlockId` and last-added
  block ID in your reply before sleeping.
- **Prefer fewer, larger writes.** A single `blocks add --json '[...]'` array
  has one chance to 502; ten sequential calls have ten chances.
- **`blocks add` is not idempotent.** A retry after a 502 that actually
  succeeded server-side will duplicate blocks. Read back and prune duplicates
  after a successful retry.

## Rewriting Existing Documents

### Full Rewrite: Delete and Recreate

```python
# Fast: delete and recreate
craft_write: "documents delete --document <rootBlockId>"
craft_write: "documents create --title \"Same Title\" --folder <folderId>"

# Slow: block-by-block deletion (avoid)
craft_write: "blocks delete --id <block1>; blocks delete --id <block2>; ..."
```

### Renaming a Document

Update the root page block:

```
blocks update --id <rootBlockId> --markdown "New Document Title"
```

## Pre-Finalize Checklist

1. **Read back**: `craft_read: "blocks get <rootBlockId> --format markdown"`
2. **Verify**: All sections present, no literal `\n` characters, correct
   ordering, no duplicate or stray blocks
3. **If broken**: Delete stray blocks with `blocks delete --id <blockId>`,
   fix and re-add
4. **Report done** only after confirming the readback is clean
5. **Safety check**: If this was a test, delete the test document or restore
   original content. This is production data — verify rollback before done.

## Canonical Example

Create a project doc with heading, tasks, code, callout, and collection:

```
# Step 1: Create document
craft_write: "documents create --title \"API Spec\""
# → rootBlockId: ABC-123

# Step 2: Add all content (JSON array — safe for any characters)
craft_write: "blocks add --id ABC-123 --json '[
  {"type":"text","textStyle":"h2","markdown":"## Overview"},
  {"type":"text","markdown":"API spec for the auth service."},
  {"type":"text","textStyle":"h2","markdown":"## Tasks"},
  {"type":"text","listStyle":"task","markdown":"- [ ] Define endpoints","taskInfo":{"state":"todo"}},
  {"type":"text","listStyle":"task","markdown":"- [x] Choose framework","taskInfo":{"state":"done"}},
  {"type":"code","rawCode":"POST /auth/login\\nContent-Type: application/json","language":"http"},
  {"type":"text","decorations":["callout"],"markdown":"Do not store tokens in localStorage"}
]'"

# Step 3: Verify
craft_read: "blocks get ABC-123 --format markdown"
```

## Connection Info

```
craft_read: "connection info"
```

Returns space ID, connection details, and MCP version.