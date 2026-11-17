# Figure Output & Rendering Rules

> Detail companion to `SKILL.md` §Figure Output & Rendering. English-only.
> (Chinese strings below are **user-facing UI phrases** that agents must quote verbatim to Chinese users — same class as the §6.7.2 conversion notice; they are runtime copy, not documentation prose.)
> Normative source of truth: the ct- unified figure-rendering spec (SVG-first, PNG fallback).

## Rendering priority — mandatory (user rule 2026-08-20)

1. **Inline first (default):** the agent MUST inline the returned SVG **directly into the conversation stream** via the visualization channel — the figure appears in the chat, not as a file. Files persisted to `CTSS_OUTPUT_DIR` (default `./outputs`, `ctss_<test>_*.svg`) are **backup / editing only** — never present SVG as file-first.
2. **Fallback ladder** (if inline SVG cannot be displayed in the conversation, in order):
   - ① **HTML-wrapped preview** — embed the SVG in an HTML page opened in the preview panel; stays vector (selectable / zoomable / editable).
   - ② **PNG bitmap** — local `cairosvg` conversion.
3. **Natural-language prompts only:** never force the user to touch CLI flags — guide them with a directly-repeatable prompt: 「图形无法预览，请改用 PNG 图片格式重新出图」/「把图转成 PNG 文件」 (EN: "The figure can't be previewed, please re-render it as a PNG image" / "Convert the figure to PNG").

## Power reference line & no hand-redraw rule (user rule 2026-08-20)

- **Reference-line rule (user rule, 2026-08-30 定稿):** the sample-size-vs-power curve is **always drawn in the conventional orientation — X-axis = sample size N, Y-axis = power** — regardless of solve direction. Both solve directions therefore draw a **dashed reference line at the user-supplied quantity** on this standard orientation: forward solves (solve `n`, given `power`) draw a **red horizontal line at the given `power`** (`power = X` label) whose X-intersection is the required sample size; reverse solves (solve `power`, given `n`) draw a **blue vertical line at the given `n`** (`n = X` label) whose Y-intersection is the achieved power. No cross-direction horizontal/vertical mix is used (a horizontal 0.8 line would land its intersection exactly on the computed sample size only if the y-axis were power — which it is in the standard orientation, so the intersection IS the intended sample size). Applies to both `adapters/coze/src/r_engine/run_task.R` (forward `abline(h = p$power)` / reverse `abline(v = p$nobs)`; a forward `pw_seq`-only input is transposed back to X=N before plotting) and the local fallback `_curve_svg_from_stats` (transposes `x=power,y=n` stats to X=N, then draws `ref_power_val` as a horizontal line via `target_power`, `ref_n_val` as a vertical line via `ref_n`). Reference lines use the **same `sx()/sy()` mapping as data points and grid labels** — one coordinate system, no axis misalignment.
- **★ Agent rule — never hand-redraw:** always present the skill-generated SVG as-is (reference line, labels, axes included). If a figure is needed for a case the skill did not plot (e.g. custom BE margins), either extend the skill or reuse the skill's numeric stats with the same axis-mapping conventions — do **not** rebuild the chart with ad-hoc coordinates inside the reply (2026-08-20 incident: an agent-drawn inline widget misaligned its y-axis ticks vs data points/reference line; charting stays under skill control so errors are fixable in code).

## figure_mode

- `svg_inline` (default) | `png_file` — local `cairosvg` converts each SVG to PNG (`svg_to_png`, strip-clip → bbox → viewBox → rasterize; emits `__FIGURE__ png` markers); use when inline SVG is slow / oversized; gracefully degrades to `svg_inline` if cairosvg missing. Set via `--figure-mode png_file` or `CTSS_FIGURE_MODE=png_file`.

## Render timing & over-threshold hint

- When `render_elapsed_seconds` > 30s or `render_svg_kb` > 200KB, the skill emits `__RENDER_HINT__` suggesting `png_file`. **★ Agent rule:** surface it in your reply and offer `png_file` — never bury it.

## Symmetry & reference implementation

- The local curve-fallback SVG generator (`_curve_svg_from_stats`) is §19-aligned (700×500, gridlines, multi-series, dynamic axis labels; stdlib only).
- `adapters/rendering.py` is the shared figure-rendering reference implementation (byte-equivalent to `meta-analysis/adapters/rendering.py`); coze SVGs use fixed `viewBox` with content drawn outside it — the pipeline auto-expands via `content_bbox()` and removes internal `clipPath` so nothing is cropped.
- SVG editing & journal format conversion (EPS/PDF/TIFF 600dpi): `references/svg_editing.md`.
