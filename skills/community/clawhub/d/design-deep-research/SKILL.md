---
name: design-deep-research
version: "0.1.0"
license: Apache-2.0
description: "Graphic design deep research: automatically collects design references across domestic and international platforms (Behance, Dribbble, Pinterest, Zcool, Huaban), performs cluster analysis on aesthetic trends, and outputs visual HTML research reports with reusable exploratory prompts. Use when: researching design directions, analyzing visual trends, gathering inspiration moodboards, or exploring visual styles. Keywords: 设计调研, 灵感调研, 风格调研, 视觉参考, 情绪板, design research, aesthetic trends, moodboard."
metadata:
  openclaw:
    emoji: 🔍
---

# Design Deep Research — Visual Inspiration & Aesthetic Trend Analysis

> "Great design doesn't emerge in a vacuum; it stands on the shoulders of extensive visual references."

## Core Philosophy

This is an **autonomous research and trend analysis skill for graphic and visual designers**, not a direct layout generator.

Workflow breakdown:
- **Intake**: Understand the designer's intent, category, and target aesthetic.
- **Harvest**: Parallel web harvesting across global and regional design platforms.
- **Analyze**: Extract recurring visual patterns, color palettes, and typographic structures.
- **Cluster**: Group references into 3–5 distinct, actionable design directions.
- **Synthesize**: Emit an interactive, standalone HTML research report with moodboards and reusable prompt seeds.

> [!TIP]
> **System Collaboration Guidelines**:
> - This skill focuses on **upstream trend discovery, aesthetic clustering, and visual moodboards**.
> - If you need to convert an approved visual style into production-ready commercial prompts for e-commerce, product heroes, or marketing posters, hand off to `commercial-image-prompt`.

---

## Execution Workflow

### Phase 0: Requirements Scoping & Planning

#### Step 1: Intake Parameters
Receive user requirements:
- **Text Brief (Required)**:
  - Design category: Poster, Brand VI, Packaging, Editorial, UI, Illustration, etc.
  - Industry / Sector: Tech, FMCG, Luxury, Culture, Education, Fashion, etc.
  - Vibe & Mood Keywords: Minimalist, Cyberpunk, Neo-Chinese, Warm Organic, Bauhaus, etc.
  - Target Medium: Digital screen, Out-of-home (OOH) physical print, Packaging box, etc.
- **Reference Image URLs (Optional)**: 1–3 visual reference links.

#### Step 2: Brief Decomposition
| Dimension | Parsing Goal | Example |
|---|---|---|
| **Design Type** | Target artifact format | Packaging, Key Visual Poster, Brand VI |
| **Industry** | Sector visual tropes & conventions | Tech (Dark slate, crisp cyan), FMCG (Vibrant, high chroma) |
| **Aesthetic Keywords** | Searchable stylistic tags | Neo-Chinese, Kinetic Typography, Glassmorphism |
| **Medium / Aspect** | Compositional bias | 9:16 vertical, 16:9 widescreen, 1:1 square |

*If reference images are provided*: Extract dominant color schemes, lighting, typography, and texture as an initial "style anchor" for search queries.

#### Step 3: Create Research Workspace Directory
Create the research workspace:
```
design-research/[brief-slug]/
├── report.html                      # Final HTML report (Phase 3)
└── references/
    ├── 01-international-inspiration.md  # Behance + Dribbble + Pinterest
    ├── 02-mockup.md                     # Mockup World + Graphic Burger + Yellow Images
    ├── 03-asset-libraries.md            # Freepik + Vecteezy
    ├── 04-image-galleries.md            # Unsplash + Pexels
    ├── 05-regional-platforms.md         # Zcool (站酷) + Huaban (花瓣) + Gutianlu9 (古田路9号)
    └── sources/                         # Verified reference links
```

---

### Phase 1: Parallel Multi-Platform Reference Mining (Agent Swarm)

Deploy parallel sub-agents across specialized platform tiers:

