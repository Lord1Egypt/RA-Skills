# Figma Remote MCP — Tool Reference

**Endpoint:** `https://mcp.figma.com/mcp`
**Auth:** OAuth 2.0 (Bearer token via CC Token Bootstrap)
**In OpenClaw:** Read tools as `figma__*`, write tools via CC as `mcp__figma__*`

---

## Read Tools

### `get_design_context` / `figma__get_design_context`

Returns React+Tailwind code, screenshot URL, and contextual hints for a Figma node.

**Parameters:**
- `fileKey` (string) — Figma file key from URL
- `nodeId` (string) — Node ID, use `:` separator (e.g. `123:456`)

**Returns:** code snippet, screenshot, Code Connect mappings if configured, design annotations

**Notes:**
- Primary tool for design-to-code workflows
- Output varies based on Figma setup: raw code, Code Connect snippets, or annotated references
- Adapt output to project's actual stack — not final code

---

### `get_screenshot` / `figma__get_screenshot`

Returns a screenshot image of the specified Figma node.

**Parameters:**
- `fileKey`, `nodeId`

**Use when:** layout fidelity is important, design context code alone is insufficient

---

### `get_metadata` / `figma__get_metadata`

Returns sparse XML with layer IDs, names, types, positions, and sizes.

**Parameters:**
- `fileKey`, `nodeId`

**Use when:** inspecting large designs where `get_design_context` would be too heavy; good for understanding layer structure before drilling into specific nodes

---

### `get_variable_defs` / `figma__get_variable_defs`

Returns variables and styles scoped to a selection: colors, spacing, typography.

**Parameters:**
- `fileKey`, `nodeId`

**Use when:** extracting design tokens for a component or page section

---

### `search_design_system` / `figma__search_design_system`

Searches all connected Figma libraries for components, variables, and styles.

**Parameters:**
- `query` (string) — search term
- `fileKey` (string) — context file

**Use when:** finding existing components before generating new ones; always check this first

---

### `get_figjam` / `figma__get_figjam`

Returns a FigJam board as XML with embedded screenshots.

**Parameters:**
- `fileKey`, `nodeId`

**File type:** FigJam only (`figma.com/board/...`)

---

### `get_code_connect_map` / `figma__get_code_connect_map`

Returns existing mappings from Figma node IDs to codebase components.

**Parameters:**
- `fileKey`, `nodeId`

---

### `get_code_connect_suggestions` / `figma__get_code_connect_suggestions`

Returns Figma-generated suggestions for mapping components to code.

**Parameters:**
- `fileKey`

---

### `get_context_for_code_connect` / `figma__get_context_for_code_connect`

Returns context needed to set up Code Connect for a component.

**Parameters:**
- `fileKey`, `nodeId`

---

### `whoami` / `figma__whoami`

Returns authenticated user info, plan, and seat type.

**Parameters:** none

**Use for:** verifying the token is valid; debugging auth issues

---

## Write Tools (CC session only)

### `use_figma` / `mcp__figma__use_figma`

General-purpose write tool — executes JavaScript via Figma's Plugin API.

**Parameters:**
- `code` (string) — JavaScript to execute in Figma plugin context
- `fileKey` (string)

**Limits:**
- 20KB response limit per call
- No image/asset import (no `loadImageAsync`, no custom fonts)
- Components must be published before Code Connect works
- Beta — output needs manual review

**IMPORTANT:** Always load `figma:figma-use` skill before calling this tool.

---

### `generate_figma_design` / `mcp__figma__generate_figma_design`

Generates UI layers from live web pages or code into a Figma file.

**Parameters:**
- `url` or code source
- `fileKey` (target file, optional — creates new if omitted)

**Notes:**
- Exempt from rate limits
- Only available in certain clients (CC, Cursor, Codex)
- Best with `figma:figma-generate-design` skill

---

### `create_new_file` / `mcp__figma__create_new_file`

Creates a new empty design or FigJam file in Drafts.

**Parameters:**
- `name` (string)
- `fileType`: `"design"` | `"figjam"`

**Returns:** `file_key`, `file_url`

---

### `generate_diagram` / `mcp__figma__generate_diagram`

Creates a FigJam diagram from Mermaid syntax.

**Parameters:**
- `mermaid` (string) — Mermaid diagram source
- `fileKey` (FigJam file)

**Supported types:** flowchart, sequence diagram, state diagram, Gantt chart

---

### `add_code_connect_map` / `mcp__figma__add_code_connect_map`

Adds a mapping from a Figma node to a codebase component.

**Parameters:**
- `fileKey`, `nodeId`, `componentPath`, `componentName`

---

### `send_code_connect_mappings` / `mcp__figma__send_code_connect_mappings`

Confirms and sends Code Connect mappings to Figma.

**Parameters:**
- `fileKey`, `mappings` (array)

---

### `create_design_system_rules` / `mcp__figma__create_design_system_rules`

Generates a rule file for design-system-aware code generation.

**Parameters:**
- `fileKey`, `codebasePath`

**Notes:** Load `figma:figma-create-design-system-rules` skill first.

---

## Rate Limits

| Plan | Read Tools (daily) | Write Tools |
|------|-------------------|-------------|
| Enterprise | 600/day, 20/min | Exempt |
| Org/Pro Full/Dev | 200/day, 10-15/min | Exempt |
| Starter | 6/month | Exempt |

Rate limits apply per workspace/team, not just per user seat.

---

## URL Format

```
figma.com/design/:fileKey/:fileName?node-id=:nodeId
```

- `nodeId` in URL uses `-` separator → convert to `:` for API calls
- Branch files: use `branchKey` as `fileKey`
- FigJam: `figma.com/board/:fileKey/:fileName`
- Figma Make: `figma.com/make/:makeFileKey/:makeFileName`
