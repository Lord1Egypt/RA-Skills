# TUI Layout Inference Rules

Reference for determining layout structure from TUI screenshots. Used during Phase 2 (Planning) of the 3-phase decomposition protocol.

## 1. Determining Row vs Column

### Projection Method (TUI Simplified)

- Children separated by vertical lines/borders, arranged horizontally → **Row** (`direction: "row"`)
- Children separated by horizontal lines/borders, arranged vertically → **Column** (`direction: "column"`)
- Children arranged in an M×N grid pattern → **Grid** (`columns: N`)

### Supporting Heuristics

- Children vary in width but share similar height → Row
- Children vary in height but share similar width → Column
- All children have identical dimensions and count > 2 → consider Grid

### Edge Cases

- Single child fills the container → direction is irrelevant; use Column as default
- Mixed sizes with one dominant fill area → the fill child is the "main" area; fixed-size children are headers/footers/sidebars

## 2. Identifying Container vs Atomic Component

| Visual Cue | Component Type |
|------------|----------------|
| Has border wrapping, contains multiple different content types | Box |
| Multiple homogeneous rows, possible prefix symbols (▸ ● ✓ ─ * - [ ]) | List |
| Has header row + aligned data columns | Table |
| Indented levels, expand/collapse markers (▸ ▾ ├ └) | Tree |
| Horizontally arranged labels, one highlighted/reversed/underlined | Tabs |
| Single line of text or label | Text |
| Multi-line paragraph text, possibly wrapping | Paragraph |
| Horizontally filled bar, partially highlighted | ProgressBar |
| Horizontal separator line (─── or ═══) | Divider |
| Centered floating box, possibly with backdrop overlay | Modal |
| Editable area with cursor indicator | Input |

## 3. Spacing Inference

- Distance (in spaces) from border characters to content → **padding**
- Blank lines/columns between sibling children → **gap**
- Spacing > 2 characters with different content types on both sides → likely an independent container boundary
- Spacing = 0 with adjacent borders → `padding: 0`

### Spacing Quantification

Count characters precisely—TUI uses monospace fonts so 1 char = 1 unit:

- Horizontal padding: spaces from left border char to first content char
- Vertical padding: blank lines from top border to first content line
- Gap: blank lines (vertical) or space columns (horizontal) between adjacent siblings

## 4. Size and Proportion Inference

### Character-Level Quantification

TUI proportions can be precisely quantified via character counting (no sub-pixel ambiguity):

- Horizontal proportion: count columns each region occupies
- Vertical proportion: count rows each region occupies
- Total terminal size: infer from screenshot or obtain from user (e.g., 80×24, 120×40)

### Proportion Notation

Annotate proportions in the layout tree:

```
Row [80col total]
├── sidebar [25col, 31%]
├── divider [1col]
└── main    [54col, 68%]

Column [40row total]
├── header  [3row]
├── body    [35row, fill]
└── status  [2row]
```

### Proportion Categories

- **Fixed size**: status bar 2 rows, divider 1 col → hardcode row/col count
- **Proportional size**: sidebar 30%, main 70% → allocate remaining space by ratio
- **Fill size**: body takes all remaining space → fill / flex-grow

### Responsive Layout Principles

TUI must adapt to different terminal sizes (from 80×24 to 200×60+). Design with proportions and fill first, fixed values second:

- **Prefer percentages and fill** — avoid hardcoding absolute column counts from screenshots
- **Fixed sizes only for semantically fixed areas**: status bar (1-2 rows), divider (1 col/row), title bar (1 row)
- **Set minimum size fallbacks**: proportional areas should have min-width / min-height to prevent content crushing in small terminals
- **Narrow terminal degradation**: when terminal width < threshold, row layouts should degrade to column stacking (e.g., sidebar collapses from side panel to top fold)

### Responsive Proportion Annotation Example

```
Row [total width adaptive]
├── sidebar [30%, min 20col]
├── divider [1col, fixed]
└── main    [fill, min 40col]
```

## 5. Border Inference

| Character Pattern | borderStyle |
|-------------------|-------------|
| ┌─┐ │ └─┘ | `"single"` |
| ╔═╗ ║ ╚═╝ | `"double"` |
| ╭─╮ │ ╰─╯ | `"rounded"` |
| +--+ \| +--+ | `"ascii"` |
| No visible border | `border: false` |

### Border Detection Tips

- Check all four corners for consistent style
- Mixed border characters (e.g., single top + double bottom) → unusual, flag for user confirmation
- Shadow effect (displaced duplicate border chars) → style decoration, not structural

## 6. Color and Style Inference

- Highlighted/reversed line → `selectedIndex` or `activeIndex`
- Dimmed/gray text → `dim: true`
- Bold text → `bold: true`
- Colored text → prefer theme semantic color names (`primary` / `success` / `warning` / `error`)
- When semantics are unclear → use base color names (`red` / `green` / `blue` / `cyan` / `magenta` / `yellow` / `gray` / `white`)

**Accessibility requirement:** When color conveys meaning (status, selection, navigation), always pair with a non-color cue (symbol, text label, bold, reverse). See `references/color-accessibility.md` for WCAG compliance rules, color-blind safe palettes, and safe color combinations.

### Color Mapping Priority

1. Theme semantic names (preferred): `primary`, `secondary`, `success`, `warning`, `error`, `info`, `muted`
2. Base ANSI names (fallback): `black`, `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`, `gray`
3. Hardcoded hex (last resort, avoid): `#ff5733`

### Style Composition

Multiple styles can combine on the same element:

- Bold + colored → heading or emphasis
- Dim + gray → disabled or secondary information
- Reversed (bg/fg swap) → selected/focused item
- Underline → link or active tab indicator
