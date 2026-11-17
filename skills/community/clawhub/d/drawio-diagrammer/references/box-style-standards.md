# Box Style Standards

## The core problem

draw.io adds zero internal padding to boxes by default. Text starts flush against the box border. This causes:
- Text that looks cramped or sits on the edge
- Text that overflows the box bottom when content wraps
- Diagrams that look unprofessional or unreadable at normal zoom

## Universal fix — apply to every content node

Add these spacing attributes to every content node style string:

```
spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;verticalAlign=top;
```

`verticalAlign=top` is required on multi-line boxes — without it, draw.io centers text vertically, which causes text to overflow at the bottom when the box is taller than the text.

### Full example node style (flowchart/SOP step)
```xml
style="rounded=1;whiteSpace=wrap;html=1;fontSize=10;align=left;
       spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;verticalAlign=top;"
```

### Full example node style (section header / single-line label)
```xml
style="rounded=1;whiteSpace=wrap;html=1;fontSize=11;fontStyle=1;align=center;
       fillColor=#dae8fc;strokeColor=#6c8ebf;
       spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;"
```

### For small label-only boxes (legend items, single-word labels)
```xml
style="rounded=1;whiteSpace=wrap;html=1;fontSize=10;
       spacingLeft=6;spacingRight=6;spacingTop=4;spacingBottom=4;"
```

## Height estimation formula

Since all heights are hardcoded, use this to avoid text overflow:

1. Count the number of `&#xa;` line breaks in the value text (each = one line)
2. Add 1 for the final line (the one without a trailing `&#xa;`)
3. Estimate visual wrapping: at fontSize=10 in a box with 12px left + 12px right spacing, effective text width = (boxWidth - 24px). Lines longer than ~8 chars per 10px of effective width will wrap.
4. Multiply total visual lines by **~16px** at `fontSize=10`
5. Add spacingTop + spacingBottom (typically 10 + 10 = 20px)
6. Add **~10px** buffer
7. Round up to the nearest 10px — always round generously

**Example:** 4 visual lines of text at fontSize=10 with 12/10 spacing
- 4 × 16px = 64px content
- 64 + 20 (spacing) + 10 (buffer) = 94px → round up to **100px**

When in doubt, make boxes taller. Extra whitespace at the bottom is invisible; overflow is visible and broken.

## After changing a box height

If you increase a box height by N pixels, **every element below it must shift down by N pixels**.
draw.io has no reflow — positions are absolute. Missing this cascade creates overlaps.

## Wide-box guidance for long-text panels

When a box contains paragraph-length text (Operating Notes, description panels, etc.):
- Width 460px is often not enough — try **530px or wider**
- After widening a box, check if any adjacent elements (legend boxes, note panels) now collide
- Shift adjacent elements outward to maintain 15–20px clearance

## Minimum spacing between boxes

- Always leave at least **15–20px gap** between any two boxes (never 0 or touching)
- For dense diagrams: use 20–30px minimum
- For section headers above content blocks: 10px gap is acceptable if intentional
- Between sub-items in a vertical list: 20px gap is recommended

## SOP / process diagram layout pattern

For SOPs and process flows with step descriptions, use a two-column layout:

```
LEFT COLUMN (x=50–200): numbered step boxes, main flow runs vertically
RIGHT COLUMN (x=680–1250): note/description boxes aligned to their step
```

- Main flow step boxes: width=550, left-aligned at ~x=50
- Note/annotation boxes: positioned to the right, x=680 or similar
- Step-to-note gap: minimum 30px horizontal clearance between left and right columns
- Between step boxes in main flow: 140px minimum vertical gap (step bottom to next step top)
- Between sub-items in a vertical list under a step: 20px gap, chained arrows A→B1→B2→B3

## Arrow routing — chained vs fan-out

**Fan-out (BROKEN):** One source box connects directly to multiple stacked targets.
```
A → B1
A → B2   ← orthogonalEdgeStyle routes arrows THROUGH B1 and B2
A → B3
```
draw.io `orthogonalEdgeStyle` does NOT route around obstacles. Arrows go straight through other boxes.

**Chained (CORRECT):** Source connects to first target, which connects to next, and so on.
```
A → B1 → B2 → B3
```
No arrows cross through any boxes. **Always use chaining for vertical sub-item lists.**

## Section labels sitting in the arrow path

In vertical flow diagrams, section labels (e.g. "TUESDAY – THURSDAY — Execution Days") often sit between two connected boxes. The vertical flow arrow passes straight through x = center of the flow column, which cuts directly through the label text.

**The fix — white fill + z-order:**

1. Give the label `fillColor=#ffffff;strokeColor=none;` so it has a solid white background that covers the arrow line behind it.
2. Move the label definition to the **end of the XML**, after all edges. draw.io renders elements in document order — last defined = renders on top. This ensures the white label paints over the arrow instead of the arrow painting over the label.
3. **Width constraint:** The label width must not extend into adjacent column panels. If note boxes start at x=320, the label must end before x=310. Use width=250 max when starting at x=60 with note panels at x=320.

**What it looks like when correct:**
- The flow arrow is visually broken by the white label box
- The arrowhead appears cleanly below the label (at the entry point of the next box)
- No white bleed into adjacent panels

**What it looks like when wrong:**
- Arrow line cuts through label text (label has no fill, or label is below edges in z-order)
- White rectangle bleeds into adjacent note panel corner (label width too wide)

**Rule of thumb:** After placing any section label in a vertical flow, check:
- Does the arrow pass through this label's y-range? If yes → apply white fill + move to end of XML
- Does the label's x + width overlap with adjacent columns? If yes → trim width

## Exit point spread (partial fix only)

Using `exitX` / `exitY` attributes on edges can spread arrow origins across the source box:
```xml
style="edgeStyle=orthogonalEdgeStyle;exitX=1;exitY=0.1;exitDx=0;exitDy=0;"
```
This helps when targets are close together but does NOT fix crossing when targets are far apart vertically. Chaining is the real fix.
