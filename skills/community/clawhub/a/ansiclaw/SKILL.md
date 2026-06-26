---
name: ansiclaw
description: "Draws BBS compatible ANSI art via the Clawbius API"
---

# ANSIClaw 🦞🎨

Draw ANSI art via the local Clawbius REST API. Use anytime the user asks for ANSI art, or when you want to create it on your own initiative.

Project home: 

  - Github: https://github.com/n2tr0n/ansiclaw
  - Clawhub: https://clawhub.ai/n2tr0n/ansiclaw

Requirements:

  - Clawbius (https://github.com/n2tr0n/clawbius); API enabled ANSI drawer - runs on tcp/7777
  - node.js v18 for running Clawbius
  - Python 'requests' (pip install requests) for scripting API calls.


---

## ⛔ HARD RULES — BEFORE ANYTHING ELSE

1. **NEVER modify reference files.** Files in `resources/` are your source material. Do not open them via `/api/file/open` without immediately calling `/api/file/new` afterward to switch to a fresh canvas. Opening a file in Clawbius makes it the active canvas — any draw calls will corrupt it. Analyze reference files by reading canvas data ONLY, then immediately create a new canvas before drawing.

2. **NEVER save or export over an existing ANS file without operators explicit instruction.** Always use a new versioned filename (e.g. `flower_v2.ans`).

3. **NEVER use `/api/file/export-png`** — the correct endpoint is **`/api/file/export/png`** (with a slash before `png`).

---

## 1. Session Start Checklist

Every new ANSIClaw session, in order:

1. `GET http://127.0.0.1:7777/api/canvas/info` — confirm Clawbius is running
   - If not running it can be started from the clawbius folder with: `launch_clawbius.sh`
2. `GET http://127.0.0.1:7777/api/openapi.json` — check for API changes
3. **Study reference files** (see Section 4 below) — mandatory before drawing
4. Read `references/api.md` for full endpoint details
5. Check that ice colors are set to OFF unless Operator says otherwise (see Section 2 below)
6. Only draw ONE iteration of the image, but analyze your result and ask the operator if you can improve it and tell them how you will improve it before drawing again. ANSI art is an iterative process — you should be learning and improving with each iteration.
7. Only draw iterations when authorized, a maximum of 5 at a time. Ensure you keep copies of each iteration .PNG and .ANS named apprproately; _v1, _v2 etc using a strategy like _v1a to resolve conflicts

**Output dir:** the 'outputs' folder in your skill folder — save ANS + PNG here - create the folder if it is not there

---

## 2. Color Rules

### ⚠️ ICE COLORS — DEFAULT IS OFF. 

**Ice colors are OFF by default. Do not use colors 8–15 as background colors.**

**If operator specifics that this is an 'ice colors ansi' you may turn ice colors control ON and use 8-15 as background colors.**

- Colors 0–7 are always safe as background
- Colors 0–15 are always safe as foreground

Turning ice colors ON:
- Call `POST /api/ui/ice-colors {"value": true}`
- Also pass `"ice_colors": true` in your `POST /api/file/new` call
- Now bg colors 8–15 are available for BACKGROUND use and open up new color mixing possibilities.

### 16-Color Palette

```
DARK (safe as foreground and background):
  0=black       1=dark blue   2=dark green  3=dark cyan
  4=dark red    5=magenta     6=brown       7=light gray

BRIGHT (foreground ONLY unless ice colors ON):
  8=dark gray   9=blue        10=green      11=cyan
  12=red        13=light mag  14=yellow     15=white
```

## 3. Block types

### Shade Blocks (F1–F4)

```
F1=176 ░  light shade    F2=177 ▒  medium shade
F3=178 ▓  dark shade     F4=219 █  full block
```

Dithering is achieved by varying the shade block (F1–F4) with different foreground/background color pairs. This is the primary tool for gradients, texture, and depth in ANSI art. Avoid large areas of solid color blocks without shade variation, unless a 'toon' style is called for in which case favor a bright/dark cell shaded approach with minimal dithering.

### Half-Blocks useful for edges and, smoother curves and anti-aliasing techniques

```
220=▄ lower half   223=▀ upper half
221=▌ left half    222=▐ right half
```

---

## 4. Studying Reference Files (MANDATORY)

Before drawing anything, study the reference files in `resources/`. Inspect the whole folder, not just the readme. Do these things: 

- Load the file if it is .ANS or .ASC and analyze it in clawbius - determine form and structure using your API and file analysis skills. focus on how blocks are used to generate aesthetic effects, how colors are combined, and how transitions are handled.
- analyze any PNG or image file for the same qualities - these are also ANSI art but rendered as images, so you can see the intended final output without the limitations of the ANSI format. Look for how colors are distributed, where half-blocks are used, and how shading is achieved.

Study the reference files with the mindset of a detective — look for patterns, techniques, and stylistic choices that you can learn from and apply in your own work. This is a critical step that should not be skipped.

### Step 1 — Read the README
```
resources/README.md
```
Get the description of each file and what it demonstrates. Also check the folder for any files not described in the readme.

### Step 2 — Open and analyze canvas data via API
```python
import requests, json
# Open the reference file
requests.post("http://127.0.0.1:7777/api/file/open",
    json={"path": "/absolute/path/to/resources/file.ans"})

# Get canvas info
info = requests.get("http://127.0.0.1:7777/api/canvas/info").json()

# Get full canvas data and analyze color/code usage
data = requests.get("http://127.0.0.1:7777/api/canvas/data").json()
blocks = data["result"]
cols = info["result"]["columns"]

# Study a region (e.g. rows 10-20):
for y in range(10, 20):
    unique = {}
    for x in range(0, cols):
        b = blocks[y * cols + x]
        key = (b["code"], b["fg"], b["bg"])
        unique[key] = unique.get(key, 0) + 1
    top = sorted(unique.items(), key=lambda x: -x[1])[:6]
    print(f"row {y}: {top}")
```

Look for:
- What foreground/background color pairs dominate each region?
- Which shade blocks (F1–F4), and half-blocks are used and where?
- How are transitions handled between regions?
- What background colors are used — are they all 0–7?

### Step 3 — Analyze the reference PNG
Each reference file in `resources/` should have a matching `.png` alongside the `.ans` file. Use the `image` tool to analyze the PNG directly:
```
image(image="<absolute_path_to_resources/file.png>", prompt="...")
```
Study:
- Color regions and how they transition
- Where black separators appear between colored areas
- Half-block usage on edges and curves
- Overall composition and density

---

## 4. Core Style Rules

### No-Tocar (Colored Areas Must Not Touch)

**This is an important stylistic rule of some ANSI art.**

Different objects can look more appealing when not touching each other directly. They can be separated by black (fg or bg=0) half-blocks or full blocks. This gives the art a clean, distinct look.

**Wrong:** Red block directly adjacent to yellow block
**Right:** Red block → black half-block separator → yellow block

Use `▌(221)`, `▐(222)`, `▀(223)`, `▄(220)` with `fg=color, bg=BLACK` to create clean color boundaries.

Example — transitioning from red to yellow area:
```
[RED F4][▐ fg=RED bg=BLACK][▌ fg=YELLOW bg=BLACK][YELLOW F4]
```

### Shading & Depth

- Use F1–F4 shade blocks to build gradients — never just solid color fills for large areas
- Light source: decide where the light is coming from and be consistent
- Lit faces: use lighter shade blocks (F1/F2) or higher-contrast fg color
- Shadow faces: use F3/F4 or black fg
- Edges catch light: use `UH(223)` or `LH(220)` with bright fg on dark bg for edge highlights

### Typical Shading Patterns

```
Sky gradient (top to bottom, dark to light):
  F4 fg=DBLUE bg=BLACK → F3 fg=BLUE bg=BLACK → F2 fg=BLUE bg=BLACK → F1 fg=CYAN bg=BLACK

Ground (dark):
  F4 fg=BLACK bg=BLACK → F3 fg=BROWN bg=BLACK → F2 fg=BROWN bg=BLACK

Metal object (gray, lit from top-left):
  top edge:  UH fg=LGRAY bg=DGRAY  ← highlight
  upper:     F2 fg=LGRAY bg=DGRAY
  mid:       F3 fg=DGRAY bg=BLACK
  lower:     F4 fg=BLACK bg=BLACK  ← deep shadow

Fire/explosion background:
  F3 fg=RED bg=BLACK → F2 fg=BROWN bg=BLACK → F1 fg=YELLOW bg=BLACK
  Vary randomly across rows/columns — avoid horizontal banding

General style tip: Once the gradient is established, add complexity - patterns can be mixed, stair stepped to create visual complexity
```

### Half-Block Edge Technique

At the boundary between a filled area and black space, use half-blocks to smooth the edge and add depth:
- `UH(223) fg=color bg=BLACK` — object color on top, black below (bottom edge of object)
- `LH(220) fg=color bg=BLACK` — black on top, object color below (top edge of object)
- These also double as separators (no-tocar) between two color regions
- Also use half blocks for round, circular edges and diagonal lines and organic shapes like hair or the curvature of an object

---

## 5. Drawing Approach

Write Python scripts using `requests`. Never curl individual cells — always batch with scripts.

**Script template:**
```python
import requests, os
BASE = "http://127.0.0.1:7777"

def post(path, data):
    r = requests.post(f"{BASE}{path}", json=data)
    resp = r.json()
    if not resp.get("ok"): print(f"WARN {path}: {resp}")
    return resp

def rect(x, y, w, h, code=219, fg=7, bg=0):
    if w > 0 and h > 0:
        post("/api/draw/rect/filled", {"x":x,"y":y,"width":w,"height":h,"code":code,"fg":fg,"bg":bg})

def at(x, y, code=219, fg=7, bg=0):
    post("/api/draw/at", {"x":x,"y":y,"code":code,"fg":fg,"bg":bg})

def line(x1, y1, x2, y2, code=219, fg=7, bg=0):
    post("/api/draw/line", {"x1":x1,"y1":y1,"x2":x2,"y2":y2,"code":code,"fg":fg,"bg":bg})

# Canvas setup — ice_colors=False unless Operator says otherwise
post("/api/file/new", {
    "columns": 80, "rows": 25,
    "title": "Title", "author": "Clawd", "group": "ANSIClaw",
    "ice_colors": False
})
```

Save scripts to skill folder `scripts/`
Save output to skill folder `output/` — always export both ANS and PNG.

---

## 6. Input Files (Image-to-ANSI Renditions)

Operator may drop a source image into `inputs/` and ask for an ANSI rendition of it. **Do not check this folder unless explicitly asked.**

When asked to render an input file:

1. Read the image with the `image` tool — study shapes, dominant colors, light source, and composition
2. Map the image's colors to the 16-color ANSI palette (find the closest match for each major region)
3. Plan the canvas layout — decide which regions become which shade/color blocks
4. Simplify aggressively — ANSI art is abstraction, not photorealism. Pick 3-5 dominant colors max
5. Sketch the composition in comments before coding: major regions, where half-blocks go, light direction
6. Draw it — apply all the usual style rules (no-tocars, shade gradients, half-block edges)
7. Save output to the usual place

---

## 7. Full API Reference

See `references/api.md` — full endpoint details, parameter lists, CP437 extended codes.

---

## 8. Lessons Learned (from real sessions)

### Sky / Background Gradients
- **Don't use random noise for texture** — even at 15-18% density it creates "rain" or "static" artifacts that look terrible.
- **Don't use per-column checkerboard dithering on every row** — ANSI cells are tall and narrow, so alternating x%2 columns creates visible vertical stripes, not smooth blending.
- **Do use clean solid bands** — banding is natural and expected in ANSI art sky gradients. 4-5 rows per band (F4→F3→F2→F1, DBLUE on BLACK) reads cleanly.
- If you want a subtle transition between bands, a single dither row between solid blocks is the maximum — and even that can stripe visually, so test it.

### Petals / Organic Shapes
- Start wider than you think you need. Horizontal spread reads better at ANSI cell aspect ratio than height.
- Use the full shade gradient within each petal (F1 at tip → F4 at base where it meets the center) to imply curvature.
- Each petal's outermost edge should be `RFH`/`LFH` (half-block) with bg=BLACK to keep the no-tocars boundary clean.
- Diagonal petals need extra width (4+ cols) to be visible — don't short-change them.

### Centers / Small Color Areas
- A 2x2 center block can convey light/shadow convincingly:
  - top-left: F1 bright-color on dark-bg (lit)
  - top-right: F2
  - bottom-left: F3
  - bottom-right: F4 (deepest shadow)
- bg=BROWN (6) is always safe (it's <8), good for warm center tones.

### API Gotchas
- Export PNG endpoint is `/api/file/export/png` (not `/api/file/export-png`).
- Always check `openapi.json` at session start — endpoints may have changed.
- `post()` should print warnings but not crash on bad responses — wrap defensively.
