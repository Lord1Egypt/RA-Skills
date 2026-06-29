# Style Guide (adapted from fireworks-tech-graph styles + archviz-skills restrained core)

Use with Mermaid init + pretty-mermaid themes, or hybrid SVG.

## Core (Always)
- Restrained Swiss + Warm Paper + Guizang.
- One accent per set (IKB default for "arc" identity).
- Hairline primary, 2px for signature/ritual.
- Sharp corners (except mindmap defaults).
- Generous whitespace, non-symmetric where natural.
- "越大越细，越小越粗" typography.

## Style Variants (map to Mermaid themes or external render)
- **Warm Paper (default)**: #f5f0eb bg, #1B365D text, subtle borders. For docs/papers.
- **Swiss Neutral**: #f5f5f4 bg, #1B365D text. Clean, print.
- **IKB Accent**: e4e8f0 bg, IKB #002FA7 accent. For guizang Swiss PPTs.
- **Dark Terminal** (inspired): Dark bg for GitHub/dev (use with nord or custom init).
- **Blueprint** (inspired): Technical, blueprint feel (dark + precise lines).
- **Notion Clean** (inspired): Minimal, light, for modern docs.

Load matching reference if using external styles (see fireworks references/style-*.md for tokens).

## Application
- In Mermaid: custom %%{init}%% per DESIGN.md.
- For SVG: pretty-mermaid with theme or fireworks-style post-process.
- Always: legend if multi-category, caption first = finding.

See DESIGN.md for full tokens and anti-defaults.