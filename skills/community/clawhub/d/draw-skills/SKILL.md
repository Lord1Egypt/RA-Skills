---
name: draw-skills
description: >
  Academic figure generation assistant. Generates detailed natural-language prompts for nanobanana
  (and other drawing tools) to produce publication-quality figures for research papers.
  Supports biology/medicine (BioRender style), CS/engineering (architecture diagrams),
  AI/Agent systems, computer vision, and more. Can analyze a paper to proactively suggest
  missing figures, generate prompts on demand, improve existing figures, or adapt a reference
  figure's visual style to new content.
  Trigger keywords: draw figure, generate figure, draw diagram, paper figure, 画图, 绘图,
  论文配图, 生成图, 绘制示意图, 流程图, 架构图, BioRender, 机制图, nanobanana prompt,
  figure prompt, 参考图风格, 图表建议, 补图
metadata:
  version: "1.0"
  last_updated: "2026-04-09"
  status: active
  related_skills:
    - academic-paper
    - deep-research
    - anthropic-skills:pdf
---

# draw-skills — Academic Figure Prompt Generator

A skill for generating high-quality drawing instructions for research paper figures.
You analyze the paper's content and domain, recommend what figures to draw (or work from user instructions),
then produce detailed natural-language prompts ready for **nanobanana** or other AI drawing tools.

> See full execution instructions: `PROMPT.md`

---

## Quick Start

```
# Analyze a paper and get figure suggestions:
/draw-skills [paste paper text or upload PDF]

# Generate a figure prompt directly:
/draw-skills generate: a multi-agent LLM pipeline diagram with three agents

# Improve an existing figure:
/draw-skills improve: [upload image]

# Use a reference figure's style:
/draw-skills ref-style: [upload reference image] + [describe what you want to draw]
```

---

## Trigger Conditions

### Trigger Keywords

**English**: draw figure, generate figure, draw diagram, paper figure, figure prompt, BioRender style,
mechanism diagram, architecture diagram, nanobanana prompt, visualize paper, figure for paper,
illustration prompt, scientific diagram, improve figure, style reference for figure

**中文**: 画图, 绘图, 论文配图, 生成图, 绘制示意图, 流程图, 架构图, 机制图, 帮我画,
参考图风格, 图表建议, 补图, 配图指令, nanobanana, 用这个风格画

---

## Operational Modes

| Mode | Trigger Phrase | Description |
|------|---------------|-------------|
| `analyze` (default) | Upload PDF / paste paper text | Analyze paper → suggest figures → user picks → generate prompts |
| `generate` | "generate: [description]" | Skip analysis, generate prompt directly from description |
| `improve` | "improve: [image]" | Analyze an existing figure's weaknesses → generate improved version prompt |
| `ref-style` | "ref-style: [image] + [description]" | Extract visual style from reference image → apply to new content |

---

## Orchestration Workflow

```
Phase 0 ── Input Collection
           Identify mode from input type and trigger phrase.
           Accept: PDF file / text / image / description / mix.
              │
Phase 1 ── Content Analysis            [analyze / improve modes]
           • Extract domain, core method, key results
           • Detect field: Bio/Med | CS/Eng | AI/Agent | CV | General
           • Identify existing figures and conceptual gaps
              │
Phase 2 ── Figure Planning             [Checkpoint ✓ user confirms]
           • List recommended figures (index + title + purpose)
           • Tag each with: recommended tool + figure type + priority
           • User selects which figures to generate
              │
Phase 3 ── Style Confirmation          [Checkpoint ✓ user confirms]
           • Auto-infer style from detected domain
           • If ref-style mode: extract palette/layout/visual-language from reference image
           • Present style recommendation + color scheme summary
           • User confirms or overrides
              │
Phase 4 ── Prompt Generation
           • One structured prompt block per figure
           • Language: English (nanobanana input language)
           • Includes: scene, style keywords, colors, key elements, layout, labeling style
           • If ref-style: append "styled after: [extracted features]" section
```

---

## Domain → Style Mapping

