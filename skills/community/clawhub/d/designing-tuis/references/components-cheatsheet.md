# Components Cheatsheet

Source of truth: tui-studio component defaults (snapshot for skill usage).

Each component includes:
- **Defaults**: props, layout, and style defaults
- **Visual Signature**: how to recognize this component in a screenshot
- **Disambiguation**: how to distinguish from similar-looking components

## Layout

### Box
- Category: layout
- Props default: `{ width: "auto", height: "auto" }`
- Layout default: `{ type: "flexbox", direction: "column", padding: 1, gap: 1 }`
- Style default: `{ color: "white", border: true, borderStyle: "single", borderColor: "white" }`
- Visual signature:
  - Rectangular region with visible border (single/double/rounded)
  - Contains multiple different types of child content
  - May have a title rendered in the top border
- Disambiguation:
  - vs Modal: Modal floats above content and is centered; Box is in-flow
  - vs Grid: Grid has uniform cells; Box is a single container with arbitrary children

### Grid
- Category: layout
- Props default: `{ width: "fill", height: "fill", columns: 2 }`
- Layout default: `{ type: "grid", gapX: 1, gapY: 0 }`
- Style default: `{ color: "white" }`
- Visual signature:
  - Multiple children arranged in uniform rows and columns
  - Equal-width columns (or near-equal)
  - Children are visually similar or same component type
- Disambiguation:
  - vs Box with Row children: Grid has uniform cell sizing; Row children may have different widths
  - vs Table: Table has a header row and data semantics; Grid is a layout container

## Display

### Text
- Category: display
- Props default: `{ content: "", wrap: true, align: "left" }`
- Layout default: `{ width: "auto", height: "auto" }`
- Style default: `{ color: "white", bold: false, dim: false }`
- Visual signature:
  - Single line or short inline text
  - No border, no interactive indicators
  - May have color or bold/dim styling
- Disambiguation:
  - vs Heading: Heading is bold + colored (cyan) and acts as section title
  - vs Input: Input has a border and/or cursor indicator; Text is static
  - vs Paragraph: Paragraph is multi-line wrapping text; Text is typically single-line

### Heading
- Category: display
- Props default: `{ level: 1, content: "Heading" }`
- Layout default: `{ width: "auto", height: "auto" }`
- Style default: `{ color: "cyan", bold: true }`
- Visual signature:
  - Bold text, often colored (cyan/white)
  - Appears at the top of a section or panel
  - Single line, larger visual weight than surrounding text
- Disambiguation:
  - vs Text: Text is not bold by default and has neutral color
  - vs Tabs active label: Tabs have multiple peer labels; Heading stands alone

### Paragraph
- Category: display
- Props default: `{ content: "", wrap: true }`
- Layout default: `{ width: "fill", height: "auto" }`
- Style default: `{ color: "white" }`
- Visual signature:
  - Multi-line wrapping text block
  - Fills available width
  - No border, no interactive elements
- Disambiguation:
  - vs Text: Text is single-line or short; Paragraph is multi-line prose
  - vs List: List has homogeneous items with prefixes; Paragraph is continuous prose

### Divider
- Category: display
- Props default: `{ orientation: "horizontal", char: "─" }`
- Layout default: `{ width: "fill", height: 1 }`
- Style default: `{ color: "gray" }`
- Visual signature:
  - Horizontal line of repeated characters (─── or ═══ or ---)
  - Spans full width of parent container
  - Height is exactly 1 row
- Disambiguation:
  - vs Box border: Box border forms a closed rectangle; Divider is a single line
  - vs Table row separator: Table separators appear between data rows within a table structure

## Input

### Input
- Category: input
- Props default: `{ value: "", placeholder: "", disabled: false }`
- Layout default: `{ width: 24, height: 1 }`
- Style default: `{ color: "white", border: true, borderColor: "white" }`
- Visual signature:
  - Single-line bordered area
  - May show cursor indicator (│ or _)
  - May have placeholder text (dim/gray)
  - Fixed width, height of 1 content row
