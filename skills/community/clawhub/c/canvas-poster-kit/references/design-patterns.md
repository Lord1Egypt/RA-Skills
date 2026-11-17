# Design Patterns — Topic-Driven Palettes & Layout Blocks

Battle-tested patterns from production posters. Choose structure and color by **topic semantics**, not by "what looked good last time."

## Palette selection logic

Ask: what does this topic *feel* like? Match the palette to the answer.

| Topic domain | Palette | Rationale |
|---|---|---|
| AI / tech / digital | bg `#000814`, card `#001d3d`, accent `#00b4d8`, muted `#90e0ef` | Dark base + neon cyan = "systems running" feel |
| Empathy / kindness / care | bg `#FBF6F1` cream, accent `#E57F4D` coral, band `#EBBB9A` peach, deep `#B85F3D` | Warm human tones; never dark-tech for warmth topics |
| Finance / trust | navy + gold accents | Institutional gravity |

**Rule:** if the user praises a previous palette ("上次的配色不错"), read it as continuity praise — do NOT auto-reuse it for a new topic. The new topic's semantics decide.

### Semantic role colors (overlay on the base palette)

For content with *roles* (agents, statuses, actors), give each role a consistent hue:
- indigo `#4338CA`/`#6366F1` → orchestrator/lead
- purple `#8B7CF6`/`#A78BFA` → sub-components
- green `#22C55E` → success/complete
- amber `#F59E0B` → human review / caution

The functional meaning behind color is what users value — color as decoration is wasted ink.

## Extracting colors from a reference image (programmatically)

Never eyeball a reference palette. PIL sampling:

```python
from PIL import Image
from collections import Counter

img = Image.open('ref.png').convert('RGB')
img = img.resize((50, 50))                      # average out noise
pixels = list(img.getdata())
common = Counter(pixels).most_common(10)        # dominant colors

# Structural zones (strips/bands live at edges):
w, h = img.size
top    = Counter(img.getpixel((x, 2))  for x in range(w)).most_common(3)
bottom = Counter(img.getpixel((x, h-3)) for x in range(w)).most_common(3)
```

Then **echo the reference's structure**, not just its colors: if the reference has a dark top strip + accent hairline + bottom band, reproduce that vertical framework on your poster (`addTopFramework` / `addBottomBand` pattern) for instant visual kinship.

## Reusable layout blocks

A poster = background + title block + 2–4 body blocks + footer. Mix these blocks:

**Hub-and-spoke (central concept + satellites)**
- Center: concentric glow circles — 3–4 `arc`s of decreasing radius, decreasing `shadowBlur`, highest transparency first (60% → 30% → solid)
- Satellites: rounded rects connected with dashed lines (`ctx.setLineDash([6, 6])`), color-coded by role

**Flow strip (process/steps)**
- 5 boxes in a row + arrow glyphs between; each box a rounded rect with number badge and 2-line label

**Feature cards (2×2 or 1×4 grid)**
- Rounded rect + 5px left accent bar (role color) + heading + 2-line body
- Card tint variations by function: `#FBE3D5` pain-point, `#F8E0D0` emphasis, `#EFD9C7` outcome

**Stats row**
- 3–4 big numbers (36–44px accent) over small captions (14px muted); align on a shared baseline

**Top framework / bottom band (when echoing a reference)**
- Top: dark strip (0.28" ≈ 25px logical) + accent hairline (8px) + soft transition (4px)
- Bottom: transition strip + accent band (~35px)

## Typography

| Role | Font | Notes |
|---|---|---|
| Headers | `"Trebuchet MS", sans-serif` 700 | Slight tech personality |
| Body | `Calibri, sans-serif` 400 | Neutral, compact |
| Code/kickers | `Consolas, monospace` | Instant "tech" vibe on dark bg |

Scale by hierarchy: title 44px, section head 24–28px, card head 20–22px, body 15–16px, caption 13–14px (logical px at ~900px width). Stick to system fonts — no webfont loading needed, exports stay self-contained.

## Glow technique

```js
ctx.save();
ctx.shadowColor = accent;
ctx.shadowBlur = 10–16;              // subtle on dark bg; more reads as blur, not glow
ctx.fillStyle = accent;
/* draw shape */
ctx.restore();                        // ALWAYS restore — glow leaks to later draws otherwise
```

On light/cream backgrounds, glow reads as dirt — use solid accent fills + left bars instead.
