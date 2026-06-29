---
name: game-dev-art-bible
description: >
  Visual identity specification for games. Defines style guides, color
  palettes, reference boards, technical art constraints, and pipeline
  requirements. Ensures visual consistency across the project.
triggers:
  - "art style guide"
  - "create art bible"
  - "visual identity"
  - "game art direction"
  - "color palette"
  - "art pipeline"
  - "style guide"
---

# Game Dev Art Bible — Visual Identity Specification

## 🎯 Purpose

Define the visual identity of a game so all artists (and AI tools) produce
consistent, on-brand assets. Covers style references, color theory, material
specs, and technical constraints per engine.

## 🤖 Multi-Platform Notes

| Platform | Notes |
|----------|-------|
| **OpenClaw** | Best for writing structured documents. Can create separate files for each section and link them. |
| **Claude Code** | Can write markdown files. Share color codes, hex values, and rules. |
| **Cursor/Windsurf** | Good for editing alongside project assets. |
| **GitHub Copilot** | Chat can help define style rules. Good for fill-in templates. |
| **Generic LLM Chat** | Output sections as code blocks. User pastes into their project docs. |
| **Any AI** | All can generate color palettes, style descriptions, and reference lists. Image-capable AIs can analyze reference images. |

---

## 📂 Document Structure

Create in `game-dev-studio/art-bible/`:

```
art-bible/
├── index.md               ← Master document
├── 01-style-guide.md      ← Overall art direction
├── 02-color-palette.md    ← Color systems + hex codes
├── 03-characters.md       ← Character design rules
├── 04-environments.md     ← Environment/world art
├── 05-ui.md               ← UI art style
├── 06-technical.md        ← Technical constraints
├── 07-reference-board.md  ← Visual references
└── 08-pipeline.md         ← Asset pipeline + tools
```

---

## 🎨 Section 1: Art Direction

### Step 1.1 — Style Definition

Ask:
> **"What's the visual style?"**
>
> ```
> 1) Pixel art — retro, constrained resolution
> 2) Low-poly 3D — faceted, stylized, performs well
> 3) Hand-painted 3D — painterly textures on 3D models
> 4) Realistic 3D — PBR, photoreal, heavy
> 5) Cel-shaded / Toon — like anime or comic (e.g. Jet Set Radio, Borderlands)
> 6) Vector / Flat — clean lines, flat colors
> 7) Hand-drawn — 2D animation frames, sketchy
> 8) Mixed media — combine styles intentionally
> 9) Procedural / Generative — algorithm-driven visuals
> 10) Abstract — non-representational
> ```

### Step 1.2 — Artistic Influences

Ask:
> **"Name 3-5 artistic influences (games, art, movies, artists)."**

Link or describe each and note *what aspect* to take from each:

| Influence | What We're Taking |
|-----------|-------------------|
| Hollow Knight | Atmospheric lighting and silhouette readability |
| Cuphead | Animation quality and frame-by-frame feel |
| Ghibli films | Color grading and environmental storytelling |

### Step 1.3 — Mood Words

Ask:
> **"List 5-10 adjectives that describe the game's look."**

Examples: warm, gritty, whimsical, dark, saturated, desaturated, crisp,
fuzzy, neon, organic, geometric, painterly, minimal.

---

## 🎨 Section 2: Color Palette

### Step 2.1 — Palette Type

Ask:
> **"Palette strategy?"**
>
> ```
> 1) Limited palette — NES-style, 16-64 colors total
> 2) Moody palette — one dominant hue, limited range
> 3) Full color — no artificial limit
> 4) Procedural — generated or data-driven
> ```

### Step 2.2 — Define Palette

For each color:

```markdown
## [Color Name]

**Role:** [primary / secondary / accent / background / UI]
**Hex:** `#RRGGBB`
**RGB:** (R, G, B)
**HSL:** (H°, S%, L%)

**Usage:**
- [Where this color is used]
- [What it communicates]

**Avoid:**
- [Where NOT to use this color]
```

### Step 2.3 — Palette Rules

```markdown
## Palette Rules

### Primary Colors (70% of screen)
- [Color A] — backgrounds, large surfaces
- [Color B] — secondary surfaces, shadows

### Secondary Colors (25% of screen)
- [Color C] — characters, interactive elements
- [Color D] — environment details

### Accent Colors (5% of screen)
- [Color E] — UI highlights, important items
- [Color F] — warnings, danger indicators

### Readability Rules
- Text on background must have 4.5:1 contrast ratio (WCAG AA)
- Interactive elements must contrast with background
```

---

## 👤 Section 3: Character Design

```markdown
# Character Design Guidelines

## Silhouette Rules
- Each character must have a unique, readable silhouette
- Use the "silhouette test": fill character in black, it should still be identifiable

## Proportion Rules
- [E.g., "All characters are 4 heads tall, cartoon proportion"]
- [E.g., "Human characters use realistic 7.5 head proportion"]

## Material Palette
| Material | PBR Values | Visual Goal |
|----------|-----------|-------------|
| Skin | Roughness 0.5, Metal 0 | Soft, matte |
| Armor | Roughness 0.3, Metal 0.8 | Shiny, metallic |
| Cloth | Roughness 0.8, Metal 0 | Soft, matte, slightly fuzzy |

## Expression Range
- [How many expressions needed per character]
- [Style of expressions: subtle, exaggerated, etc.]

## Animation Style
- **Walk cycle:** [bouncy / realistic / minimal]
- **Idle:** [breathing only / fidgets / still]
- **Attack:** [telegraphed / snappy / heavy]
```

---

## 🌍 Section 4: Environment Art

```markdown
# Environment Art Guidelines

