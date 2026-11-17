# Visual Review Protocol

## ⚠️ TOP PRIORITY RULE — Inspect every section you touched

After any edit that changes text, color, or geometry in a specific section of a diagram, **crop and inspect that section independently** before sending. Do not just glance at the full diagram at thumbnail scale and call it clean.

Specific failure mode to avoid: you edit note panel text, the text overflows the box because height wasn't increased, you look at the full diagram and it "looks fine" at small scale, you send it, the user notices the overflow. This is a recoverable but avoidable mistake. Don't let it happen.

**After every targeted edit:**
1. Re-export the PNG at 2x
2. Crop specifically to the section you changed
3. Inspect that crop at full size — check text fits, no overflow, no overlap
4. Only then look at the full diagram for global consistency

---

## The rule

Never declare a diagram "done" or deliver it without completing the screenshot-analyze-fix loop. Always.

The reason: diagrams look clean at thumbnail scale but have obvious issues at normal zoom — arrows cutting through boxes, text overflowing, zero-gap collisions between elements. The only way to catch these is to export and actually look.

---

## The loop

### 1. Export PNG at 2x scale with border
```bash
/Applications/draw.io.app/Contents/MacOS/draw.io --export --format png --output <path.png> --scale 2 --border 30 <file.drawio>
```

### 2. Read and inspect the image

For small diagrams (fits in one screen): read the full image, check every element.

For large/tall diagrams: **do not read as one image**. Crop into sections and inspect each separately using Python/PIL:

```python
from PIL import Image

img = Image.open("/path/to/diagram.png")
w, h = img.size

# Crop top section (first ~900px)
top = img.crop((0, 0, w, 900))
top.save("/path/to/diagram-top.png")

# Crop middle section
mid = img.crop((0, 850, w, 1750))
mid.save("/path/to/diagram-mid.png")

# Crop bottom section
bot = img.crop((0, 1700, w, h))
bot.save("/path/to/diagram-bot.png")
```

Overlap sections by ~50px to avoid missing elements at section boundaries. Read each cropped image separately.

### 3. What to check

- [ ] Text is fully visible and not clipped at box edges
- [ ] No text overflow below the bottom of its box
- [ ] Adequate breathing room between text and box borders (spacingLeft/Right/Top/Bottom applied)
- [ ] Arrows do not pass through or behind other boxes
- [ ] All arrows connect cleanly to their source and target
- [ ] Section label text is not intersected by flow arrows — if a section label sits between two connected boxes, the vertical arrow will pass through the label text; fix by moving the label definition to the END of the XML (so it renders on top) and adding `fillColor=#ffffff;strokeColor=none;` to block the arrow line behind the text
- [ ] Minimum 15–20px gap between any two boxes
- [ ] Zero-gap / touching boxes (especially where sub-item lists end and the next section begins) — **for every touching pair, ask: is this intentional?** Boxes should only touch if they are meant to communicate a tight, inseparable coupling in the flow. If the touching is accidental (just how spacing landed), add a gap. If it's intentional, leave it and document why in a comment or note.
- [ ] Section labels and colors are consistent
- [ ] Nothing looks cramped, overlapping, or colliding
- [ ] Left margin inside boxes — text should not start flush against the left wall
- [ ] Wide text panels — content does not overflow the right edge of the box

### 4. Common issues found in SOP diagrams

**Fan-out arrows cutting through boxes**
- Symptom: arrows from one step go directly to multiple stacked targets; lines visually pass through intermediate boxes
- Fix: chain arrows A→B1→B2→B3→B4 — each box connects to the next, not all from the source

**Zero-gap collision between sub-items and the next section**
- Symptom: bottom of the last sub-item box touches the top of the next section box (y + height = next y)
- Fix: cascade all elements below the collision point down by 20px minimum

**Text overflowing the right edge of wide panels**
- Symptom: paragraph text in a notes box runs past the box's right wall
- Fix: widen the box (e.g. 460→530px), then shift any adjacent elements to maintain clearance

**Text flush against left wall (no left margin)**
- Symptom: text starts at x=0 inside the box, touching the border
- Fix: ensure `spacingLeft=12` (or higher) is in the box style; also add `align=left` for multi-line content

**Text vertically centered and overflowing the bottom**
- Symptom: multi-line text is centered vertically but the box isn't tall enough, so the bottom lines clip
- Fix: add `verticalAlign=top` to the style so text flows from the top; recalculate height

### 5. Fix everything found

Edit the `.drawio` XML directly. Common fixes:
- Increase box height if text overflows (then shift everything below down by the same delta)
- Switch fan-out arrow patterns to chained arrow patterns
- Add `spacingLeft=12;spacingRight=12;spacingTop=10;spacingBottom=10;verticalAlign=top;` if missing
- Widen boxes for long-text panels; shift adjacent elements to clear the new width
- Increase gaps between boxes

### 6. Re-export and re-inspect

After every round of fixes, export a fresh PNG and re-read it. Repeat until the full checklist passes.

### 7. Deliver only after final clean pass

Only send the Drive link or final PNG after the visual review confirms it's clean.

---

## Token cost vs quality

Running multiple export-and-inspect cycles burns tokens. Do it anyway. A broken diagram costs more — Sam has to flag it, it has to be re-exported, and trust in the output erodes. The tokens spent on review are worth it every time.

---

## Known draw.io limitations to watch for

- `orthogonalEdgeStyle` does **not** route around obstacles — arrows go straight through other boxes if not laid out carefully
- All positions are **hardcoded** — changing a box height means manually shifting everything below it
- Text wraps based on box width — a line that fits at one width may not fit at a narrower width, increasing effective line count and overflowing box height
- PNG export has no interactive elements — hyperlinks and tooltips only work in the `.drawio` file itself
- `verticalAlign=middle` (the default) causes bottom-clipping on multi-line boxes — always use `verticalAlign=top` for content boxes
