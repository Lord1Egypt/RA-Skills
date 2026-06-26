# Expected artifacts

## Run directory contract

Store all run outputs under:

```text
figma-pixel-runs/<project-slug>/<run-id>/
```

Recommended subfolders:

```text
figma/
capture/
backstop/
pixelmatch/
final/
```

Create this structure with `scripts/init-run-dir.cjs`.

Try to produce and retain these files for each run:

- `figma/reference-image.png`
- `capture/captured-page.png`
- `pixelmatch/diff.png`
- `final/report.json`
- `final/summary.md`
- `backstop/backstop-run-summary.json` when Backstop is used
- `backstop/html_report/index.html` when Backstop succeeds far enough to write it

## Compact-first reading order

To reduce token use during iteration, inspect artifacts in this order:

1. `run-result.json`
2. `pipeline-summary.json`
3. `final/report.json`
4. `figma/viewport.json`
5. `figma/export-image-result.json`
6. `pixelmatch/report.json`
7. `backstop/backstop-run-summary.json`

Only read larger files like full markdown summaries, raw Figma JSON, or Backstop HTML when the compact artifacts are missing or do not explain the issue.
Only send images through vision/image analysis when compact artifacts and ordinary file reads still do not explain the mismatch. Keeping images as runtime assets does not meaningfully affect token use until they are passed into the model.

## Minimum useful output

Even when tooling is unstable, try to return at least:
- reference image path
- current screenshot path
- mismatch percentage or failure reason
- diff image path if available
- short human-readable layout summary

## Notes

- Backstop can fail because of missing CLI, bad reference naming, or unreachable local URL.
- pixelmatch should remain the reliable fallback.
- Preserve raw stdout/stderr summaries when tools fail.
- Use `scripts/generate-layout-report.cjs` at the end of the pipeline to emit both machine-readable and human-readable output.
