# Arc Text Icon — Parameter Tuning Guide

This reference covers parameter tradeoffs for the arc-text-icon skill. Read SKILL.md first for the geometry.

## Curvature: Half-angle vs Visual Effect

`half_angle` (degrees) is the half-arc opening measured from vertical.

| half_angle | Visual | Best for |
|---|---|---|
| 20-25° | Subtle gentle curve, almost flat | Banner headings, very wide labels |
| 30-40° | Mild curve, looks like a stamp | Wide badges, certificates |
| 45-55° | Clearly arc-shaped, well balanced | **Default. Outer packaging.** |
| 55-65° | Pronounced arc, dramatic | Small seals, decorative |
| 70-80° | Almost circular | Compact badges, ribbon ends |

**Hard limit**: `half_angle` close to 90° makes the text wrap nearly half the circle, characters start overlapping at the bottom.

## Font Size vs Chord Length Tradeoff

For N characters, the chord (horizontal projection) divides into roughly N segments. To avoid overlap:

```
chord / (N - 1) > font_size * 1.05 + 5
```

Equivalently:
```
chord > (N - 1) * (font_size * 1.10)
```

| N | font_size | min chord (safe) | recommended chord |
|---|---|---|---|
| 8 | 60 | 528 | 700 |
| 8 | 80 | 704 | 900 |
| 10 | 70 | 770 | 1000 |
| 10 | 90 | 990 | 1300 |
| 12 | 70 | 924 | 1200 |
| 12 | 80 | 1056 | 1500 (default) |
| 12 | 90 | 1188 | 1500 (risky) |
| 14 | 60 | 924 | 1200 |
| 14 | 70 | 1078 | 1400 |
| 16 | 50 | 880 | 1100 |

**Default**: 12 chars, `font_size=78, chord=1500, half_angle=55°` → spacing 146 px vs ink 84 px → 62 px gap. Comfortable.

## Font Selection Guide

| Font | Path | Style | Use when |
|---|---|---|---|
| `kai` (楷体) | arphic/ukai.ttc | Brushstroke, traditional, hand-written feel | **Default for outer packaging.** Gift boxes, certificates, vintage labels. |
| `hei` (黑体) | noto/NotoSansCJK-Bold.ttc | Sans-serif, modern, clean | Tech products, contemporary brands, posters |
| `song` (宋体) | noto/NotoSerifCJK-Bold.ttc | Serif, scholarly, official | Government documents, formal seals, books |

If you need a specific style not in this list, install additional fonts:
- `apt install fonts-arphic-ukai` (楷体) — already done
- `apt install fonts-arphic-uming` (明体/宋体)
- `apt install fonts-wqy-microhei` (文泉驿微米黑)

## Color & Stroke

- **Color**: any hex (`#000000` / `#C8102E` red / `#FFD700` gold). Use named colors: red `red`, gold `gold`.
- **Stroke**: optional. Set `--stroke-color` to enable. Typical widths: 1-2 px thin, 3-4 px bold seal, 5+ px decorative.
- **Color combinations that work well**:
  - Black text, no stroke — official, document-grade
  - Red `#C8102E` text + gold `#FFD700` stroke 3px — festive seal
  - White text on dark bg (`--bg #1a1a2e`) — modern brand
  - Black text on gold bg (`--bg #FFD700`) — luxury

## When to Render Multiple Sizes

Always render at least two backgrounds:
1. **Transparent PNG** — for designers / downstream compositing
2. **White-bg preview PNG** — for chat clients that don't composite alpha (Feishu, Telegram, Slack often show transparent PNGs as blank)

For high-end output, optionally also render:
3. Themed bg (red `#8B0000`, navy `#1a1a2e`, gold `#FFD700`) for direct comparison

## When Things Go Wrong — Diagnosis Tree

```
Empty output (0 strong pixels)
  → Geometry placed all characters off-canvas
  → Verify: dy range ∈ [50, canvas_h-50]? r < canvas_h? cy inside or just outside?

Characters stacked in one corner (dx clustered)
  → Used cos instead of sin for x projection
  → Fix: dx = cx + r*sin(theta)

Characters tilted inward (字头朝圆心)
  → rotation = +theta
  → Fix: rotation = -theta

Characters tilted 90° (laying flat)
  → rotation = theta ± 90
  → Fix: rotation = -theta (only)

Characters all reversed (right-to-left)
  → progress = 1 - i/n instead of i/n
  → Fix: progress = (i + 0.5) / n

User says "字距没变" (spacing didn't change)
  → Modified progress_padding instead of font_size / chord
  → Fix: progress_padding only adjusts end margins; for inter-character gap, change font_size or chord
```