# draw.io Output Mode

Use draw.io mode when the user needs an **editable professional diagram**, not just a rendered preview.

## When To Use

- Architecture diagrams that will be handed to engineering, teaching, or client review.
- Cloud / infra / network diagrams where vendor icons and editable shapes matter.
- Diagrams expected to continue changing after the agent response.
- Codebase / module maps that are too dense for Mermaid but still need a structured editable artifact.

Do not use draw.io mode for quick Markdown notes, small inline diagrams, or charts where data accuracy matters more than editability.

## Output Contract

Minimum deliverable:

1. A `.drawio` source file or a clear XML generation plan.
2. A PNG / SVG / PDF export recommendation if draw.io desktop CLI is available.
3. A short editability note: what can be moved, renamed, recolored, or re-routed.
4. A fallback Mermaid or ASCII outline when the environment cannot render draw.io.

## Minimal Pipeline

```text
brief
  -> diagram type + topology
  -> scene contract (nodes / containers / edges / labels)
  -> draw.io XML plan
  -> validate: ids, dangling edges, overlaps, clipped labels
  -> optional export: PNG / SVG / PDF
```

Recommended local export when draw.io desktop is installed:

```bash
drawio --export --format png diagram.drawio
drawio --export --format svg diagram.drawio
drawio --export --format pdf diagram.drawio
```

## Visual Rules

- Keep archviz tokens: warm paper, restrained borders, max one accent.
- Prefer orthogonal connectors for architecture and system diagrams.
- Use containers for layers, domains, teams, or packages.
- Use semantic shapes; do not decorate with arbitrary icons.
- If vendor icons are requested, resolve exact draw.io shape names instead of guessing.

## Agent Gate

Before shipping, check:

- Every edge has valid source and target.
- No label is clipped.
- No edge crosses through a node unless intentional and labeled.
- Diagram remains readable after export at 1200px width.
- Editable source is primary; PNG/SVG/PDF are exports, not the only artifact.