| Domain | Auto-Detection Keywords | Recommended Style |
|--------|------------------------|-------------------|
| Biology / Medicine / Biochemistry | pathway, signaling, receptor, cell, protein, mechanism, drug, inflammation, apoptosis | BioRender-style: white background, 3D bio-forms, vivid palette, anatomical precision, clear labels |
| CS / Systems Engineering | architecture, system, pipeline, framework, module, distributed, network, protocol | Technical architecture: flat design, rectangular modules, directional arrows, minimal color |
| AI / Agent / NLP | agent, LLM, transformer, attention, multi-agent, reasoning, prompt, chain-of-thought | AI system diagram: rounded modules, node-edge graph, gradient accents, hierarchical layout |
| Computer Vision | detection, segmentation, CNN, feature map, backbone, encoder, decoder, attention map | CV network diagram: stacked 3D blocks, feature maps, consistent color temperature, perspective layers |
| General / Experimental | results, comparison, ablation, statistical, flowchart, overview | Scientific illustration: clean white background, Nature/Science color convention |

---

## Figure Type Taxonomy

| Type | Description | Typical Domain |
|------|-------------|---------------|
| Mechanism diagram | Step-by-step biological/chemical process | Biology, Medicine |
| System architecture | Components and their connections | CS, Engineering |
| Agent pipeline | Multi-agent workflow with roles and messages | AI, NLP |
| Network architecture | Layer-by-layer ML model structure | CV, ML |
| Conceptual overview | High-level summary of the paper's contribution | All |
| Comparison / Ablation | Side-by-side method comparison | All |
| Data flow diagram | How data moves through a system | CS, Engineering |
| Experimental setup | Visual description of experiment design | All |

---

## Output Format (per figure)

```
## Figure [N]: [Title]
**Status**: [NEW — not in paper] | [EXISTING — redraw/improve] | [EXISTING — good, skip if satisfied]
**Purpose**: [what this figure communicates]
**Recommended tool**: nanobanana
**Figure type**: [from taxonomy above]
**Style**: [style name]

**Prompt**:
[Full English natural-language prompt, 100–300 words, covering:
 - Overall scene and subject
 - Style keywords
 - Color scheme
 - Key elements to include (exhaustive list)
 - Spatial layout and composition
 - Labeling / annotation style]

**Style reference** *(ref-style mode only)*:
[Extracted visual features: e.g., "warm navy + coral palette, left-to-right horizontal flow,
flat vector icons, moderate label density, soft drop shadows"]

**Caption (EN)**: [Publication-ready English figure caption. Format: "Fig. N. [One sentence
describing what is shown]. [One or two sentences explaining the key takeaway or how to read
the figure]. [Optional: abbreviation definitions if needed.]"]

**Caption (ZH)**: [对应的中文图注。格式：图N. [一句话说明图的内容]。[一两句说明读图方式或关键
结论]。[如有需要列出缩写含义。]]

**nanobanana tips**: [iteration suggestions, aspect ratio, what to emphasize on retry]
```

---

## Iron Rules

⚠️ **NEVER copy reference image content** — In ref-style mode, extract visual style only (palette,
layout pattern, visual language weight, atmosphere). Never reproduce specific icons, text,
exact arrow paths, or element proportions from the reference.

⚠️ **Always write prompts in English** — nanobanana is optimized for English input.
Include Chinese annotations separately as comments for the user's reference.

⚠️ **Domain-appropriate style only** — Do not apply BioRender style to an engineering diagram
or flat-icon style to a biological mechanism. When domain is ambiguous, ask before assuming.

⚠️ **Prompts must be specific, not generic** — Every prompt must name the actual biological
molecules / system components / model layers involved. A prompt that could apply to any paper
in the field is a failed prompt.

⚠️ **Two checkpoints, no skipping** — Always pause at Phase 2 (figure list) and Phase 3
(style confirmation) for user confirmation before generating prompts.

⚠️ **Always include the framework/overview figure** — Even if the paper already contains an
overview figure, always include it in the figure list marked as `EXISTING — redraw/improve`.
Never silently skip it. The existing version may be low-quality, incomplete, or inconsistent
with other figures. Let the user decide whether to regenerate it.

⚠️ **Always output captions** — Every figure prompt block must include both English and Chinese
captions ready to paste into the paper. Captions must describe content AND convey the key
insight, not just label what is drawn.

---

## Integration

- Works alongside **academic-paper** skill: after writing a paper, use draw-skills to fill in figures
- Works alongside **anthropic-skills:pdf**: PDF reading is handled natively; draw-skills interprets the content
- Output prompts can also be used with Gemini, DALL-E, or Stable Diffusion with minor adjustments

---

## Version Info

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Last updated | 2026-04-09 |
| Target tool | nanobanana (natural language input) |
| Secondary tools | Gemini image gen, DALL-E 3 |
| Maintainer | User |