| Agent | Target Platforms | Focus Area | Output Artifact |
|---|---|---|---|
| **1: Global Inspiration** | Behance + Dribbble + Pinterest + Savee | Full brand cases, VI systems, avant-garde typography | `01-international-inspiration.md` |
| **2: Mockups & 3D** | Mockup World + Graphic Burger + Yellow Images | Realistic material rendering, packaging physical mockups | `02-mockup.md` |
| **3: Vector & Assets** | Freepik + Vecteezy | Vectors, ornamental patterns, geometric badges | `03-asset-libraries.md` |
| **4: Photography** | Unsplash + Pexels | Editorial photography, cinematic light, authentic human mood | `04-image-galleries.md` |
| **5: Regional & Asian** | 站酷 (Zcool) + 花瓣 (Huaban) + 古田路9号 | Regional trends, China-chic, Asian commercial packaging | `05-regional-platforms.md` |

#### Strict Reference Standards:
1. **Zero Hallucination of URLs**: Every recorded image URL and project source link must be an authentic, accessible URL. Never fabricate placeholder links.
2. **Failure Handling**: If a platform returns no relevant results, explicitly record `No matching assets found on [Platform]` with attempted keywords and reasons. Never pad with irrelevant fake data.

---

### Phase 1.5: Harvest Review Checkpoint
Summarize harvested references for user confirmation:
- Total references gathered (Target: ≥30 real references across ≥5 platforms).
- Identified preliminary aesthetic clusters.
- Prompt user for approval before running deep aesthetic analysis.

---

### Phase 2: Visual Synthesis & Aesthetic Clustering

#### 2.1 Aesthetic Feature Extraction (7 Dimensions)
Evaluate harvested reference pools across 7 core visual dimensions (see `references/analysis-framework.md`):
1. **Color Palette**: Dominant hues, secondary structural colors, accent saturation, emotional temperature.
2. **Typography**: Typeface classification (Serif, Sans, Display, Geometric Mono), hierarchy, tracking/kerning density.
3. **Graphic Language**: Vector geometry, textural grain, 3D elements, iconographic style.
4. **Lighting & Texture**: Specular highlights, matte finishes, film grain, paper embossing, glassmorphism.
5. **Composition & Grid**: Golden ratio, asymmetric balance, negative space breathing room, visual gravity.
6. **Emotional Tone**: Mood keywords, psychological associations.
7. **Signature Techniques**: 3–5 concrete design techniques that define the aesthetic.

#### 2.2 Prompt Derivation (Exploratory Prompt Seeds)
For each clustered design direction, derive an exploratory image prompt:

```
[Subject/Hero], [Style/Movement], [Color Palette], [Lighting/Texture], [Composition/Viewpoint], [Mood/Atmosphere], --ar [W:H] --style raw
```

> [!TIP]
> Prompts generated here are intended for **aesthetic exploration and moodboard generation**. For strict commercial e-commerce assets (white background cutouts, marketing banners with text-safe zones), hand off to `commercial-image-prompt`.

---

### Phase 3: Interactive HTML Report Generation

Generate a self-contained, responsive HTML report using `references/report-template.html`:
- **Executive Summary**: Total references, platform coverage, core design challenge.
- **Direction Cards**:
  - Distinct style name & one-line aesthetic thesis.
  - Visual feature breakdown grid (Color, Type, Graphics, Lighting, Composition).
  - Curated gallery of verified reference images with working source links.
  - Reusable prompt seed with bracketed parameter placeholders `[like this]`.
- **Cross-Direction Trade-Off Matrix**: Comparison table highlighting contrast between directions.

Write output to `design-research/[brief-slug]/report.html`.

---

### Phase 4: Quality Gate

| Verification Item | Pass Criteria | Rejection Trigger |
|---|---|---|
| **Direction Count** | 3–5 distinct aesthetic directions | Fewer than 3 or more than 6 |
| **Differentiation** | Directions differ across ≥2 visual dimensions | Surface-level variants (e.g. just light vs dark) |
| **Reference Fidelity** | ≥3 real, accessible case studies per direction | Broken image links or fabricated URLs |
| **Actionability** | Concrete techniques provided for designers | Vague, generic commentary without rules |
