---
name: craw-figma
description: Full bidirectional Figma integration — read files via REST API, create/modify/delete layers via local WebSocket connector + Figma plugin. Audit accessibility, extract design tokens, export assets. Write operations appear in real time on Figma Desktop.
---

# Craw Figma Skill

Complete Figma control for AI agents: **read** via REST API, **write** via a local plugin. Change design layers, extract design tokens, audit accessibility, export assets.

## Architecture

```
Craw ──→ figma_client.mjs (REST API) ──────→ Figma cloud    (read: file, styles, export)
     ──→ figma_send.js    (WebSocket) ──→ figma_connector.js ──→ Figma Plugin → Figma Desktop
     ──→ style_auditor.mjs              (design system analysis, CSS tokens)
     ──→ accessibility_checker.mjs      (WCAG AA/AAA, contrast, touch targets)
```

## Requirements

- **Figma Personal Access Token** → for REST API (read). Get it: Figma → Settings → Account → Personal Access Tokens
- **Figma Desktop** → required for write operations
- **Node.js 18+**

## Quick Start

### 1. Set up your token

```bash
export FIGMA_ACCESS_TOKEN="figd_your_token_here"
```

### 2. Read a Figma file

```bash
node scripts/figma_client.mjs get-file <file-key>
# Example: node scripts/figma_client.mjs get-file "ABC123xyz" --depth 4
```

Get a file key from: `https://www.figma.com/design/<FILE_KEY>/...`

### 3. Install the Figma Plugin (one-time, for write access)

1. Clone/download the skill repository
2. Open **Figma Desktop** → **Plugins** → **Development** → **Import plugin from manifest...**
3. Select `plugin/manifest.json` from this skill's directory
4. The plugin "Craw Figma Connector" is now installed

### 4. Start the connector + run the plugin

```bash
# Terminal 1: Start the local WebSocket server
node scripts/figma_connector.js
# → Listening on ws://localhost:9199
```

In Figma Desktop:
- Right-click canvas → **Plugins** → **Craw Figma Connector**
- The panel shows **Connected to Craw** when the WebSocket connects

### 5. Send write commands

```bash
# Create a rectangle
node scripts/figma_send.js createRectangle \
  --payload '{"x":100,"y":100,"width":400,"height":300,"fillColor":{"r":0.14,"g":0.49,"b":1},"cornerRadius":12,"name":"Hero Card"}'

# Get current selection
node scripts/figma_send.js getSelection
```

## Available Commands

### Write (Plugin — real-time in Figma Desktop)

| Command | Payload (JSON) | Description |
|---------|---------------|-------------|
| `createRectangle` | `{x, y, width, height, fillColor?, cornerRadius?, name?}` | New rectangle |
| `createFrame` | `{x, y, width, height, fillColor?, name?}` | New frame/artboard |
| `createEllipse` | `{x, y, width, height, fillColor?, name?}` | New ellipse |
| `createText` | `{x, y, characters, fontSize?, fontName?, fillColor?, name?}` | New text layer |
| `selectNode` | `{id}` | Select + zoom into node |
| `updateNode` | `{id, x?, y?, resize?{width,height}, fillColor?, name?}` | Modify existing node |
| `deleteNode` | `{id}` | Remove node |
| `setFillColor` | `{id, color{r,g,b}, opacity?}` | Set fill color |
| `groupSelection` | `{}` | Group selected nodes |
| `getSelection` | `{}` | List selected nodes |
| `getPageInfo` | `{}` | Current page info |
| `createPolygon` | `{x, y, width, height, pointCount, fillColor?, name?}` | Regular polygon (N sides) |
| `createStar` | `{x, y, width, height, pointCount, innerRadius?, fillColor?, name?}` | Star shape |
| `createVectorNetwork` | `{x, y, width, height, vectorNetwork: {vertices, segments}, fills?, strokes?}` | Custom vector path |
| `booleanOperation` | `{operation: UNION|SUBTRACT|INTERSECT|EXCLUDE, nodeIds, name?, fillColor?}` | Union/subtract/intersect shapes |
| `updateNode` (auto-layout) | `{id, layoutMode?, paddingLeft?, ..., itemSpacing?, primaryAxisAlignItems?, ...}` | Apply Auto Layout to frame |

### Shape Generator (advanced)

| Script | Description |
|--------|-------------|
| `node scripts/shape_generator.js test-basic` | Demo: rectangle, ellipse, polygon, star, heart in grid |
| `node scripts/shape_generator.js test-union` | Demo: union of two overlapping circles |
| `node scripts/shape_generator.js generate '{"type":"heart","width":200}'` | Single shape by type |

### Auto Layout Module

| Script | Description |
|--------|-------------|
| `node scripts/auto_layout.js card '{"width":320}'` | Create card with auto-layout |
| `node scripts/auto_layout.js button '{"name":"CTA"}'` | Create button with padding |
| `node scripts/auto_layout.js row '{"padding":8}'` | Horizontal row |
| `node scripts/auto_layout.js column '{"padding":16}'` | Vertical column |

