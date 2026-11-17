# Codex Agent — Harness Reference

Use this reference when the design skill runs inside Codex. The skill remains
file-system based: create the design package under `designs/<project>/`, serve it
over HTTP, verify it in a browser when available, then report the exact paths and
URLs.

## Tool Map

| Capability | Codex behavior |
|-----------|----------------|
| Ask user questions | Ask directly in chat only when platform, scope, or source file cannot be inferred safely. Prefer reasonable defaults for rough requests. |
| Read local inputs | Use `rg`, `sed`, and normal filesystem reads. For images, inspect with available image tools before estimating values. |
| Create / edit files | Use Codex file editing tools. Keep all generated files inside `designs/<project>/`. |
| Run post-processing | Run `node <SKILL_DIR>/agents/run-pipeline.mjs designs/<project>/ --strict-measure` after `preview.html` exists. |
| Preview | Start an HTTP server for `designs/`; use Codex Browser / browser plugin if available. |
| Screenshot QA | Capture desktop and mobile screenshots when browser tools are available; otherwise run static QA and state that visual QA was not available. |
| Debug JS | Use browser console / DevTools when available; otherwise inspect script errors from terminal output and generated files. |

## Default Assumptions

When the user does not specify details:

- Platform: mobile app/H5 requests use iPhone 15/16 size `393 x 852`; admin,
  dashboard, table, or PC requests use desktop `1440px`.
- Design system: use `universal` unless the request mentions Ant Design, antd,
  antd-mobile, a known brand folder, or a platform convention such as macOS.
- Precision: use `standard` for text input, `precise` for Figma/Sketch, and
  `standard + estimated markers` for screenshots.
- Variations: produce one main design. Mention two decision points only in the
  final summary, not as extra generated screens, unless the user asks.

## Codex Workflow

1. **Load instructions.** Read `SKILL.md`, `system-prompt.md`, this file, the
   matching input handler, and the relevant design-system files. If Ant Design
   or brand tokens apply, load those after universal files.

2. **Create the project directory.**

   ```bash
   mkdir -p designs/<project-name>
   ```

3. **Generate the five core deliverables.** At minimum, write:

   - `preview.html`
   - `annotated.html`
   - `tokens.css`
   - `spec.json`
   - `assumptions.log`

   Complex prototypes may also include `data.jsx`, `components.jsx`, `app.jsx`,
   `component-tokens.css`, assets, or reports. Keep supporting files next to the
   HTML that uses them.

4. **Run deterministic post-processing.**

   ```bash
   node <SKILL_DIR>/agents/run-pipeline.mjs designs/<project-name> --strict-measure
   ```

   If this changes `preview.html`, update `annotated.html` so the visual output
   and annotations stay aligned.

5. **Serve over HTTP.**

   ```bash
   python3 -m http.server 4311 --directory designs
   ```

   If port `4311` is busy, choose the next free port and use that in the final
   URL.

6. **Verify.**

   Open:

   - `http://localhost:<port>/<project-name>/preview.html`
   - `http://localhost:<port>/<project-name>/annotated.html`

   Check that:

   - The page loads without console errors.
   - `tokens.css` resolves before page-specific CSS.
   - Dark mode works when present.
   - Mobile tap targets are at least 44px.
   - Text does not overflow obvious containers.
   - No unresolved `var(--missing-token)` names appear.

7. **Deliver.** Final response should include:

   - Local paths for the five core deliverables, measured evidence, and `acceptance.spec.mjs`.
   - Preview URL.
   - QA summary: mode, suggested/applied count, warnings, and visual QA limitations.

## Browser Unavailable Fallback

If Codex Browser / screenshot tools are unavailable:

1. Still run `run-pipeline.mjs`.
2. Inspect generated reports: `preview.qa-report.json`,
   `preview.measure-report.json`, `preview.token-report.json`, and `spec.json`.
3. State clearly: `Visual browser QA was not available; static QA passed/failed
   as follows...`

Do not claim visual approval without a rendered browser check.

## Output Summary Template

```text
Generated design package:
- preview: designs/<project>/preview.html
- annotated spec: designs/<project>/annotated.html
- tokens: designs/<project>/tokens.css
- machine spec: designs/<project>/spec.json
- assumptions: designs/<project>/assumptions.log
- measured report: designs/<project>/preview.measure-report.json
- measured screenshot: designs/<project>/preview.measured.png
- acceptance: designs/<project>/acceptance.spec.mjs

Preview URL: http://localhost:<port>/<project>/preview.html
QA: <report-only/fix>, <N> suggested, <N> applied, <N> warnings. Visual QA: <done/not available>.
```