- Disambiguation:
  - vs Text: Text has no border and is not interactive
  - vs Select: Select has a dropdown arrow (▾) or expanded options list
  - vs PasswordInput: PasswordInput shows mask characters (***) instead of actual text

### PasswordInput
- Category: input
- Props default: `{ value: "", mask: "*" }`
- Layout default: `{ width: 24, height: 1 }`
- Style default: `{ color: "white", border: true, borderColor: "white" }`
- Visual signature:
  - Same as Input but content shows mask characters (*** or •••)
  - May have a "password" or "secret" label nearby
- Disambiguation:
  - vs Input: Input shows actual text; PasswordInput shows mask characters

### Select
- Category: input
- Props default: `{ options: [], selectedIndex: 0 }`
- Layout default: `{ width: 24, height: 5 }`
- Style default: `{ color: "white", border: true, borderColor: "white" }`
- Visual signature:
  - Bordered area with multiple options listed vertically
  - One option highlighted/selected
  - May have dropdown arrow (▾) in collapsed state
  - Fixed width, multi-row height
- Disambiguation:
  - vs List: List is a data display component (wider, more items); Select is a form input (compact, fixed width)
  - vs RadioGroup: RadioGroup has explicit radio markers (◉ ○); Select may use highlight only

### Checkbox
- Category: input
- Props default: `{ label: "", checked: false }`
- Layout default: `{ width: "auto", height: 1 }`
- Style default: `{ color: "white" }`
- Visual signature:
  - Single line with check marker (☑ ☐ [x] [ ] ✓ ✗)
  - Label text follows the marker
  - Height is exactly 1 row
- Disambiguation:
  - vs RadioGroup option: Radio uses circular markers (◉ ○); Checkbox uses square markers (☑ ☐)
  - vs List item: List items may have prefixes but are part of a scrollable collection

### RadioGroup
- Category: input
- Props default: `{ options: [], selectedIndex: 0 }`
- Layout default: `{ width: "auto", height: "auto" }`
- Style default: `{ color: "white" }`
- Visual signature:
  - Multiple lines with circular/radio markers (◉ ○ or (•) ( ))
  - Exactly one option selected (filled marker)
  - Mutually exclusive selection
- Disambiguation:
  - vs List: List is for data display with arbitrary prefixes; RadioGroup has exclusive radio markers
  - vs Checkbox group: Checkboxes allow multi-select (square markers); RadioGroup is single-select (round markers)
  - vs Select: Select is bordered and compact; RadioGroup shows all options inline

### Slider
- Category: input
- Props default: `{ min: 0, max: 100, value: 50, step: 1 }`
- Layout default: `{ width: 24, height: 1 }`
- Style default: `{ color: "green" }`
- Visual signature:
  - Horizontal bar with a position indicator
  - Track line with filled/unfilled portions
  - May show numeric value
  - Height is exactly 1 row
- Disambiguation:
  - vs ProgressBar: ProgressBar is read-only display; Slider is interactive input
  - vs Divider: Divider is a simple line separator; Slider has a position indicator

## Data

### Table
- Category: data
- Props default: `{ columns: [], rows: [], selectedRow: 0 }`
- Layout default: `{ width: "fill", height: 10 }`
- Style default: `{ color: "white", border: true, borderColor: "white" }`
- Visual signature:
  - First row is header (bold/reversed/underline-separated)
  - Multiple aligned columns, possibly separated by │
  - Data rows below header with consistent column alignment
  - May have one row highlighted (selected row)
- Disambiguation:
  - vs List: List has no header row and no column alignment
  - vs Grid: Grid is a layout container; Table is a data display with header semantics

### List
- Category: data
- Props default: `{ items: [], selectedIndex: 0 }`
- Layout default: `{ width: "fill", height: 8 }`
- Style default: `{ color: "white", border: true, borderColor: "white" }`
- Visual signature:
  - Multiple homogeneous rows, vertically arranged
  - Possible prefix symbols (▸ ● ✓ ─ * - [ ])
  - One row may be highlighted/reversed (selected state)
  - May have scroll indicators (▲ ▼ or 1/N counter)
