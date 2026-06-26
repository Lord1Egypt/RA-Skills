# Layout Rules: Anti-Overlap & Text Sizing

These rules prevent the most common visual defects: text overflow, element overlap, and cramped layouts.

---

## ⚠️ Critical Rules (Learned from Production Diagrams)

These mistakes have caused real defects. Follow them every time.

### 1. Destination box must span ALL incoming arrow y-coordinates
If multiple arrows fan into one box from different y positions, the destination box height must cover the full range.
```
dest_y     ≤ min(arrow_y for all arrows)
dest_y + dest_height ≥ max(arrow_y for all arrows)
```
If the box is too short, arrows will appear to float above or below it.

### 2. Text must never exceed box width
After calculating text width, verify:
```
text_width + horizontal_padding < box_width
```
For long single-line text in wide footer/banner boxes: **always split onto 2 lines** rather than making the box wider than the canvas. Use `\n` in the text field and increase box height by one line-height.

### 3. Arrow coordinates use exact box edges
- Horizontal left→right: `arrow_x = src_x + src_width`, `arrow_y = src_y + src_height/2`, `width = dest_x - arrow_x`
- Vertical top→bottom: `arrow_x = src_x + src_width/2`, `arrow_y = src_y + src_height`, `height = dest_y - arrow_y`
- **No overlap, no gap** — start/end exactly at box edges

### 5. Title and subtitle must span the full canvas width
After placing all elements, calculate the canvas x range: `min_x` to `max_x + max_width`. Then set:
```
title_x = min_x
title_width = (max_x + max_width) - min_x
```
This ensures `textAlign: "center"` actually centers the text over the whole diagram, not just part of it.
For each arrow, confirm:
- Start point lands on a box edge (not inside, not outside)
- End point lands on a box edge (not inside, not outside)
- Arrow y is within the vertical range of the destination box

---
## Text Sizing Formula

Excalidraw does NOT auto-size containers. You must calculate dimensions manually.

### Character Width Estimates (fontFamily: 3, monospace)

| fontSize | Avg char width (px) | Line height (px) |
|----------|---------------------|-------------------|
| 12 | 7.2 | 15 |
| 14 | 8.4 | 17.5 |
| 16 | 9.6 | 20 |
| 20 | 12.0 | 25 |
| 24 | 14.4 | 30 |
| 28 | 16.8 | 35 |

### Container Sizing

For text inside a rectangle:

```
text_width  = max_line_length × char_width
text_height = num_lines × line_height

container_width  = text_width + horizontal_padding
container_height = text_height + vertical_padding
```

**Minimum padding:**
- Horizontal: `40px` (20px each side)
- Vertical: `30px` (15px each side)

**Example:** "Process Data" at fontSize 16:
- 12 chars × 9.6 = 115.2px text width
- 1 line × 20 = 20px text height
- Container: **156px × 50px** (115 + 40, 20 + 30)

**Example:** "Send Verification\nEmail to User" at fontSize 16:
- 18 chars × 9.6 = 172.8px (longest line)
- 2 lines × 20 = 40px text height
- Container: **213px × 70px** (173 + 40, 40 + 30)

### Multi-line Text

When a label is long (>15 chars at fontSize 16, >12 chars at fontSize 20), use `\n` to break it:

```json
{
  "text": "Send Verification\nEmail to User",
  "originalText": "Send Verification\nEmail to User"
}
```

Then size the container for the longest line and the total number of lines.

---

## Positioning Text Inside Containers

The text element's `x` and `y` must be centered within the container:

```
text_x = container_x + (container_width - text_width) / 2
text_y = container_y + (container_height - text_height) / 2
```

Set `textAlign: "center"` and `verticalAlign: "middle"` and `containerId: "<parent_id>"`.

---

## Element Spacing

### Minimum Gaps

| Between | Minimum gap |
|---------|-------------|
| Adjacent shapes (same row/column) | **60px** |
| Shape and its arrow label | **10px** |
| Parallel flow rows/columns | **100px** |
| Sections/groups | **120px** |
| Diagram edge to nearest element | **80px** (padding) |

### Grid Alignment

Snap element positions to a 20px grid for clean alignment:

```
x = round(x / 20) * 20
y = round(y / 20) * 20
```

### Arrow Routing

- Arrows should have **at least 20px clearance** from non-connected elements.
- For arrows that would cross elements, add waypoints:
  ```json
  "points": [[0, 0], [50, 0], [50, -80], [150, -80], [150, 0], [200, 0]]
  ```
- Prefer orthogonal (right-angle) routing over diagonal for clean diagrams.

