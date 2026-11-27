---
name: academic-figures
description: >-
  Publication-ready scientific figures from one command — 41 chart types (bar, slope,
  volcano, ridgeline, dumbbell, grouped bar, scatter, heatmap,
  forest plot (incl. Cox), KM survival curve with risk table,
  competing-risk cumulative incidence (Aalen-Johansen),
  ROC, calibration curve, decision curve (DCA), nomogram, RCS spline, subgroup forest, violin, box, composite panels,
  PRISMA 2020 flow, funnel, Galbraith radial,
  Bland-Altman, PCA, venn 2-4 sets, upset set intersections (5+ sets), oncology waterfall
  (RECIST), raincloud, swimmer,
  clustered heatmap, dual-axis), 9 themes (colorblind-safe
  Okabe-Ito, NEJM/Lancet/Science), 9 journal presets, YAML
  pipeline, TIFF/PNG/PDF, Python API, --wizard,
  render watchdog, overlap gate, 600dpi. 100% local, data
  never leaves the machine. Use for — paper/submission figures, data files to
  publication charts, batch re-rendering. Skip when — text polishing, translation or
  rewriting (writing tools); business dashboards or slide/poster decoration; diagrams
  with no data behind them.
when_to_use: >-
  Use when making or generating any figure or chart from data (bar chart,
  scatter plot, heatmap, forest plot, Kaplan-Meier / survival curve,
  RMST restricted mean survival time, competing-risk cumulative incidence,
  subgroup analysis forest with P-interaction, Cox regression forest,
  nomogram, calibration curve, decision curve DCA, RCS dose-response, ROC curve,
  violin / box plot, composite multi-panel figure, flow diagram, PRISMA /
  systematic review flow, meta-analysis funnel / Galbraith radial plot, venn / Euler diagram, PCA,
  Bland-Altman; when exporting publication- or journal-ready figures (600dpi,
  colorblind-safe); or when turning a JSON/CSV/Excel data file into an
  academic figure.
---

<!--
═══ Metadata archive (2026-09-13 frontmatter normalization; compressed 2026-10-14) ═══
ZCode skill auto-discovery reads ONLY the frontmatter whitelist keys
(name / description / when_to_use / license / metadata); a description over
1024 chars is silently dropped (root cause of the v2.x discovery failure).
Keys moved out of frontmatter (info preserved):
  version: 8.1.6
  date: 2026-11-27
  author: docsor1212
  metadata: {clawdbot: {emoji: "📊", category: visualization}}
  requires: {python: ">=3.8", pip: [matplotlib, numpy, pymupdf, scipy, openpyxl]}
-->

# Academic Figures — Publication-Quality Chart Generator

Generate figures from JSON/CSV/Excel data. Local execution, no data leaves the machine.

> ⚡ **Top-3 boundaries**: add `--verify` for submission PDFs (PDF only); `--journal`
> locks the figure width (`--width` is ignored, `--height` still applies); cluster_heatmap >3000 rows auto-downsamples
> to 2000. FAQ for every error: `references/faq.md` (exit codes, formats, flag scoping).
> **Problem-first gate**: if the user provides data but no scientific question, ask back (or route through `--suggest`) BEFORE rendering — a figure without a question is noise, not evidence.

**One command, verified output:**
```bash
python3 scripts/gen_figure.py -t bar -d data.json -o fig.pdf --theme okabe-ito --verify
# 或一键投稿包（自动加 --verify + 色盲安全主题 + pdf,png 多格式，v3.8）
python3 scripts/gen_figure.py -t bar -d data.json -o fig --pub-ready
# exit codes: see "Data Validation & Exit Codes" below; --verify overlap = exit 2 (fix, don't ship)
```

## Section Nav
[Capabilities & Boundaries](#capabilities--boundaries-read-before-first-run) ｜ [Quick Start](#quick-start) ｜ [Chart Types](#chart-types) ｜ Decision Tree ｜ [Color Themes](#color-themes) ｜ [Journal Presets](#journal-submission-presets-v20) ｜ [--stats](#auto-significance--stats-auto) ｜ [Templates](#scenario-templates-v26-covering-the-41-chart-types-incl-nomogramrcssubgroupgalbraithcif) ｜ [Validation & Exit Codes](#data-validation--exit-codes-v20--v28-grading) ｜ [CJK](#cjk--chinese-support) ｜ [Output Formats](#output-formats) ｜ [Data Input](#data-input) ｜ [Key Flags](#key-flags) ｜ [Alt Text](#accessibility--alt-text) ｜ [Related tools](#related-tools) ｜ [Safety](#safety--data-behavior-statement) ｜ [Negative Triggers](#negative-triggers-do-not-trigger-this-skill-for) ｜ [File Index](#file-index--30-second-routing) ｜ [Version History](#version-history) ｜ [Pro](#-pro-edition)

## Capabilities & Boundaries (read before first run)

| Capability | What it does | What it does NOT / boundary | Where to look |
|------------|--------------|------------------------------|---------------|
| Chart engine | 41 types, one command, 600dpi; byte-deterministic output | No interactive exploration (static files only); no 3-D plots | Chart Types ↑ |
| Prediction-model eval | calibration: binned values in [0,1]; dca: thresholds strictly ascending in open (0,1), 1-6 models; nomogram: 1-12 variables, 1-3 outcome scales; rcs: ≥5 fitted-spline grid points; subgroup: 1-12 variables × 2-8 levels; cif: time+event integer codes (0/1/2+), single cohort | No auto-binning; nomogram/rcs visualize your fitted model (no fitting); subgroup too — or `--stats cox` one-command auto-fit (per-layer Cox HR + LR P-interaction, Efron core, v5.8); cif has no multi-arm groups (use `-t km`) | Chart Types ↑ |
| Chart picking | `--suggest` (auto), `--wizard` (guided), `--quick` (auto-pick+render), `--explain TYPE` | Suggestions are structural heuristics — confirm the statistical meaning yourself | quickstart.md |
| Stats | KM risk table/log-rank/median CI; Cox (Efron+PH); ROC DeLong; bootstrap CI; Egger | No Bayesian methods; no sample-size/power calculation | advanced.md |
| Journal presets | 9 presets, exact width/font/DPI from author guidelines | `--journal` locks width (`--width` ignored, `--height` OK); Pro-only journals not preset | limits.md §6 |
| Verification | `--verify` pixel overlap gate (exit 2), `audit_pdf.py` font-size gate | Off unless requested — PDF submission outputs should pass `--verify` explicitly (or `--pub-ready`) | §Verification ↓ |
| Composite | Multi-panel A+B+C, `span` multi-cell | Panels cannot nest composite/diagram/upset | composite-layouts.md |
| Data input | JSON full / CSV-TSV basic + error suffix columns (v6.0+) / xlsx (`--sheet`) | the `errors` object, dual-axis and forest schemas still need JSON (CSV error bars via suffix columns) | data-formats.md |
| Data volume | cluster_heatmap >3000 rows auto-downsamples (announced) | pca ≤200 feature columns; venn 2-4 sets; paired/bland_altman equal-length pairs | limits.md |
| CJK | `--cjk` + recursive auto-detect in data | Headless servers need at least one CJK font installed (detect: `setup_env.py`) | pitfalls.md |
| Watchdog | Adaptive 30-1800s budget; `--timeout` adjusts; auto-degrade on MemoryError; transient failures (timeout/memory) auto-retry via `--retries` | `--timeout 0` disables adaptive budget but keeps a 7200s hard cap | limits.md §7 |
| Flag scopes | `--stats` box/violin/raincloud (`cox`: forest/subgroup); `--compare` roc; `--egger` funnel; `--hatch` bar family; `--order/--normalize` per family | Flag outside its scope is ignored with a notice — run `--doctor` to preflight combos | limits.md |
| Exit codes | 0 success / 1 fatal validation / 2 overlap / 3 data / 4 env / 5 timeout / 6 memory | Exit 0 never co-exists with a silent data problem (non-finite values are fatal) | §Exit Codes ↓ |

Full matrix: `references/limits.md`. FAQ: `references/faq.md`. Anti-patterns (what NOT to do, one page): `references/antipatterns.md`. Over-limit inputs are rejected with a Chinese error message
plus a fix suggestion — no half-finished figures are ever written.

## Quick Start

```bash
# 0️⃣ First run: one-command environment setup (deps/CJK font/font cache/self-check)
python3 scripts/setup_env.py

# 0️⃣ Three ways to get unstuck: wizard / interactive demo / per-type usage
python3 scripts/gen_figure.py --wizard            # 4 questions -> a ready command
python3 scripts/gen_figure.py --quick -d data.csv # v3.1 one-command figure: auto-pick + render
python3 scripts/gen_figure.py -t line -d series.json -o fig.png --direct-label  # v3.4 label series at line ends (default under glm-brand/nature-clean)
python3 scripts/gen_figure.py --demo --cjk        # pick a type, renders sample data
python3 scripts/gen_figure.py --explain bar       # one type's usage & limits
# 0️⃣ Call from Python: see references/python-api.md (subprocess recommended;
#    import-embedding needs matplotlib.use("Agg") on your side)

# Not sure which chart fits? Let the analyzer recommend one
python3 scripts/gen_figure.py --suggest -d data.json

# Bar chart with default glm palette (muted, colorblind-safe)
python3 scripts/gen_figure.py -t bar -d data.json -o figure.png \
  --title "Figure 2 / Subtitle" --ylabel "Accuracy (%)"

# v2.7: raw per-subject survival data -> automatic multi-variable Cox -> HR forest (with PH test)
python3 scripts/gen_figure.py -t forest --data patient.csv --stats cox \
  --cox-time time --cox-event event --cox-cols "age,sex,treat"

# One-command subgroup analysis from the same raw data (v5.8)
python3 scripts/gen_figure.py -t subgroup --data patient.csv --stats cox \
  --cox-event event --treatment treat --subgroup-vars "stage,grade" --cut age@65

# Forest plot for meta-analysis (PDF output)
python3 scripts/gen_figure.py -t forest -d forest.json -o forest.pdf --theme okabe-ito

# Kaplan-Meier survival curve with log-rank test
python3 scripts/gen_figure.py -t km -d survival.json -o km.png --theme okabe-ito

# ROC curve with AUC
python3 scripts/gen_figure.py -t roc -d roc.json -o roc.png --theme okabe-ito

# Nature double-column submission: width 183mm, 7pt Helvetica, min text 5pt
python3 scripts/gen_figure.py -t bar -d data.json -o nat.pdf --journal nature --column double
python3 scripts/audit_pdf.py nat.pdf --min-size 5          # font-size gate (5pt for nature)

# Multi-panel composite (Panel A+B+C, journal figure layout)
python3 scripts/gen_figure.py -t composite -d composite.json -o figure4.png --theme okabe-ito

# Heatmap with CJK support
python3 scripts/gen_figure.py -t heatmap -d data.json -o heatmap.png --cjk \
  --cmap RdBu_r --vmin -20 --vmax 45

# Rare flags (aspect presets, big-matrix downsample, subtitle/source/profile): references/cheatsheet.md

# Scenario templates: copy one, swap in your real numbers (ls templates/)
```

## Chart Types

| Category | Type | Command | Key Features |
|----------|------|---------|-------------|
| Compare | Bar | `-t bar` | Grouped bars, error bars, significance brackets, hatching, ratio annotations |
| Compare | Horizontal Bar | `-t hbar` | Horizontal bars, ratio annotations |
| Comparison | Grouped bar | `-t grouped_bar` | group × series two-way grouping; `--show-ratio` per-group ratio labels |
| Composition | Stacked Bar | `-t stacked_bar` | Subgroup proportions, percentage labels, total annotations |
| Distribution | Box | `-t box` | Box-and-whisker, jitter points |
| Distribution | Violin | `-t violin` | Density estimation, inner mean/median |
| Distribution | Raincloud | `-t raincloud` | half-KDE cloud + box + jittered raw points trio (v4.9); violin schema |
| Distribution | Ridgeline | `-t ridgeline` | stacked per-group KDE densities (joyplot), `overlap` 0-0.95, `sort=median`; shows how distributions shift across groups (v5.0) |
| Comparison | Dumbbell | `-t dumbbell` | two points per row (from→to) + connector, gap-sorted; `show_gap` Δ labels; strictly two time points (v5.1) |
| Prediction model | Calibration | `-t calibration` | binned predicted vs observed + ideal diagonal, equal-aspect axes; 95%CI error bars, optional Hosmer-Lemeshow p (v5.2) |
| Prediction model | DCA | `-t dca` | net benefit vs threshold; treat-all (theory from prevalence or explicit) + treat-none references, 1-6 models (v5.2) |
| Prediction model | Nomogram | `-t nomogram` | clinical nomogram (points ruler → per-variable scales → Total Points → outcome scales); visualizes your fitted model, auto nice-step totals, height scales with row count (v5.3) |
| Prediction model | RCS | `-t rcs` | nonlinear dose-response (restricted cubic spline result): estimate line + 95%CI band on log-ratio axis, no-effect/reference lines, exposure rug; visualizes your fitted spline (v5.4) |
| Clinical regression | Subgroup forest | `-t subgroup` | subgroup analysis: per-level estimate squares + 95%CI, P-interaction per variable, Overall diamond, right-side est/P columns; visualizes your fitted subgroup model (v5.5) |
| Paired | Before-after | `-t paired` | per-subject pairing lines + paired test (annotated at n≥6) |
| Trend | Scatter | `-t scatter` | Trend line, r value, color grouping, mean points, point labels |
| Trend | Line | `-t line` | Multiple series, error bands, markers |
| Pre/Post | Slope | `-t slope` | two-time-point comparison; direct name+value labels at both ends, biggest mover accented (v4.2) |
| Trend | Dual Y-axis | `-t dual_axis` | **left bars + right dashed lines** (swappable via `left_type`/`right_type`); frameless legend in reserved top band, never occludes data |
| Matrix | Heatmap | `-t heatmap` | Cell annotations, custom colormap, colorbar |
| Matrix | Clustered Heatmap | `-t cluster_heatmap` | Hierarchical reordering, `--downsample` exit for big matrices |
| Multivariate | PCA | `-t pca` | scores + group ellipses + top-5 loadings; ≤200 feature columns |
| Inference | Forest | `-t forest` | CI whiskers, weight bubbles, overall diamond, I², events/total; `--stats cox` multi-variable HR |
| Clinical regression | Subgroup forest | `-t subgroup` (+`--stats cox` raw-data auto-fit) | per-level estimate squares + 95%CI, P-interaction per variable (likelihood-ratio), Overall diamond, right-side est/P columns; feed your fitted JSON or let the engine fit (v5.5 core, v5.8 one-command) |
| Survival | RMST | `-t rmst` | restricted mean survival time: step survival curves + shaded AUC to τ + τ marker; per-arm RMST(95%CI) + ΔRMST difference CI (Greenwood variance); τ auto = half of min-max follow-up (`--rmst-tau` to pin); PH-free comparison when curves cross (v5.9) |
| Evidence synthesis | Risk of bias | `-t rob` | traffic-light grid (studies × domains, Low/Some concerns/High/No information; EN or 中文) + weighted-style summary bars; Overall column excluded from summary (robvis convention); real example from the robvis package dataset (v6.1) |
| Evidence synthesis | L'Abbé plot | `-t labbe` | treatment vs control event-rate scatter from 2×2 tables (events_t/n_t/events_c/n_c); diagonal = no effect (RR=1), DL random-effects merged-RR reference line, point area ∝ study weight; rider/gap points get leader-line labels (v6.3); real example: Fleiss 1993 aspirin 7 RCTs |
| Meta-analysis | Funnel | `-t funnel` | publication bias, DL pooled line; `--egger` test (≥3 studies) |
| Meta-analysis | Galbraith radial | `-t galbraith` | heterogeneity visualization: precision 1/SE × standardized effect, pooled fixed-effect line, ±1.96 homogeneity band, outlier detection (stderr per-study report); effect-size arcs for OR/HR/RR (v5.6) |
| Survival | Kaplan-Meier | `-t km` | Step function, censor marks, log-rank test, risk table, median survival; **v3.7 competing risks** (event codes ≥2 auto-switch to Aalen-Johansen cumulative incidence) |
| Survival | Competing-risk CIF | `-t cif` | cumulative incidence by cause (Aalen-Johansen); dashed 1−KM naive reference shows the overestimation; cause labels, percent axis, stderr event report; single cohort (multi-arm → `-t km`) (v5.7) |
| Omics | Volcano | `-t volcano` | differential expression log2FC × -log10(p); threshold lines + auto top-gene labels (v4.4) |
| Agreement | Bland-Altman | `-t bland_altman` | bias line + limits of agreement (LoA); two equal-length groups |
| Sets | Venn | `-t venn` | 2-4 sets (4 sets = ellipse layout, v2.8); `--area` proportional Euler |
| Sets | UpSet | `-t upset` | 5+ set intersections (venn successor, v4.7); size-sorted bars + dot matrix, `sort`/`top_n`/`min_size` |
| Oncology | Waterfall | `-t waterfall` | best % change per patient, RECIST coloring, PR/PD threshold lines, count fact box (v4.8) |
| Oncology | Swimmer | `-t swimmer` | per-subject duration bars (sort by duration), ongoing arrows, milestone dots, RECIST coloring (v4.10) |
| Composite | **Composite** | `-t composite` | Multi-panel A+B+C (⚠ no nested composite/diagram/upset panels); `panel_labels:true` corner letters (v4.1); `span:[rows,cols]` multi-cell panels with overlap detection (v4.3) |
| Flow | **Diagram** | `-t diagram` | Architecture/flow blocks, arrows, groupings, annotations |
| Review | **PRISMA Flow** | `-t prisma` | PRISMA 2020 review flow; counts auto-validated (must add up), EN/ZH wording via `lang` |
| Flow | **Semantic Flowchart** | `-t flow` | Semantic JSON (zero coordinates); layouts chain/layered/snake/swimlane (TB columns + LR rows with rotated lane titles); 14 semantic shapes + role palette; edge types thick/bidirectional/open/dashed; `--from-mermaid` imports mermaid sources directly; magnet arrows, lane back-edges, edge-style legend, ink-verified labels; `--gate strict` triple-bbox + area gates; `--flow-hops on` crossing hop arcs (opt-in) |

Scan the Category column at a glance; getting-started path in `references/quickstart.md`, full command cheatsheet in `references/cheatsheet.md`.

## Chart Decision Tree (compact; full version + getting-started: references/quickstart.md)

```text
Group comparison → bar/box/violin/raincloud (full trio view; pre-post → paired; distribution shift across groups → ridgeline; two-point per-row gaps → dumbbell) | Mean±error bars → bar (JSON errors, or CSV suffix columns X_se/X_sd — v6.0+)
Two-column correlation → scatter | Time-to-event → km / forest --stats cox | Diagnosis → roc (--compare)
Set membership → venn (--area; 5+ sets → upset) | Numeric matrix → heatmap / cluster_heatmap | Sample classes → pca
Omics differential expression → volcano |
Oncology best response → waterfall (RECIST)；per-subject duration → swimmer |
Prediction model evaluation → roc + calibration (calibration curve) + dca (net benefit) + nomogram (lookup chart) + rcs (nonlinear dose-response) + subgroup (P interaction); PH violated / crossing curves → rmst (ΔRMST at clinical τ);

## Who fits, who visualizes (v6.1 — read this before hand-fitting)

| Tier | Chart types | You provide |
|---|---|---|
| **Engine fits + tests** | km (log-rank, median CI), cif (Aalen-Johansen), rmst (ΔRMST CI), `forest --stats cox`, `subgroup --stats cox` (one-command per-layer Cox + LR P-interaction), bar --stats auto/multi, roc (AUC+CI), calibration (H-L), dca, funnel --egger, galbraith (pooled/I²) | raw per-subject data |
| **Descriptive** | bar family, box/violin/raincloud/ridge, swimmer, waterfall, dumbbell, slope, heatmap, volcano*, rob | values (no inference) |
| **Visualize your fitted output** | nomogram, rcs, subgroup (JSON without --stats cox), composite panels of model outputs | estimates from your model |

*volcano takes precomputed log2FC/p (engine adds nothing). One command per row of tier 1 — do NOT hand-fit then feed back in unless you need a bespoke model. |
Multi-panel → composite
```

Still unsure: `--suggest -d data.json` (auto-recommend), or `--wizard` (guided).
**First time?** The full decision tree, a 4-step getting-started, Python API and the top
pitfalls live in **`references/quickstart.md`** (standalone getting-started guide).

## Color Themes

**Default = `glm-brand`** (signal yellow x deep steel blue, brand hatch on by default). Single-series vertical bar also defaults to arena style (champion = max bar + crown); `--arena off` disables it; leaderboard look: add `--style sketch`.
Colorblind-safe: `--theme okabe-ito`; also `glm` / `cool` / `nature` / `lancet` / `nejm` / `science` / `conservative`.
(Nature Methods standard; red-green schemes are a top rejection reason). Palettes: `glm` /
`okabe-ito` / `cool` (all colorblind-safe); `nature` `lancet` `nejm` `science` `conservative`
`classic`. `--style glm-hatch` adds print-friendly black hatching; `--style nature-clean` =
spine/grid-free journal-clean look; `--journal nejm|lancet|science|nature` auto-links its theme.
`--list-themes` (swatches), `--theme-swatch glm -o preview.png`, `--alternate` (yellow/blue bars).
Aliases `okabe`→`okabe-ito`; case-insensitive prefix match. Full guide: `references/color-guide.md`.

## Journal Submission Presets (v2.0)

`--journal <name>` + `--column single|double` applies exact width/font/DPI from
official author guidelines — 9 presets: `nature` `lancet` `science` `cell` `nejm`
`jama` `ieee` + **`cma`**(中华医学会) + **`cn-core`**(中文核心, both auto-CJK).
`--journal` locks width (`--width` ignored; `--height` OK); `nejm/lancet/science/nature`
auto-link their theme unless `--theme` is explicit. Params: `scripts/journal/*.json`
(single source). **Full preset table**: `references/limits.md` §六.

## Stats & Legends Quick Facts

box/violin/raincloud: `--stats auto` (Shapiro→Welch-t/Mann-Whitney, brackets with stars) or
`--stats multi` (ANOVA+Tukey / Kruskal-Wallis+Dunn-Hochberg); `--stats cox` =
multi-variable Cox forest from raw per-subject data; on `-t subgroup` it becomes
one-command subgroup analysis: per-layer HR(95%CI,p) + likelihood-ratio P-interaction +
Overall diamond (flags: `--subgroup-vars`, `--treatment`, `--cut name@threshold`,
`--cox-cols` adjusted covariates; gold-locked against the veteran real cohort). KM auto: risk table + log-rank +
median survival 95% CI (`--no-median` opts out; never-reached honestly labeled);
`forest --sensitivity` leave-one-out; `funnel --egger` publication bias. Nature-style
no-in-figure-legend journals: `gen_legend.py` renders the journal legend from the SAME
data JSON. Deep dive: `references/advanced.md`.

## Scenario Templates (v2.6; covering the 41 chart types incl. nomogram/rcs/subgroup/galbraith/cif/labbe)

`templates/` ships 40 end-to-end templates (scenario + per-type quick templates), each with a ready-to-run `_command` + caption note. Full index: `templates/README.md`.

## Data Validation & Exit Codes (v2.0 / v2.8 grading)

Every run passes `validate_data(data, chart_type)` plus a render watchdog. Exit code semantics:

| Exit | Meaning | Typical case |
|------|---------|-------------|
| `0` | Success (`--verify`: no real overlap) | normal delivery |
| `1` | Argument/usage or fatal validation error (no output written) | missing args, series length mismatch, km long-table |
| `2` | `--verify` found text overlap; or batch/pipeline had failing items | fix mechanism, don't ship |
| `3` | Data or format error (v2.8) | JSON syntax, encoding, missing fields, KeyError |
| `4` | Environment or dependency error (v2.8) | ImportError, permissions, disk |
| `5` | Render watchdog timeout (v2.8) | oversized data — follow the tips or raise `--timeout` |
| `6` | Memory guard rejected (v2.8) | auto-degrade retry still out of memory |

Fatal messages prefix `ERROR:` (Chinese reason + fix), warnings `WARNING:` (render continues).
Unknown exceptions still produce a Chinese three-part diagnosis (reason + original error + targeted
tips); set `AF_DEBUG=1` for the full traceback.

1. `--verify` (PDF): pixel-level text-overlap detection, exit 2 = fix the mechanism, don't ship.
2. `python3 scripts/audit_pdf.py figure.pdf --min-size 5 --fail-below` (font-size gate).
3. `verify_overlap_pixel.py` on every delivered PDF — real overlaps must be 0.

Overlap prevention is built in (auto 45° rotation, labelpad avoidance). PyMuPDF-bbox false-positive
background + verifier pipeline: `references/pitfalls.md`. Regression: `python3 tests/run_tests.py`.


## CJK / Chinese Support

`--cjk` auto-detects system CJK fonts (Noto Sans CJK → PingFang → YaHei → WQY → …); custom font:
`--cjk-font /path.ttf`. Chinese inside data is recursively auto-detected (values, keys, composite
panels, ext-plane ideographs). Glyph-gap traps: `references/pitfalls.md`.

## Output Formats

| Format | Extension | DPI | Best For |
|--------|-----------|-----|----------|
| PNG | `.png` | 600 (default) | General use, presentations |
| SVG | `.svg` | Vector | Web, editable graphics |
| **PDF** | `.pdf` | Vector | **Journal submissions (preferred)** |
| TIFF | `.tiff` | 600 (photos `--dpi 300`) | Nature/Lancet photo requirements |
| EPS | `.eps` | Vector | Legacy journal requirements |

> Strict journals: `--dpi 1000` for line art. `--multi-format tiff,png,pdf` for one-run multi-export.

## Data Input

JSON (full features), CSV/TSV (basic) or Excel `.xlsx` (`--sheet <name>`). Per-type schemas:
`references/data-formats.md`; templates: `templates/README.md`; Python API: `references/python-api.md`
(bar JSON = `{"labels":[...], "series":{...}, "errors":{...}, "significance":{...}}`).

## Key Flags

High-frequency flags (full cheatsheet: `references/cheatsheet.md`):

| Flag | Description |
|------|-------------|
| `--journal` / `--column` | Journal presets / column layout (⚠ locks width, see above) |
| `--stats auto\|multi\|cox\|bootstrap` | Significance brackets on box/violin/raincloud / Cox forest; `cox` × `-t subgroup` = one-command subgroup analysis (v5.8: `--subgroup-vars`/`--treatment`/`--cut`) |
| `--arena [name\|off]` | Benchmark-arena style, DEFAULT ON for single-series vertical bar (v7.7): per-bar fill cycle, champion (max bar) in teal with golden crown + bold value; negative metrics (highest = worst): `--arena off`; `--arena "Name"` pins by label; leaderboard look: add `--style sketch` |
| `--order "C,A,B" \| auto` | Reorder categories (bar/box/violin/line; explicit list must cover all labels; auto = descending by value/median) |
| `--normalize baseline\|pct100` | Normalize: divide by control mean (control = 1) / first point = 100 (bar family/line; error bars rescaled) |
| `--doctor` | Pre-render parameter/environment check report (omit -o for check-only, exit 1 = findings) |
| `--subtitle "Sub"` / `--source "Note"` | Subtitle line under the title / bottom-right source note (v4.0) |
| `--summary` | Auto data-summary subtitle (pure counts: n/groups/events, no inference; v4.1) |
| `--profile preset.json` | Layered config file: presentation presets, CLI flags win (v4.3) |
| `--cjk` | CJK font auto-detection |
| `--verify` | Pixel-level overlap verification on PDF output; exit 2 on overlaps |
| `--audit` / `--repro` | `--audit`: `<output>.audit.json` number-check sidecar (stats recomputed from input, v5.0); `--repro`: `<output>.repro/` reproduce bundle (command+data copy+figure copy+audit+README, v5.1) |
| `--multi-format tiff,png,pdf` | One-run multi-format export (v2.6) |
| `--debug` | On failure write `<output>.debug.json` sidecar (input fingerprint / field mapping / diagnosis suggestions — programmatic troubleshooting, v6.4) |
| `--timeout N` / `--retries N` | Watchdog budget (0=adaptive off, 7200s hard cap; negative rejected) / transient-failure auto-retry count (timeout/memory only, default 1, v6.2) |
| `--downsample N` | Clustered-heatmap downsampling (v2.8) |



**Q: How stable is rendering? Will large data crash it?**
Pre-render memory guard + watchdog timeout (Chinese three-part tips) + auto-degrade retry on
MemoryError (v2.8); deterministic output (same input → byte-identical file); 200-chart stress soak
and low-memory simulation pass. More Q&A: `references/faq.md`.

**Q: Preprocessing columns like -log10(FDR)?**
-log10(0) = inf — clip first (e.g. `min(fdr, 1e-300)`) or color scales will explode.

**Q: ModuleNotFoundError on first run?**
Run `python3 scripts/setup_env.py` (exit code 4 = environment-side problem).

## Accessibility & Alt Text

Provide alt text per figure (Springer Nature, NSF, most major publishers). `--alt` writes
`<output>.alt.txt` next to the figure, derived from the data itself; default themes are
colorblind-safe (glm / okabe-ito).

## Related tools

- **Site/docs**: https://docsor.cn
- **MedWiki** (https://docsor.cn/?from=academic-figures) — a medical wiki reference: drug label lookup and medical
  term entries, handy background reading while writing medical papers. Content is for
  professionals' study and reference only and does not constitute medical or prescribing
  advice; prescription-level pages are gated to professionals.
- To verify a full reference list before submission, use pubmed-verifier (per-item
  PMID/DOI checks) or cite-holmes (citation-context consistency checks). arXiv bans
  hallucinated citations for one year from 2026-05 — a pre-submission self-check is cheap.
- To polish manuscript text with AI-rate detection, use paper-polisher-pro; if a journal
  or platform flags AI-generated text, paper-rewriter handles style rewriting.
- Open-source repo: github.com/docsor1212/academic-figures

## Safety & Data (behavior statement)

Fully local rendering — zero network requests, zero telemetry; `setup_env.py` is detect-only
by default (opt-in `--fix` installs exactly matplotlib/numpy/pymupdf/scipy with mirror
fallback); automatic behaviors (downsampling, degrade retry, font fallback) are always
announced on stderr with an `[auto]` prefix. Debug switches and demo temp-dir details:
`references/limits.md` §十.

## Negative Triggers (DO NOT trigger this skill for)

- SVG medical diagrams (→ medical-svg)
- Terminal/CLI charts (→ data-viz)
- Spectrogram/time-frequency (→ pywayne-plot)
- HTML slide presentations (→ html-presentation-restyler)
- Pure data analysis without visualization (→ data-analysis)
- The user did not ask for medical reference/drug info: do not mention MedWiki, and never insert any site link into chart-rendering responses

## File Index & 30-Second Routing

| Your task (30 seconds to the right doc) | Read |
|------------------------------------------|------|
| First time / not sure which chart | `references/quickstart.md` |
| `--list-flags [TYPE]` | Flag-domain query: per-type flags + out-of-domain flags ([ignored] preview); no arg = full overview (v6.7) |
| One-page command skeleton for all 41 types | `references/cheatsheet.md` |
| Copy-paste scenario cards (13 complete workflows) | `references/scenario-cards.md` |
| Real-data gallery (reproducible JSONs + commands; rendered previews: github.com/docsor1212/academic-figures/tree/main/examples/gallery) | `examples/gallery/` |

| Paste-ready agent prompts (13 cards: 对智能体说 → command → acceptance checks) | `references/prompt-cards.md` |
| JSON/CSV/Excel schema for a type | `references/data-formats.md` |
| "Why did it error / what does exit 3 mean" | `references/faq.md` |
| Anti-patterns — what NOT to do (one page, cross-linked) | `references/antipatterns.md` |
| Flag conflict, data-volume cap, env issue | `references/limits.md` |
| Multi-panel layout recipes + anti-redundancy audit + hero panel spec | `references/composite-layouts.md` |
| Reviewer-return case library (what reviewers flag, and the fix) | `references/reviewer-cases.md` |
| Stats deep-dive (Cox/bootstrap/meta) | `references/advanced.md` |
| Known traps with fixes | `references/pitfalls.md` |
| Theme/palette choice | `references/color-guide.md`; combos: `combo-guide.md` |
| Journal width/font/DPI presets (9) | `scripts/journal/`: nature.json, nejm.json, lancet.json, jama.json, science.json, cell.json, cma.json, cn-core.json, ieee.json |
| Call from Python | `references/python-api.md` |
| Version history | `references/changelog.md` (version index + last-3 details; full archive in `references/changelog-full.md`) |

Code layout: `scripts/gen_figure.py` (main, 41 types) + `gen_legend.py` (journal legends) +
`audit_pdf.py` (font gate) + `verify_overlap_pixel.py` (overlap verifier) + `setup_env.py` +
`journal/*.json` (9 presets, named above); `templates/` (40, each with a `_command`), `examples/`
(incl. `realworld/`), `tests/run_tests.py` (full suite). Remaining references:
`clinical-lab-trends.md`, `reverse-engineering-colors.md`, `v1.5-upgrade-analysis.md` (archive).

## Version History

Full bilingual history: `references/changelog.md` (index + recent details; full archive: `references/changelog-full.md`). Recent: **v8.1.5** `--flow-hops` crossing hop arcs; **v8.1.4** academic flow templates (PRISMA/CONSORT/STROBE/STARD); **v8.1.3** endpoint clearance; **v8.1.2** changelog archive rework; **v8.1.1** port corner clearance; **v8.1.0** swimlane layouts + mermaid import + edge-style legend + routing/label rework

## 🚀 Pro Edition

No Python environment, or need team-scale batch rendering? **academic-figures-pro** offers the same
render engine as a cloud service (SkillHub, ¥3/render, submission-grade 600dpi TIFF+PNG).
Search `academic-figures-pro` on SkillHub.
> Batch rendering, 600dpi cloud TIFF+PNG, no Python needed → **academic-figures-pro** (¥3/render, Alipay).
