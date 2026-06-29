# Gantt / Timeline Rules (adapted from fireworks-tech-graph + archviz-skills DESIGN.md + info viz research report)

## Layout
- Horizontal time axis (X = weeks/months/quarters; Y = tasks/phases).
- Bars: colored by category (use DESIGN.md tokens), labeled inside or beside.
- Milestones: diamond (*) or circle markers with labels above.
- Generous spacing; snap conceptually to grid.
- ViewBox for SVG: 0 0 960 400 typical; wider for long timelines.

## Mermaid Implementation
Use `gantt` syntax with custom init from DESIGN.md (warm paper or Swiss palette, IKB accent for key items).
Include legend for categories.

**Critical preview-safety rule (iterated from real overflow cases)**:
- Inside the gantt block: **only ultra-short identifiers** (V1.1, V1.2, PhaseA-1 etc.). Descriptive names (Chinese or long English) will overflow the bar box in Typora/Obsidian/GitHub/Mermaid 11.x because bar pixel width depends on duration, not text.
- Immediately after the ```mermaid block: a Markdown table mapping ID → full name → duration → key deliverable.
- Always append a clean ASCII Gantt version (see templates/ascii-gantt.txt) as the guaranteed clean rendering for the source document.

## ASCII Fallback (for terminal/READMEs)
- Time header row.
- Rows with character bars: |===| for duration (length proportional).
- * or o for milestones.
- Align columns strictly (mono font, 80-col limit).
- Legend at bottom.
- Example in templates/ascii-gantt.txt.

## Validation
- Time data explicit.
- Categories consistent.
- **Inside gantt**: only short codes (no descriptive text). Descriptive mapping lives in the table below.
- No overlaps in labels (inside diagram or table).
- Legend present if >2 categories.
- For ASCII: columns aligned, no wrapping.
- Pre-check passed: any long Chinese task name was refactored to codes + table.

## When to Use
- Roadmaps, project plans, timelines.
- Per SKILL.md: prefer gantt type for temporal; ASCII when no render needed.
- Combine with variation rule if recurring in doc.