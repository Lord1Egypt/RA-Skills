# Contributing to archviz-skills

Thanks for your interest in contributing!

## How to contribute

1. **Fork** the repo
2. **Create a branch** (`git checkout -b feature/my-addition`)
3. **Make changes** following the design system in DESIGN.md
4. **Test** your templates render correctly in Obsidian/GitHub
5. **Submit a PR** with a clear description

## Guidelines

- All templates must follow DESIGN.md tokens (Warm Paper or IKB, max 1 accent)
- All templates must declare the DESIGN.md contract layer they serve: atmosphere, tokens, components, layout, or guardrails
- Mermaid templates must be preview-compatible (no architecture-beta in .md source)
- ASCII templates must fit 80 columns
- Keep labels short (≤6 words / ≤8 Chinese chars)
- No emoji in labels or node names
- Light surfaces must use dark text. Do not pair Warm Paper / Stone surfaces with near-white text.

## Adding templates

Place in the correct subdirectory:
- `templates/mermaid/` — .mmd files
- `templates/ascii/` — .txt files  
- `templates/html/` — .html files (self-contained, no deps)
- `templates/python/` — .py files (Plotly/Matplotlib)

Include a comment header with: diagram type, use case, env, dials, palette, validation target.

Before PR:
1. Compare the output against DESIGN.md, not personal taste.
2. Run a render check in the target environment.
3. Confirm contrast, no overlap, short labels, and fallback strategy.
4. If tokens change, update README, SKILL.md quick reference, and examples that hardcode the old values.

## Reporting issues

Use the issue template. Include: what you expected, what happened, which environment (Obsidian/GitHub/terminal).
