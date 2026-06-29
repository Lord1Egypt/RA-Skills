# Validation Checklist (merged from fireworks-tech-graph, gm-data-chart, archviz-skills)

## Pre-Generation (MANDATORY)
- [ ] Full Diagram Brief + 4-layer analysis (Identity/System/Components/Layout) with confidence (✅/⚠️/❓).
- [ ] Dials set (Complexity/Density/Restraint) and documented.
- [ ] Type + Output Mode chosen (Mermaid primary; ASCII for Gantt/terminal; no default).
- [ ] Tokens locked: semantic names, hex values, one accent max, contrast rule checked.
- [ ] Labels short (≤6 words English / ≤8 Chinese chars), consistent language.
  - For Gantt/sequence/any source MD: strip <br/>, avoid long descriptive inside nodes/bars/participants (use codes or " / " separators).
- [ ] For Gantt: explicit time data, categories, milestones.
  - **Hard**: inside gantt block only ultra-short codes (V1.1 etc.); full names in immediate table below; ASCII fallback included.
- [ ] For Sankey: weighted flows, semantic edge labels.
- [ ] "Why" and design intervention visible.
- [ ] Matches existing document style/palette.
- [ ] If recurring concept: plan variation per DESIGN.md.
- [ ] Editorial: Family A/B/C/D chosen; G3 ask gate passed if ambiguous.
- [ ] Editorial: judgment + promise + one evidence (Family A); serif ≤500; no `#ffffff` canvas.

## Post-Generation
### Mermaid
- [ ] Renders cleanly in target (Obsidian, GitHub, Mermaid live editor).
- [ ] No syntax errors.

### ASCII
- [ ] Columns aligned in mono font.
- [ ] No wrapping in 80 columns.
- [ ] Legend clear.

### SVG / Hybrid (if rendered via pretty-mermaid or external)
- [ ] Syntax valid (rsvg-convert or equivalent passes).
- [ ] No arrow-node collisions, text overflows, or overlaps.
- [ ] Arrow labels have background rects (opacity 0.95).
- [ ] Legend present if >2 arrow types.
- [ ] Visual self-review (if images readable): clean routing, sufficient spacing, readable text (>=11px, good contrast).
- [ ] Matches DESIGN.md tokens + user's document style.

## Error Recovery
- Syntax fail: Simplify or switch type/mode.
- Visual issues: Widen gutters, add jump-over arcs (for SVG), background rects, or use ASCII.
- Generic look: Re-run brief; enforce variation.
- Always document confidence and cite exact values.

## Quality (from anydesign/gm)
- Cite hex/px/specifics.
- Infer semantic roles.
- Never invent tokens or assume palette.
- Self-contained for papers (caption first = finding).

Run this before shipping any diagram.