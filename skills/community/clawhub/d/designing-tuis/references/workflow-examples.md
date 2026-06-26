# Workflow Examples

## Default Route: Screenshot → Code (Direct Generation)

### Example 1: Simple Dashboard (lazygit-like)

**Phase 1 — Grounding:**
1. Scan screenshot boundaries: global rounded border wraps entire terminal
2. Identify top-level regions:
   - Vertical split: left panel (file tree) | right panel (diff view)
   - Bottom: status bar (1 row, full width)
3. Record:
   - Left panel: rounded border, ~30% width
   - Right panel: rounded border, ~70% width
   - Status bar: no border, fixed 1 row

**Phase 2 — Planning:**
```
Column [total height adaptive]
├── Row [fill height, min 20row]
│   ├── sidebar [30%, min 20col, rounded border]
│   │   └── Tree (file list, expand/collapse markers)
│   ├── divider [1col, fixed]
│   └── main [fill, min 40col, rounded border]
│       └── Paragraph (diff content, syntax-colored)
└── status [1row, fixed, no border]
    └── Text (branch name + file path, dim)
```

**Phase 3 — Generation (→ Code):**
- Target: BubbleTea (Go)
- Generate `model` struct with `width`, `height`, tree state, viewport state
- `Update()`: handle `tea.WindowSizeMsg` → recalculate sidebar = width*30/100, main = width - sidebar - 1
- `View()`: compose with lipgloss, `tea.WithAltScreen()`
- Confirm with user, iterate if needed

**Comparison & Iteration:**
- Render preview at 80×24 and 120×40
- Check: sidebar/main ratio ≈ 30/70 (tolerance ≤ 10%)
- Check: no render ghosts on resize
- P0 pass → deliver

---

### Example 2: Multi-Panel Application (k9s-like)

**Phase 1 — Grounding:**
1. Global structure: Column layout (top to bottom)
   - Header bar (1 row): cluster info, colored labels
   - Tab bar (1 row): multiple tab labels, one highlighted
   - Main area (fill): Table with header + data rows
   - Status/command bar (1 row): key hints

**Phase 2 — Planning:**
```
Column [total adaptive]
├── header [1row, fixed, no border]
│   └── Row: logo + cluster name + namespace (colored)
├── tabs [1row, fixed]
│   └── Tabs (pods / deploy / services / ..., activeIndex=0)
├── main [fill, min 15row, border single]
│   └── Table (columns: NAME, READY, STATUS, RESTARTS, AGE)
└── status [1row, fixed, no border]
    └── Text (key hints: <q> quit, <enter> describe, ...)
```

**Phase 3 — Generation (→ Code):**
- Target: Ink (React/JSX)
- `<Box flexDirection="column" width="100%" height="100%">`
- Header: `<Box height={1}>` with colored `<Text>` elements
- Tabs: `<Tabs>` component, `activeIndex` state
- Main: `<Box flexGrow={1}>` containing table
- Status: `<Box height={1}>` with dim text
- Responsive by default (flexbox model)

---

### Example 3: Existing Code Iteration

1. User provides screenshot showing sidebar is too narrow after resize
2. **Comparison**: sidebar at 80col terminal = 20col (25%) → target was 30%
3. **Fix**: adjust proportion calculation: `sidebarWidth = max(width*30/100, 20)`
4. Re-render, verify at 80×24: sidebar = 24col (30%) ✓
5. Verify at 120×40: sidebar = 36col (30%) ✓

---

## Advanced Route: Screenshot → .tui Schema → Code

### Example 4: Multi-Framework Output

**Use case:** Team needs the same dashboard in BubbleTea (Go CLI) and Textual (Python admin tool).

**Phase 1 & 2:** Same as default route (Grounding + Planning)

**Phase 3 — Generation (→ Schema):**

Save `designs/dashboard.tui`:
```json
{
  "version": "1",
  "meta": { "name": "dashboard", "terminalSize": "adaptive", "theme": "default" },
  "tree": {
    "component": "Box",
    "layout": { "type": "flexbox", "direction": "column" },
    "style": { "border": false },
    "children": [
      {
        "component": "Box",
        "layout": { "direction": "row", "height": "fill", "minHeight": 20 },
        "children": [
          {
            "component": "Tree",
            "layout": { "width": "30%", "minWidth": 20 },
            "style": { "border": true, "borderStyle": "rounded" },
            "props": { "nodes": [] }
          },
          {
            "component": "Divider",
            "props": { "orientation": "vertical" },
            "layout": { "width": 1 }
          },
          {
            "component": "Paragraph",
            "layout": { "width": "fill", "minWidth": 40 },
            "style": { "border": true, "borderStyle": "rounded" },
            "props": { "content": "" }
          }
        ]
      },
      {
        "component": "Text",
        "layout": { "height": 1 },
        "style": { "dim": true },
        "props": { "content": "main ● src/app.go" }
      }
    ]
  }
}
```

**Schema → Code conversion:**
- Follow `references/schema-to-code-mapping.md`
- Generate BubbleTea version: proportion via `tea.WindowSizeMsg` recalculation
- Generate Textual version: proportion via CSS `width: 30%` + `min-width: 20`

---

### Example 5: Existing .tui File Edit

1. Open `designs/current.tui`
2. User requests: "make the sidebar wider"
3. Change sidebar node: `"width": "30%"` → `"width": "40%"`, `"minWidth": 20` → `"minWidth": 25`
4. Verify: sibling widths still sum correctly (40% + 1col fixed + fill = 100%)
5. Re-generate target code if using advanced route

---

## Comparison and Iteration Protocol

After any generation (either route), validate:

| Priority | Check | Action if Failed |
|----------|-------|------------------|
| P0 | Layout direction correct (row/column) | Restructure layout tree |
| P0 | Proportions within 10% of target | Adjust width/height values |
| P0 | No render ghosts on resize | Add clear-screen, verify alt-screen |
| P1 | Component types correct | Swap component (e.g., List → Table) |
| P2 | Text content complete | Add missing labels/items |
| P3 | Colors and styles match | Adjust style properties |
| P4 | Spacing (padding/gap) matches | Fine-tune padding/gap values |

**Responsive validation:** Test at minimum two terminal sizes (e.g., 80×24 and 120×40). Verify proportions hold and no content is truncated.
