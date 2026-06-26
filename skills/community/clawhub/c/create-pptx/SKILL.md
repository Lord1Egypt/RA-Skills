---
name: create-pptx
description: >
  Create PowerPoint presentations (PPTX) using Python and python-pptx. Handles
  timelines, charts, diagrams, slide layouts, custom colors, shapes, connectors,
  text formatting, and slide transitions. Knows WPS compatibility pitfalls.
  Use when the user asks to: generate a PPT/PPTX file, create a presentation,
  make a slide deck, draw a timeline, visualize data as slides, or export
  something to PowerPoint. Also use when the user says "做成 PPT"、"生成幻灯片"、
  "做个演示文稿"、"做个 pptx".
---

# Create PowerPoint (python-pptx)

## Setup

```bash
pip install python-pptx   # or: uv pip install python-pptx
```

Output scripts to a logical location (e.g., `前端开发/demo/` or project folder),
then run with `python3 <script.py>` and open the result.

## Core helpers

Read and import `scripts/pptx_helpers.py` for ready-made drawing primitives:
background, horizontal/vertical lines, textboxes, ovals, diagonal connectors,
and fade transitions. Copy or `import` as needed.

Key units: **EMU** (English Metric Units). 1 pt = 12700 EMU, 1 cm ≈ 360000 EMU.
Standard 16:9 slide = 12192000 × 6858000 EMU.

## Workflow

1. **Understand the content** — milestones, categories, colors, # slides
2. **Plan layout** — compute X/Y positions in EMU up front; avoid magic numbers
3. **Build shapes** — use helpers or `slide.shapes.add_shape/add_textbox`
4. **Add transitions** — always call `add_fade_transition(slide)` from helpers
5. **Run and open** — `python3 script.py && open output.pptx`

### Multi-slide instead of click animations (WPS-safe default)

WPS does not reliably support click-triggered PowerPoint animations.
**Always use multiple slides** to reveal content progressively:

```
Slide 1 → skeleton / structure only
Slide 2 → skeleton + first data layer
Slide 3 → skeleton + all data layers
```

Add a fade transition (`add_fade_transition`) to each slide for smooth switching.

If the user explicitly asks for animations AND they are using Microsoft PowerPoint
(not WPS), you may attempt XML-based animations — but read `references/wps-compat.md`
first for the XML structure and known pitfalls.

## Common patterns

### Colors & theme

Define all colors as `RGBColor` constants at the top. Dark backgrounds look
premium — use near-black (`0x06, 0x0D, 0x1E`) with bright accents.

### Timeline layout

```python
TL_L, TL_R = 850000, 11950000        # left/right margins (EMU)
TL_W  = TL_R - TL_L
M_STEP = TL_W // 11                   # 12 months → 11 intervals

def month_x(m):                       # 1-based month → EMU x-position
    return TL_L + M_STEP * (m - 1)
```

### Collision resolution

When multiple cards share the same or nearby X position, spread them:

```python
def resolve_collisions(events, card_w, gap):
    events.sort(key=lambda e: e['cx'])
    need = card_w + gap
    for _ in range(120):
        moved = False
        for i in range(len(events) - 1):
            a, b = events[i], events[i+1]
            if b['cx'] - a['cx'] < need:
                push = (need - (b['cx'] - a['cx'])) / 2
                a['cx'] -= push; b['cx'] += push; moved = True
        if not moved:
            break
```

### Shape IDs for animation

`python-pptx` assigns shape IDs automatically. To retrieve them after creation:

```python
shp = slide.shapes.add_shape(...)
shape_id = shp.shape_id        # use this in animation XML
```

For connectors added via raw XML, read back the max existing ID first:

```python
def _max_existing_id(slide):
    return max((int(el.get('id')) for el in slide.element.iter()
                if el.get('id') and el.get('id').isdigit()), default=1)
```

## Template assets

Ready-to-use `.pptx` base files in `assets/`. Use them as the starting
`Presentation()` object to inherit their design/theme:

```python
from pptx import Presentation
prs = Presentation('/Users/scott/.cursor/skills/create-pptx/assets/business-dark.pptx')
```

| File | Style | Source |
|------|-------|--------|
| `assets/business-dark.pptx` | 深色商务 · Pitch Deck 风格 · 60 slides | Slidesgo "Product Vision Pitch Deck" (Attribution required) |
| `assets/education.pptx` | 明亮教育 · 笔记本课程风格 · 多 slides | Slidesgo "Notebook Lesson XL" (Attribution required) |

> **Attribution**: Free Slidesgo templates require keeping the attribution slide.
> When using these files, do NOT delete the last "Credits" slide.

## Reference files

Read the relevant file based on the task:

- **`references/pptx-patterns.md`** — EMU 单位速查、预设形状 ID、连接器 XML、
  过渡 XML、多段落文字框、典型脚本结构
- **`references/charts.md`** — python-pptx 原生图表 API：柱状、折线、饼图、散点、
  多系列、样式设置（当用户需要数据图表时读此文件）
- **`references/standard-slides.md`** — 标准商务幻灯片函数库：标题页、目录页、
  要点页、图文并排、数据页、章节分隔页、结尾页（当用户需要完整 PPT 结构时读此文件）
- **`references/wps-compat.md`** — WPS 动画兼容性踩坑记录（当用户提到 WPS 或
  动画效果异常时读此文件）