## Grid & Scale
- **Unit scale:** [1 unit = 1 meter / 1 unit = 0.5 meters]
- **Player height:** [X units]
- **Tile size:** [X units]
- **Module grid:** [X x Y for modular pieces]

## Lighting
- **Primary light:** [warm/cool, direction, intensity]
- **Ambient:** [color, intensity]
- **Shadow:** [hard/soft, resolution]
- **Fog:** [color, density, distance]

## Level Art Rules
- [Rule about visual clarity / readability]
- [Rule about contrast / leading the eye]
- [Rule about performance (draw calls, poly count)]

## Material Library
| Material | Texture Size | Tiling | PBR Values | Notes |
|----------|-------------|--------|-----------|-------|
| Stone Wall | 1024x1024 | 2x2 | R:0.8, M:0 | Keep neutral |
| Metal Floor | 2048x2048 | 1x1 | R:0.3, M:0.9 | Add scratches |
| Wood Planks | 512x512 | 4x2 | R:0.7, M:0 | Vary color |
```

---

## 🖥️ Section 5: UI Art

```markdown
# UI Art Direction

## UI Style
- [Minimalist / ornate / diegetic / flat / skeuomorphic]

## UI Color Palette
- **Primary UI:** `#RRGGBB` — buttons, panels
- **Interactive:** `#RRGGBB` — hover, clickable
- **Danger:** `#RRGGBB` — health low, warnings
- **Success:** `#RRGGBB` — achievements, positive
- **Disabled:** `#RRGGBB` — inactive elements

## Typography
- **Primary font:** [name], [weight range]
- **Secondary font:** [name], [weight range]
- **Fallback:** [system font]
- **Sizes:** H1: 32px, H2: 24px, Body: 16px, Caption: 12px

## Icon Style
- [Filled / outlined / glyph / illustrated]
- [Line thickness: Xpx]
- [Corner radius: Xpx]
```

---

## ⚙️ Section 6: Technical Constraints

### Step 6.1 — Engine Constraints

| Constraint | Godot | Unity | UE |
|-----------|-------|-------|-----|
| Max texture size | 4096x4096 (default) | 2048x2048 (mobile), 4096x4096 (desktop) | 8192x8192 |
| Max poly count per mesh | Varies by target | 50k-100k (desktop), 5-10k (mobile) | 100k+ (desktop), 10k (mobile) |
| Draw calls target | <500 (mobile), <2000 (desktop) | <100 (mobile), <500 (desktop) | <1000 (desktop) |
| Atlas packing | TileSet/TileMap | Sprite Atlas | Texture Atlas |

### Step 6.2 — Asset Naming Convention

```
[type]_[description]_[variant]_[size].[ext]

Examples:
char_player_run_01.png
env_wall_stone_01.png
ui_btn_primary_32.png
fx_explosion_01.png
```

### Step 6.3 — Export Settings

| Asset Type | Format | Compression | Mipmaps | Notes |
|-----------|--------|------------|---------|-------|
| Textures (opaque) | PNG (source), .tex (engine) | BC1/BC7 (DXT) | Yes | No alpha |
| Textures (transparent) | PNG (source) | BC3 (DXT5) | Yes | Premultiply alpha |
| Sprites | PNG | RGBA 8-bit | No | Power of 2 required |
| 3D Models | FBX/glTF | — | — | Apply scale, -Z forward |
| Audio | WAV (source), OGG (build) | Vorbis | — | 44.1kHz, 16-bit |

---

## 🖼️ Section 7: Reference Board

Create a reference board section with desciptions:

```markdown
# Reference Board

## Color References
- [Image description] — warm palette, earthy tones
- [Image description] — neon accents on dark backgrounds

## Lighting References
- [Game / scene description] — volumetric lighting examples
- [Game / scene description] — rim lighting on characters

## Mood References
- [Link / description] — overall atmosphere target
- [Link / description] — specific environment mood

## Technical References
- [Game / scene description] — similar visual quality target
- [Game / scene description] — benchmark for performance
```

---

## 🔧 Section 8: Asset Pipeline

```markdown
# Asset Pipeline

## Tools
- **Modeling:** [tool] [version]
- **Texturing:** [tool] [version]
- **Animation:** [tool] [version]
- **Audio:** [tool] [version]
- **VFX:** [tool]

## Import Process
1. Create asset in source tool
2. Export to [format] with [settings]
3. Import into engine with [import settings]
4. Verify in-engine appearance
5. Test performance (render budget, draw calls)

## Quality Check
- [ ] Meets poly budget
- [ ] Texture resolution correct
- [ ] PBR values within range
- [ ] No Z-fighting or clipping
- [ ] LODs generated (for 3D)
- [ ] Collision mesh set
- [ ] Named per convention
- [ ] Placed in correct folder
```

---

## 📄 Final Output

```markdown
# [Game Title] — Art Bible

**Version:** 1.0
**Date:** [YYYY-MM-DD]
**Art Director:** [Name]

## Style Summary
[One paragraph. Core visual identity.]

## Quick Reference
| Aspect | Value |
|--------|-------|
| Style | [pixel / low-poly / hand-painted / etc.] |
| Color Count | [limited / full / procedural] |
| Color Mood | [warm/cool, saturated/muted] |
| Texture Budget | [total MB] |
| Poly Budget | [triangles per frame] |
| Res Target | [1080p / 1440p / 4K / dynamic] |
| Framerate Target | [30 / 60 / 144 FPS] |

## Next Steps
- [ ] Finalize palette
- [ ] Create style test (single scene proving the art)
- [ ] Start `game-dev-studio/skills/architecture` for tech art pipeline
- [ ] Begin asset production
```
