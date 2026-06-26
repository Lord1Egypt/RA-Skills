---
name: kai-business-blueprint
description: Use when generating business capability blueprints, domain-knowledge maps, or architecture diagrams from presales materials, meeting notes, or solution docs. Triggers: 商业蓝图, 商业模式画布, 领域知识大图, 架构图, capability map, strategy canvas. Not for generic documents, PPTs, or simple flowcharts.
---

# Business Blueprint Skill

Use the Python scripts in this repository as the execution surface.

## Output Directory

All generated files go into `projects/workspace/` — not the repository root.

## Industry Selection

Choose `--industry` from exactly one of: `"common"`, `"finance"`, `"manufacturing"`, `"retail"`. Select the closest match; do not invent other values.

| Industry | Hints content |
|----------|-------------|
| `common` | No hints — generic domains |
| `finance` | Risk control, credit, compliance, customer profile |
| `manufacturing` | Production planning, quality, warehouse, supply chain |
| `retail` | Store operations, membership, POS, order fulfillment |

## How to Generate a Blueprint

### Step 1: Read industry hints

Read the seed template at `business_blueprint/templates/{industry}/seed.json` and get `industryHints.checklist`.

### Step 2: Extract entities

**Architecture mode** (default, or when `meta.blueprintType` is absent):
Extract `capabilities`, `actors`, `flowSteps`, `systems`.
Read `references/entities-schema.md` for field definitions and `references/systems-schema.md` for systems layer rules.

**Domain-knowledge mode** (when seed has `meta.blueprintType: "domain-knowledge"`):
Extract knowledge entities into `library.knowledge.*`.
Read `references/domain-knowledge-extraction.md` for naming rules and extraction guide.
Read `references/knowledge-entities-schema.md` for field definitions.

### Step 3: Write blueprint JSON

Write the JSON file directly to the output path.
Read `references/blueprint-schema.md` for the complete schema structure.

### Step 4: Generate visualizations

```bash
python scripts/business_blueprint/cli.py --export <blueprint.json>
```

Default: SVG + HTML viewer. Use `--format drawio|excalidraw|mermaid` for other formats.
Read `references/route-eligibility.md` for export route selection rules.

## Architecture Rendering Rules

Use dark mode by default. Only use light mode when the user explicitly asks for it.

Never force every node in a layer into one fixed row. Dense layers must wrap,
group, or fall back to freeflow instead of becoming a toothpaste layout.
Legend must live in a bottom safe area. Never place the legend as a floating overlay in the top-right corner.
Do not use fixed-height wrappers or `overflow: hidden` to hide overflow in generated viewers.

Route eligibility matrix:

| Route | Eligibility |
|-------|-------------|
| `freeflow` | Any valid blueprint with at least one renderable node or relation |
| `architecture-template` | Categorized architecture graph with systems, capabilities, actors, and relations |
| `evolution` | Dated or staged flow where timeline ordering is explicit |
| `domain-knowledge` | `meta.blueprintType: "domain-knowledge"` with knowledge entities |

If a specialized route fails integrity, fall back according to
`references/route-eligibility.md`. If `freeflow` also fails, export exits non-zero with a structural diagnostics payload.

Geometry thresholds are machine-readable and live in
`evals/export-integrity-thresholds.json`; defect categories live in
`evals/defect-taxonomy.json`. Phase 2 does not attempt full Windows terminal parity. For encoding-sensitive terminal runs, set `PYTHONIOENCODING=utf-8`.

### Step 5: Generate downstream projection (optional)

```bash
python scripts/business_blueprint/cli.py --project <blueprint.json>
```

Generates `solution.projection.json` for downstream report/slide workflows.

## Commands

| Command | Description |
|---------|-------------|
| `--plan <path> --from <text>` | Generate blueprint JSON from source text (prefer writing JSON directly) |
| `--export <path>` | Export SVG + HTML viewer (default), or `--format` for others |
| `--validate <path>` | Validate blueprint and print JSON results |
| `--refine <path>` | Refine an existing blueprint |
| `--project <path>` | Generate canonical projection JSON for downstream skills |

Run as: `python scripts/business_blueprint/cli.py <command> <path>`

## Collaboration Boundary

This skill produces **semantic intermediate artifacts**. Downstream skills consume them:

- `report-creator` consumes `solution.projection.json` → assembles reports
- `slide-creator` consumes `solution.projection.json` → assembles presentations
- Other skills may consume `relations` → generate PlantUML or other diagram syntax
- Downstream skills should **never directly edit** `solution.blueprint.json`
- `solution.handoff.json` is viewer-only metadata, not a downstream narrative input

## Error Handling

- `--validate` returns errors → fix before `--export`.
- `--validate` returns only warnings → proceed, note warnings in handoff.
- Specialized route fails integrity → fall back per `references/route-eligibility.md`.
- `freeflow` also fails → export exits non-zero with structural diagnostics.
- Python < 3.12 → use `python3 -m business_blueprint.cli` as fallback.

## Sandbox Execution

In isolated Python sandboxes (Jupyter, cloud REPL):

```python
subprocess.run(["python", "scripts/business_blueprint/cli.py", "--export", str(blueprint_path)])
```

Do NOT use `sys.path.insert` (raises NameError) or `os.system` (not available in notebook cells).
Set `PYTHONIOENCODING=utf-8` for encoding-sensitive runs.