- Disambiguation:
  - vs Table: Table has a header row (bold or underline-separated); List does not
  - vs Tree: Tree has indentation levels (├ └ │); List items are flat
  - vs RadioGroup: RadioGroup has mutually exclusive radio markers (◉ ○); List is a general-purpose collection

### Tree
- Category: data
- Props default: `{ nodes: [], selectedPath: [] }`
- Layout default: `{ width: "fill", height: 10 }`
- Style default: `{ color: "white", border: true, borderColor: "white" }`
- Visual signature:
  - Indented levels (2-4 spaces per level)
  - Tree-drawing characters: ├ └ │ ─
  - Expand/collapse markers: ▸ ▾ + -
  - Hierarchical parent-child relationships visible through indentation
- Disambiguation:
  - vs List: List has no indentation; all items are at same level
  - vs Nested Box: Box uses borders to show hierarchy; Tree uses indentation and line-drawing chars

### ProgressBar
- Category: data
- Props default: `{ value: 0, max: 100, showLabel: true }`
- Layout default: `{ width: "fill", height: 1 }`
- Style default: `{ color: "green", trackColor: "gray" }`
- Visual signature:
  - Horizontal bar filling available width
  - Partially filled with color (green), remainder in track color (gray)
  - May show percentage label (e.g., "75%")
  - Height is exactly 1 row
- Disambiguation:
  - vs Slider: Slider is interactive (user can drag); ProgressBar is read-only
  - vs Divider: Divider is uniform; ProgressBar has two-tone fill

## Navigation

### Tabs
- Category: navigation
- Props default: `{ tabs: [], activeIndex: 0 }`
- Layout default: `{ width: "fill", height: 3 }`
- Style default: `{ color: "white", activeColor: "cyan" }`
- Visual signature:
  - Horizontally arranged text labels (typically 2-6)
  - One label is in active state (reversed/underlined/bold/colored)
  - Usually positioned at top of a content area
  - May have separator characters between labels
- Disambiguation:
  - vs Breadcrumb: Breadcrumb has path separators (/ or >); Tabs are parallel peers
  - vs Button group: Buttons typically have borders; Tabs are flatter
  - vs Heading: Heading is a single label; Tabs have multiple peer labels

### Breadcrumb
- Category: navigation
- Props default: `{ items: [] }`
- Layout default: `{ width: "fill", height: 1 }`
- Style default: `{ color: "gray", separator: "/" }`
- Visual signature:
  - Single line of text items separated by / or > characters
  - Represents a path or navigation hierarchy
  - Last item may be highlighted (current location)
- Disambiguation:
  - vs Tabs: Tabs are parallel navigation options; Breadcrumb shows hierarchical path
  - vs Text: Plain text doesn't have separator-delimited path structure

## Overlay

### Modal
- Category: overlay
- Props default: `{ open: true, title: "", closable: true }`
- Layout default: `{ width: 50, height: 12 }`
- Style default: `{ color: "white", border: true, borderColor: "cyan" }`
- Visual signature:
  - Centered floating rectangular box
  - Usually has a title bar and close indicator (× or [X])
  - May have a dimmed/dark backdrop overlay
  - Appears above other content (the only Z-axis overlay in TUI)
- Disambiguation:
  - vs Box: Box is in-flow content; Modal floats above content
  - vs Toast: Toast is single-line, auto-dismissing, and has no border/title

### Toast
- Category: overlay
- Props default: `{ message: "", variant: "info", durationMs: 2500 }`
- Layout default: `{ width: "auto", height: 1 }`
- Style default: `{ color: "white", bgColor: "blue" }`
- Visual signature:
  - Single-line notification message
  - Background color indicates variant (blue=info, green=success, red=error, yellow=warning)
  - Appears briefly and auto-dismisses
  - Usually at bottom or top edge of screen
- Disambiguation:
  - vs Modal: Modal is multi-line with border and title; Toast is single-line and ephemeral
  - vs Text: Text is persistent; Toast is temporary
