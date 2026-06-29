# Brandmark Studio

A brand identity skill for OpenClaw that generates production-ready SVG logos, icons, brandmarks, and visual identity systems through a structured, professional design workflow.

---

## What It Does

Brandmark Studio treats logo and icon creation as a real design process: discovery, strategy, concept generation, asset creation, simplification, and quality review. It doesn't just produce a generic SVG — it generates a rationale, explores multiple concepts, and iterates on quality.

### Supported Outputs

| Asset Type | Description |
|-----------|-------------|
| `logo` | Full brandmark with wordmark and symbol |
| `icon` | Standalone symbol or pictogram |
| `logo_and_icon` | Both lockup and standalone icon |
| `icon_pack` | Coordinated set of related icons |
| `favicon` | 16×16 and multi-resolution favicon variants |
| `app_icon` | Platform-ready app icon (iOS, Android, web) |
| `avatar` | Profile picture / social media mark |
| `badge` | Circular or shield emblem |
| `emblem` | Decorative heraldic or institutional mark |
| `monogram` | Interwoven letterform mark |

---

## The 6-Step Workflow

1. **Discovery** — Collect or infer brand name, industry, audience, and desired style from the user's request. If details are missing, the skill infers reasonable defaults rather than forcing a questionnaire.

2. **Strategy** — Build an internal design brief: brand goals, emotional goals, positioning, visual metaphors, style direction, and archetype alignment. Selects 2–4 design principles with justification.

3. **Concept Generation** — Produces **three significantly different concepts** (not cosmetic variations). Each concept includes symbolism, composition, strengths, risks, and recommended use cases.

4. **Asset Creation** — Generates production-ready SVGs for the chosen concept. Delivers only what the asset type requires: master, horizontal, stacked, icon, favicon, monochrome, reverse, etc.

5. **Icon Simplification Engine** — Automatically derives favicon, avatar, and app icon versions from any logo or brandmark. Each simplified version must remain recognizable at 16×16.

6. **Quality Review** — Scores the final mark across seven dimensions (1–10). Overall score below 8.0 triggers a specific refinement recommendation.

---

## Design Engine

### 9 Style Families

Styles can be blended for nuanced direction:

- **Modern** — Clean, geometric, minimal
- **Classic** — Timeless, serif, heritage
- **Luxury** — Premium, refined, exclusive
- **Creative** — Playful, expressive, unexpected
- **Entertainment** — Bold, dynamic, spectacle
- **Dark** — Gothic, occult, horror, noir
- **Future** — Sci-fi, tech, synthetic
- **Nature** — Organic, flowing, earthy
- **Cultural** — Ethnic, traditional, symbolic

### 12 Archetypes

Archetypes influence symbolism, shape language, and composition:

Hero, Outlaw, Sage, Innocent, Explorer, Ruler, Creator, Caregiver, Lover, Jester, Magician, Everyman

---

## Quality Standards

- **SVG 1.1** output with transparent background
- `viewBox` required, no fixed dimensions
- Scalable from **16×16** through **512×512**
- Favicon versions must survive at true 16×16

### What It Avoids

- Clipart aesthetics
- Photorealism
- Excessive path counts or gradients
- Decorative complexity
- Details that collapse at favicon size

### What It Prioritizes

- Scalability, memorability, simplicity
- Strong silhouettes
- Effective negative space
- Brand relevance

---

## Directory Structure

```
brandmark-studio/
├── SKILL.md                          # Main workflow and trigger rules
└── references/
    ├── archetypes.md                 # 12 archetypes and their visual influence
    ├── asset-types.md                # Deliverable specifications per asset type
    ├── concept-generation.md         # Concept divergence rules
    ├── design-principles.md          # Design principle library
    ├── icon-packs.md                 # Extended icon category reference
    ├── icon-simplification.md        # Favicon/avatar simplification rules
    ├── quality-review.md             # 7-dimension scoring rubric
    ├── styles.md                     # 9 style families with blend logic
    └── svg-rules.md                  # SVG technical standards
```

---

## Usage

Install the skill into your OpenClaw workspace and trigger it naturally:

- "Make me a logo for a horror podcast"
- "Design an app icon for a weather app"
- "Create a monogram for a law firm"
- "Build an icon pack for a cooking app"

The skill handles the rest — discovery, strategy, concepts, and production assets.

---

## Notes

- The skill is optimized for **OpenClaw** and uses its skill loading system (`references/` files load on demand).
- All output is **SVG** — no raster generation is included in the workflow.
- **Revision support**: After the initial design is delivered, iterate by telling the agent what to change (stroke weight, color, archetype shift, etc.). No formal revision workflow is needed.

---

*Skill version: 1.0.0*
