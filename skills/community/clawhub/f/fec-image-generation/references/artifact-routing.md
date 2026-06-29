# Artifact Routing

## Mode selection

Choose the execution mode before writing a prompt:

| Mode | Use when | Behavior |
| ---- | -------- | -------- |
| Deterministic source | Text, labels, charts, connectors, or exact geometry must be correct | Build Mermaid, SVG, HTML/CSS, canvas, plotting, or design-tool source first, then export PNG. |
| Host-native image tool | The task needs raster aesthetics, illustration, product mood, photo-like output, or image editing and the current environment has an image tool | Write a structured prompt and call the host image tool. Save or report the prompt when future edits are likely. |
| Prompt-only advisor | No image tool is available or the user only wants a prompt | Produce the final prompt, usage notes, and verification checklist. Do not imply an image was generated. |
| Hybrid | Exact text or UI structure plus generated imagery are both needed | Generate supporting imagery, then compose final text/layout in SVG, HTML, canvas, or a design tool. |

Do not introduce local image API scripts, provider-specific environment variables, or OpenAI-compatible gateway assumptions as part of this workflow. If a project already owns such a pipeline, treat it as a host tool and keep prompts provider-neutral.

## Route by output

| Output | Preferred route | Notes |
| ------ | --------------- | ----- |
| Poster / ad creative | Image generation, then optional layout polish in HTML/SVG or design tool | Lock exact copy before generation; recompose text outside the bitmap when accuracy matters. |
| UI mockup | HTML/CSS or design-tool mockup first; raster generation only for mood or hero references | Keep controls readable and avoid fake product states in final handoff. |
| Product image | Image generation or edit with reference constraints | Preserve brand, perspective, material, and lighting; do not overwrite original assets. |
| Infographic | Structured SVG/HTML/canvas for text and charts; generated illustrations only as supporting media | Export PNG after layout QA. |
| Academic figure | Deterministic plotting, SVG, Mermaid, LaTeX, or canvas | Accuracy beats style; keep source reproducible. |
| Comic / storyboard | Image generation with panel manifest | Track panel count, exact captions, characters, scene continuity, and reading order. |
| Avatar | Image generation or edit | Ask only when identity, style, or usage rights are ambiguous. |
| Brand board | Mixed route: generated imagery, palette/type/layout board in HTML/SVG | Record palette roles, typography mood, imagery rules, and avoid-list. |
| Image edit | Edit target plus explicit invariants | Preserve requested identity, composition, text, object, lighting, or background constraints. |

## Visual asset categories

Use these categories to pick prompt detail and verification focus:

- Product and commerce: product image, packaging, lifestyle scene, marketplace board.
- UI and interface: app mockup, chat scene, dashboard view, landing hero, social post.
- Technical and academic: architecture, sequence, state, ER, method figure, graphical abstract.
- Narrative and brand: poster, campaign key visual, storyboard, comic, avatar, mascot, brand board.
- Information design: infographic, map, comparison, step-by-step guide, KPI board.
- Editing: background replacement, object removal, local replacement, retouching, portrait edit.

If the category is text-heavy or diagram-heavy, prefer a deterministic source or hybrid route.

## Prompt contract

Use this compact structure when calling an image tool:

```text
Asset type:
Use:
Canvas / aspect ratio:
Audience:
Required text:
Subject:
Composition:
Style / brand tone:
Reference assets:
Must preserve:
Avoid:
Output:
```

For exact text, prefer adding text in SVG/HTML/design source after image generation. If text must be inside generated imagery, keep it short and verify manually.

For image edits, add:

```text
Source image:
Edit region:
Invariants:
Replacement:
Lighting / perspective:
```

## Handoff checklist

- Final image path is inside the workspace when the asset is project-bound.
- Source or prompt is saved when future edits are likely.
- Exact text, diagram labels, chart values, citations, and brand marks are manually checked.
- Generated variants that were rejected are not referenced by code or docs.
- If no image was generated, the final answer clearly states prompt-only mode.