### ⚠️ Arrow Connection Rule — ALWAYS VERIFY

**Arrows MUST visually connect source to destination. Floating arrows are a critical defect.**

**MANDATORY: For every horizontal left→right arrow:**
- Arrow `x` = `src_x + src_width` (right edge of source box)
- Arrow `y` = `src_y + src_height / 2` (vertical center of source box)
- Arrow end x = `dest_x` (left edge of destination box)
- Arrow `width` = `dest_x - (src_x + src_width)`
- Arrow `points` = `[[0,0],[width,0]]`

**MANDATORY: For every vertical top→bottom arrow:**
- Arrow `x` = `src_x + src_width / 2` (horizontal center of source box)
- Arrow `y` = `src_y + src_height` (bottom edge of source box)
- Arrow end y = `dest_y` (top edge of destination box)
- Arrow `height` = `dest_y - (src_y + src_height)`
- Arrow `points` = `[[0,0],[0,height]]`

**Note:** The destination box must be tall enough to span the arrow's y coordinate, otherwise the arrow will appear to float. Adjust box height to cover all incoming arrows.

For horizontal intra-row arrows (connecting boxes left→right):
- Arrow `y` must equal the **vertical center of both boxes**: `box_y + box_height / 2`
- Arrow `x` (start) = `src_x + src_width`
- Arrow `width` = `dest_x - (src_x + src_width)`

**Checklist before finalizing any arrow:**
1. Start point (x,y) lies exactly on the edge of the source element
2. End point (x + width, y + height) lies exactly on the edge of the destination element
3. No arrow points into empty whitespace between unconnected elements
4. For `startBinding`/`endBinding`: verify `elementId` matches the actual element id

**Common mistake:** Using a fixed x=700 for all vertical arrows when the target box center is at a different x. Always calculate x from the destination box position.

**When source and destination have different center-x values**, use an L-shaped waypoint path instead of a diagonal:
```json
// Example: source cx=1000, dest cx=360, vertical drop=114px
// Route: down 57px, left 640px, down 57px
"x": 1000, "y": 470,
"width": -640, "height": 114,
"points": [[0,0], [0,57], [-640,57], [-640,114]]
```
This keeps routing orthogonal (no diagonals) and visually connects to both boxes.

**MANDATORY verification step for every arrow:**
After writing arrow JSON, trace the path manually:
- Start point: `(arrow.x + points[0][0], arrow.y + points[0][1])`
- End point: `(arrow.x + points[-1][0], arrow.y + points[-1][1])`
- Verify start point lies on source element's edge
- Verify end point lies on destination element's edge
- If either check fails, fix the coordinates before rendering

---

## Common Layout Patterns

### Horizontal Flow (LR)
```
[elem1] --60px-- [elem2] --60px-- [elem3]
   y: same for all elements in a row
   x: prev_x + prev_width + 60
```

### Vertical Flow (TB)
```
[elem1]
  |  60px gap
[elem2]
  |  60px gap
[elem3]
   x: same for all elements in a column
   y: prev_y + prev_height + 60
```

### Decision Branching
```
                [elem1]
                   |
              {decision}
             /          \
    --60px--             --60px--
   [yes_path]          [no_path]
```
- Branch targets should be at least 100px apart horizontally.
- Decision diamond: use 140×90 minimum for short labels.

### Fan-out
```
              [source]
           /     |     \
     --80px-- --80px-- --80px--
    [t1]     [t2]     [t3]
```
- Space targets evenly; center the source above them.

---

## Diamond (Decision) Sizing

Diamonds are trickier because the visible text area is only ~50% of the bounding box.

```
diamond_width  = text_width × 2 + 40
diamond_height = text_height × 2 + 20
```

**Example:** "Valid?" at fontSize 16:
- 6 chars × 9.6 = 57.6px
- Diamond: **155px × 60px** (58 × 2 + 40, 20 × 2 + 20)

---

## Preventing Overlap: Checklist

Before rendering, verify:

1. **No coordinate collisions:** For every pair of elements, check:
   ```
   elem1.x + elem1.width + min_gap < elem2.x  (if side by side)
   elem1.y + elem1.height + min_gap < elem2.y  (if stacked)
   ```

2. **Text fits in container:** Container dimensions ≥ text dimensions + padding.

3. **Arrow labels don't collide:** If an arrow has a label, place it offset from the midpoint, not overlapping other elements.

4. **Sections don't encroach:** Adjacent sections need 120px+ gap.

5. **Diamond text visible:** Diamond containers are 2× wider/taller than text needs.
