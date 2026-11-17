# Input Handler — Sketch File

## Applies to
- `.sketch` files
- Exported Sketch JSON

## Precision characteristics

Sketch files provide **0px error** measurements — all values come from exact layer coordinates. This is the most accurate input type.

## Process

### Step 1 — Run the parser agent (automated, 0px error)

```bash
node <SKILL_DIR>/agents/parse-sketch.mjs design.sketch --output designs/<project>/
# Optional: filter to one artboard
node <SKILL_DIR>/agents/parse-sketch.mjs design.sketch --artboard "Home Screen" --output designs/<project>/
```

This produces `sketch-layers.json` with every layer's precise frame coordinates,
computed padding, fill colors, borders, and text attributes.
Read this file instead of parsing the .sketch ZIP manually.

**Manual fallback** (if agent is unavailable):

```bash
# Sketch files are ZIP archives
unzip -o "design.sketch" -d /tmp/sketch_extract
ls /tmp/sketch_extract/pages/
```

### Step 2 — Identify artboards

List all artboards and their sizes. If multiple exist, ask user which to extract.

### Step 3 — Precise spacing calculation

Sketch stores absolute positions. Compute all spacing mathematically:

```python
# Padding (child relative to parent)
padding_top    = child.y - parent.y
padding_left   = child.x - parent.x
padding_right  = (parent.x + parent.width) - (child.x + child.width)
padding_bottom = (parent.y + parent.height) - (child.y + child.height)

# Gap between siblings (vertical)
gap = sibling2.y - (sibling1.y + sibling1.height)

# Gap between siblings (horizontal)
gap = sibling2.x - (sibling1.x + sibling1.width)
```

### Step 4 — Color extraction

```python
def extract_color(fill):
    color = fill.get('color', {})
    r = int(color.get('red', 0) * 255)
    g = int(color.get('green', 0) * 255)
    b = int(color.get('blue', 0) * 255)
    a = color.get('alpha', 1)
    return f'rgba({r},{g},{b},{a})' if a < 1 else f'#{r:02x}{g:02x}{b:02x}'
```

### Step 5 — Font extraction

```python
def extract_font(attrs):
    return {
        'family': attrs.get('NSFontNameAttribute', 'system'),
        'size':   attrs.get('NSFontSizeAttribute', 16),
        'weight': attrs.get('NSFontTraitsAttribute', {}).get('NSFontWeightTrait', 0)
    }
```

### Step 6 — Token mapping

Map extracted exact values to tokens:
```
Measured: 16px → var(--spacing-md)       [EXACT]
Measured: #0066FF → var(--color-primary) [EXACT — matches token]
Measured: 44px height → var(--btn-height-mobile) [EXACT]
Measured: 8px radius → var(--radius-md)  [EXACT]
```

All Sketch-sourced values are `[EXACT]` — no uncertainty marking needed unless a value doesn't match any token.
