# Workflow checklist

## Trigger

Use this skill when:
- the user shares a Figma URL
- and asks to build, restyle, compare, match, or tighten layout to that design
- including short prompts like `build this`, `make this`, `match this`, `recreate this`, `implement this`, or `implement this design`

## Execution order

1. Read Figma source
2. Fetch or identify the correct reference frame/image
3. Check fonts used in the design — ask user to connect them, warn that missing fonts cause inaccurate diffs
4. Create a dedicated run folder with `scripts/init-run-dir.cjs`
5. Choose the most stable serving path for the implementation
6. Capture the rendered page with Playwright
7. Run pixelmatch to get diff percentage and diff image
8. Run tile comparison (300px bands) — read `topMismatchTiles` to locate the worst vertical zones
9. Run OpenCV analysis on tiles with mismatches to get annotated diff and region-to-layer mapping
10. Apply visible layout fixes
11. Re-run comparison with `--compare-only` to skip Figma fetch
12. Report mismatch, artifacts, and blockers
13. Ask whether to clean up `figma-pixel-runs/<project-slug>/` working files

## Priorities

Write every artifact into `figma-pixel-runs/<project-slug>/<run-id>/`.
Reuse shared Figma API/export artifacts from `figma-pixel-runs/<project-slug>/shared/figma/` whenever the same Figma file/node is rerun.

Prefer `scripts/run-pipeline.cjs` as the orchestration entry point for the happy path. It should derive width and height from Figma node bounds, surface viewport fallback clearly when bounds are unavailable, and leave behind `run-manifest.json` and `run-result.json` at the run root.
Use `--compare-only` flag on subsequent runs to skip Figma API fetch and use the shared cache reference image directly.
Do not create unrelated working files inside the implementation project. Scratch Figma files, temporary exports, and intermediate processing assets should live under the run directory or shared cache, not inside the page/app project.

Fix biggest visible mismatches first:
- section backgrounds
- hero size and heading scale
- missing content columns
- repeated footer/meta rows
- preview panel proportions
- use real Figma-derived crops/screenshots instead of invented preview placeholders
- page ending / extra whitespace