### Style Dictionary Pipeline

| Script | Description |
|--------|-------------|
| `cd scripts/style-dictionary && npx style-dictionary build` | Generate CSS variables + Figma tokens |
| Output: `scripts/style-dictionary/build/variables.css` | DR's Lab CSS custom properties (`--color-*`, `--spacing-*`, etc.) |
| Output: `scripts/style-dictionary/build/figma-tokens.json` | Figma-compatible nested tokens |

### Read (REST API)

| Action | Args | Description |
|--------|------|-------------|
| `get-file` | `<key> [--depth N]` | Full file document tree |
| `get-file-nodes` | `<key> <id>...` | Specific nodes by ID |
| `get-styles` | `<key>` | Published styles (color, text, effects) |
| `get-components` | `<key>` | Published components |
| `get-versions` | `<key>` | Version history |
| `render-images` | `<key> <id> [--format png\|svg\|pdf] [--scale N]` | Export as images |
| `get-image-fills` | `<key>` | Image fill URLs used in file |
| `get-metadata` | `<key>` | Lightweight file info |
| `me` | — | Current user info |

### Analysis

| Action | Args | Description |
|--------|------|-------------|
| `style_auditor.mjs` | `<key> [--brand-colors "#HEX,#HEX"] [--generate-css]` | Analyze colors, fonts, consistency, CSS tokens |
| `accessibility_checker.mjs` | `<key> [--level AA\|AAA] [--format json\|report]` | WCAG contrast, touch targets, font sizes |

## Color Format

Figma uses RGB in 0–1 range:
```json
{"r": 0.14, "g": 0.49, "b": 1}     // #247DFF (blue)
{"r": 1, "g": 0.42, "b": 0.21}      // #FF6B35 (orange)
{"r": 1, "g": 1, "b": 1}            // #FFFFFF (white)
```

## Auto-setup for AI Agents

When a user installs this skill, the AI agent should:
1. Check if `FIGMA_ACCESS_TOKEN` is set — if not, instruct the user to generate one and export it
2. For write operations, check if the Figma plugin is installed — if not:
   - Guide the user through importing `plugin/manifest.json` in Figma Desktop
   - Suggest running `node scripts/figma_connector.js` separately
   - Offer to run `figma_connector.js` if the agent has shell access
3. Test connectivity with `figma_client.mjs me` before proceeding

## Tips

- Keep `figma_connector.js` running while working with write commands
- The plugin auto-reconnects if the connector restarts (3s retry)
- Commands sent while the plugin is offline are queued and sent on reconnect
- Health check: `http://localhost:9200` shows status and pending queue
- Use `--generate-css` to extract Figma styles as CSS custom properties
- Command timeout defaults to 30s. Override: `FIGMA_CMD_TIMEOUT=60000 node figma_connector.js`
- Boolean operations (union/subtract) may take longer — timeout is automatically handled and logged

## Files

```
skills/craw-figma/
├── SKILL.md
├── scripts/
│   ├── figma_client.mjs          — Figma REST API client (read)
│   ├── figma_connector.js        — Local HTTP server (run this) — timeout 30s configurable
│   ├── figma_send.js             — Send commands to Figma plugin
│   ├── shape_generator.js        — General-purpose shape creation (polygons, stars, hearts, union)
│   ├── auto_layout.js            — Auto Layout module (cards, rows, buttons, spacing)
│   ├── heart_generator.js        — Legacy heart shape generator
│   ├── star_generator.js         — Legacy star generator
│   ├── design_engine.js          — Design orchestration engine
│   ├── design_orchestrator.js    — Orchestrator with NotebookLM consultation
│   ├── design_critic.js          — Design critique pipeline
│   ├── craw_design_cmd.sh        — Shell wrapper for design commands
│   ├── svg_to_figma.js           — SVG path → Figma Vector Network converter
│   ├── style_auditor.mjs         — Design system analysis
│   ├── accessibility_checker.mjs — WCAG compliance
│   └── style-dictionary/
│       ├── config.json           — Style Dictionary configuration
│       ├── tokens/               — DTCG tokens → SD format
│       ├── build/variables.css   — Generated CSS custom properties
│       └── build/figma-tokens.json — Figma-compatible tokens
├── plugin/
│   ├── manifest.json             — Figma plugin manifest
│   ├── code.js                   — Plugin code (ES5, production)
│   ├── code.ts                   — Plugin code (TypeScript source)
│   └── ui.html                   — Plugin panel UI
├── design-tokens/
│   ├── design-tokens.json        — Core tokens (DTCG format)
│   ├── projects/drs-lab.json     — DR's Lab project tokens
│   └── load-tokens.js            — Token loader utility
└── references/
    ├── figma-api-reference.md    — REST API docs
    └── design-patterns.md        — UI patterns & best practices
```
