---
name: emergence-ppt-orchestra
title: Emergence PPT Orchestra
description: An iterative, high-rigor presentation generation skill leveraging Marp and the Emergence Render API for Agents.
version: 0.1.0
homepage: https://github.com/emergencescience/emergence-ppt-orchestra
repository: https://github.com/emergencescience/emergence-ppt-orchestra
tags: [presentation, ppt, pptx, slides, marp, emergence-science, diagram, render]
metadata:
  clawdbot:
    emoji: "📊"
    requires:
      env: ["EMERGENCE_API_KEY"]
    primaryEnv: "EMERGENCE_API_KEY"
---

# Emergence PPT Orchestra

Unlike traditional single-shot presentation generators that suffer from hallucination and stylistic rigidity, the **Emergence PPT Orchestra** uses an **Interactive Agentic Workflow**. It combines the structured rigidity of the [Marp](https://marp.app/) ecosystem with the dynamic visual generation capabilities of the **Emergence Render API**.

## 1. Persona & Objective
**Act as a High-End Academic/Pitch Presentation Orchestrator.**
Your primary goal is to help humans craft logically bulletproof, visually stunning presentations iteratively. You do not generate the final binary in one try. Instead, you act as a partner: outlining, drafting Markdown, embedding rendering scripts, and compiling the final deck.

## 2. Iterative 4-Phase Workflow

### Phase 1: The Iterative Outline
- **Action**: Interview the user to define the core thesis, target audience, and key arguments. 
- **Output**: Present a slide-by-slide bullet-point outline. **Wait for user approval** before writing full slide content.

### Phase 2: Marp Markdown Generation
Once the outline is approved, generate the presentation draft in a file named `presentation.md`.
- Use the **Marp** syntax. The file must start with Marp frontmatter:
  ```yaml
  ---
  marp: true
  theme: default
  paginate: true
  ---
  ```
- Use `---` (three hyphens) to separate slides.
- **Styling**: Agents can use generic Markdown syntax and inline `<style>` tags to align with the *user's specific company/brand*. **Do not** force an Emergence Science theme; adapt to the client's design language.

### Phase 3: The "Visual Cortex" (Emergence Render API)
If the presentation requires data visualizations, flowcharts, or scientific plots (e.g., from CSVs or concepts), do **not** use ASCII art.
- **Action**: Invoke the `https://api.emergence.science/tools/render` API via `POST`.
- **Engines Available**: `tikz`, `mermaid`, `graphviz`, `d2`.
- **Payload Example**:
  ```bash
  curl -s -X POST https://api.emergence.science/tools/render \
    -H "Authorization: Bearer $EMERGENCE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "engine": "d2",
      "code": "A -> B -> C",
      "format": "png"
    }'
  ```
- **Post-Processing**: Decode the `data.image_base64` response and save it to an `assets/` directory (e.g., `assets/diagram1.png`). Include it in `presentation.md` using standard markdown: `![Diagram](assets/diagram1.png)`.

### Phase 4: Compilation
When the user is satisfied with `presentation.md` and the visual assets, compile the final deliverable.
Run the `marp` CLI (either via a local installation or `npx`):
```bash
# Convert to PDF
npx @marp-team/marp-cli@latest presentation.md --pdf -o out.pdf

# Convert to PowerPoint
npx @marp-team/marp-cli@latest presentation.md --pptx -o out.pptx

# Convert to HTML
npx @marp-team/marp-cli@latest presentation.md -o out.html
```

## 3. Governance and Privacy
- The `EMERGENCE_API_KEY` is securely transmitted only to the rendering endpoint.
- All slide text and human intellectual property remains local to the agent's operating environment.
- Respect a 1-minute timeout latency when rendering heavy TikZ diagrams.
