---
name: codebase-radar
description: "Scan codebase for dependency graph, tech debt hotspots, and module health scores"
---

# Codebase Radar

Full-spectrum static analysis for any codebase: dependency graphs, module health scoring, tech debt detection, dead code, and visualization in Mermaid/D2.

## Workflow

1. **Project scan** — Tree view, line counts, language distribution, file size outliers.
2. **Dependency graph** — Resolve imports/requires across modules; detect circular dependencies; list external deps with versions.
3. **Cohesion & coupling** — Score each module: how focused its internals are (cohesion) and how tightly bound to others (coupling).
4. **Tech debt signals** — Scan for TODO/FIXME/HACK density, outdated dependency alerts, low comment-to-code ratio.
5. **Dead code detection** — Find unreferenced functions, classes, variables; flag large commented-out blocks.
6. **Health scorecard** — 5-dimension score per module: Cohesion, Coupling, Maintainability, Coverage estimate, Tech debt.
7. **Visualization** — Generate dependency diagram in Mermaid (`graph TD`) or D2 format.
8. **Report** — Produce project health summary with ranked refactoring priorities.

## Sample Prompts

- `codebase-radar scan --path ./my-project --format json > report.json`
- `codebase-radar scan --path ./my-project --visual mermaid --output deps.md`
- `codebase-radar health --path ./my-project --score-only --json`
- `codebase-radar deadcode --path ./src --exclude tests/`

## Safety

- Read-only scanner; never modifies source files.
- Language-agnostic for import detection; language-specific analyzers are opt-in.
- Large repos may require `--max-files` limit to avoid memory issues.
