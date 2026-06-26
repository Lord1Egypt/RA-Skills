---
name: academic-figures
version: 1.5.0
date: 2026-06-17
author: docsor1212
description: >
  Publication-quality figure generator. 14 chart types (bar, hbar, stacked_bar,
  heatmap, scatter, line, dual_axis, box, forest, violin, km, roc, composite,
  diagram), 6 themes (okabe-ito colorblind-safe, nature, lancet, conservative,
  default, glm). CJK support, hatching patterns, ratio annotations, multi-panel
  layouts, flow diagrams. Output PNG/SVG/PDF/TIFF/EPS. matplotlib+numpy only.
  Triggers: make figure, generate chart, plot data, bar chart, scatter, heatmap,
  forest plot, violin, Kaplan-Meier, ROC, survival curve, 论文配图, 画图, 柱状图,
  热力图, 散点图, 森林图, SCI配图, 学术图表, 科研绘图, 统计图, 数据可视化,
  发表级图片, 期刊配图, hatching, 斜纹, composite, 组合图, flow diagram, 流程图.
metadata:
  clawdbot:
    emoji: "📊"
    category: visualization
requires:
  python: ">=3.8"
  pip: ["matplotlib", "numpy"]
---

# Academic Figures — Publication-Quality Chart Generator

Generate figures from JSON/CSV data. Local execution, no data leaves the machine.

## Quick Start

```bash
# Bar chart with colorblind-safe palette (recommended for all submissions)
python3 scripts/gen_figure.py -t bar -d data.json -o figure.png --theme okabe-ito \
  --title "图2 主标题 / Subtitle" --ylabel "准确率 Accuracy (%)"

# Forest plot for meta-analysis (PDF output)
python3 scripts/gen_figure.py -t forest -d forest.json -o forest.pdf --theme okabe-ito

# Heatmap with CJK support
python3 scripts/gen_figure.py -t heatmap -d data.json -o heatmap.png --cjk \
  --cmap RdBu_r --vmin -20 --vmax 45

# Scatter with trend line, Nature style
python3 scripts/gen_figure.py -t scatter -d data.csv -o scatter.png \
  --xlabel "Baseline (%" --ylabel "Gain (%)" --theme nature

# Kaplan-Meier survival curve with log-rank test
python3 scripts/gen_figure.py -t km -d survival.json -o km.png --theme okabe-ito \
  --title "图3 Kaplan-Meier生存曲线" --xlabel "时间 (月)" --ylabel "生存概率"

# ROC curve with AUC
python3 scripts/gen_figure.py -t roc -d roc.json -o roc.png --theme okabe-ito \
  --title "图4 ROC曲线" --xlabel "1 - 特异度" --ylabel "敏感度"

# Stacked bar chart (subgroup proportions)
python3 scripts/gen_figure.py -t stacked_bar -d subgroups.json -o stacked.png --theme okabe-ito \
  --title "图5 ANCA相关血管炎器官受累"

# Dual Y-axis chart (clinical score + lab marker)
python3 scripts/gen_figure.py -t dual_axis -d dual.json -o dual.png --theme okabe-ito \
  --title "图6 CRP与DAS28随治疗变化"

# TIFF output for Lancet submission (photo content → 300dpi)
python3 scripts/gen_figure.py -t bar -d data.json -o figure.tiff --dpi 300 --theme lancet

# Horizontal bar chart with ratio annotations + GLM palette (GLM-5.2 blog style)
python3 scripts/gen_figure.py -t hbar -d throughput.json -o perf.png --theme glm \
  --show-ratio --title "Throughput Improvement" --xlabel "Normalized Throughput"

# Bar chart with hatching patterns (print-friendly, colorblind-safe)
python3 scripts/gen_figure.py -t bar -d data.json -o hatch.png --theme okabe-ito \
  --hatch --show-values --title "ACR50 Response Rates"

# Multi-panel composite (Panel A+B+C, journal figure layout)
python3 scripts/gen_figure.py -t composite -d composite.json -o figure4.png --theme okabe-ito

# Architecture/flow diagram (research design, CONSORT-style)
python3 scripts/gen_figure.py -t diagram -d flow.json -o flow.png --theme glm --width 12 --height 6
```

## Chart Types

| Type | Command | Key Features |
|------|---------|-------------|
| Bar | `-t bar` | Grouped bars, error bars, significance brackets, hatching, ratio annotations |
| Horizontal Bar | `-t hbar` | Horizontal bars, ratio annotations |
| Stacked Bar | `-t stacked_bar` | Subgroup proportions, percentage labels, total annotations |
| Heatmap | `-t heatmap` | Cell annotations, custom colormap, colorbar |
| Scatter | `-t scatter` | Trend line, r value, color grouping, mean points |
| Line | `-t line` | Multiple series, error bands, markers |
| Dual Y-Axis | `-t dual_axis` | Two Y-axes, solid+dashed lines, combined legend |
| Box | `-t box` | Box-and-whisker, jitter points |
| Forest | `-t forest` | CI whiskers, weight bubbles, overall diamond, I², events/total |
| Kaplan-Meier | `-t km` | Step function, censor marks, log-rank test, risk table, median survival |
| ROC | `-t roc` | AUC, 95% CI, optimal cutoff, multi-model comparison |
| Violin | `-t violin` | Density estimation, inner mean/median |
| **Composite** | `-t composite` | Multi-panel (A+B+C), any chart type per panel, journal figure layouts |
| **Diagram** | `-t diagram` | Architecture/flow blocks, arrows, groupings, annotations |

## Color Themes

| Theme | Description | Colorblind Safe |
|-------|-------------|----------------|
| `okabe-ito` | Nature Methods gold standard (Wong 2011) | ✅ Yes |
| `nature` | NPG Nature journal palette | ❌ |
| `lancet` | Lancet medical palette | ❌ |
| `conservative` | Professional muted palette | ❌ |
| `default` | Balanced, versatile palette | ❌ |
| `glm` | Muted/elegant tech-blog palette (GLM-5.2 pixel-extracted) | ✅ Yes |

> **⚠️ Recommendation**: Use `--theme okabe-ito` for all submissions. Nature, Science, Cell, and most major journals now **require** colorblind-accessible figures. Red-green color schemes are a top rejection reason.

### Why Okabe-Ito?

The Okabe-Ito palette (`#E69F00, #56B4E9, #009E73, #F0E442, #0072B2, #D55E00, #CC79A7, #000000`) is the gold standard for colorblind-safe scientific visualization:
- Explicitly recommended by **Nature Methods** (Wong 2011, Nat Methods 8:441)
- Default in Wilke's "Fundamentals of Data Visualization"
- All 8 colors distinguishable under protanopia, deuteranopia, and tritanopia
- Visually vibrant — **no aesthetic compromise** vs. traditional palettes

## CJK / Chinese Support

Pass `--cjk` to auto-detect and load system CJK fonts. Zero manual configuration needed.

```bash
python3 scripts/gen_figure.py -t bar -d data.json -o fig.png --cjk
```

Font detection priority: Noto Sans CJK → PingFang → Microsoft YaHei → WQY → AR PL → Droid.

For custom font: `--cjk-font /path/to/font.ttf`

## Output Formats

| Format | Extension | DPI | Best For |
|--------|-----------|-----|----------|
| PNG | `.png` | 600 (default) | General use, presentations |
| SVG | `.svg` | Vector | Web, editable graphics |
| **PDF** | `.pdf` | Vector | **Journal submissions (preferred)** |
| TIFF | `.tiff` | 600 (override: `--dpi 300`) | Nature/Lancet photo requirements |
| EPS | `.eps` | Vector | Legacy journal requirements |

> **Tip**: Nature and Science prefer **PDF/EPS vector** for line art. Use `.pdf` or `.eps` extension.

### DPI Standards (2026)

| Content Type | Required DPI | How |
|-------------|-------------|-----|
| Line art (graphs, charts) | 600-1000+ | Default is 600; use `--dpi 1000` for strict journals |
| Photos / micrographs | 300-600 | Use `--dpi 300` |
| Mixed (graphs + photos) | 600 | Default |
| Vector (PDF/SVG/EPS) | N/A | Resolution-independent |

## Data Input

JSON (full features) or CSV (basic). See `references/data-formats.md` for complete schema per chart type.

**JSON bar chart example:**
```json
{
  "labels": ["Group A", "Group B"],
  "series": {"Treatment": [75, 82], "Control": [68, 70]},
  "errors": {"Treatment": [3, 2], "Control": [2, 1]},
  "significance": {"Treatment:0": "***", "Control:1": "NS"}
}
```

## Key Flags

| Flag | Description |
|------|-------------|
| `--title "text"` | Figure title. Supports `\n` for newline |
| `--xlabel`, `--ylabel` | Axis labels |
| `--width N`, `--height N` | Figure size in inches |
| `--format F` | Force output format: png, svg, pdf, tiff, eps |
| `--dpi N` | Override DPI for raster output |
| `--show-values` | Show numeric labels on bars |
| `--no-trend` | Hide trend line (scatter) |
| `--no-legend` | Hide legend |
| `--cmap NAME` | Colormap (heatmap) |
| `--vmin`, `--vmax` | Value range (heatmap) |
| `--horizontal` | Horizontal bar chart (alias: `-t hbar`) |
| `--hatch` | Add hatching patterns to bars (print-friendly, 10 patterns cycle) |
| `--show-ratio` | Show ratio annotations (e.g., "4.96x") on grouped bars |
| `--ratio-base N` | Base series index for ratio calculation (default: 0) |

## Accessibility & Alt Text

When submitting to journals, provide **alt text** for each figure describing what the figure shows. Example:
> "Bar chart showing Treatment group (mean 75, SD 3) vs Control group (mean 68, SD 2). Error bars represent standard deviation. Asterisks indicate statistical significance (p < 0.001)."

Springer Nature, NSF, and most major publishers require alt text for accessibility compliance.

## When Agent Generates Figures (Not CLI)

If creating a figure via Python script rather than CLI:

1. Always call `detect_cjk_font()` first if any label may contain CJK
2. Use `fontproperties=font_prop` on all text-setting calls with CJK content
3. Set `plt.rcParams['axes.unicode_minus'] = False` (prevents minus sign boxes)
4. **Use Okabe-Ito colors** for any multi-category plot
5. Verify output: file size > 20KB for multi-label charts indicates font loaded
6. Preferred output: **PDF** for submissions, PNG at 600 DPI for previews
7. **Hatching preference**: User prefers hatched/striped bar patterns (`--hatch`) for print-friendliness and visual distinction between series. Hatch lines use `_darken_color()` (darkened fill color) for guaranteed contrast on any fill. Do NOT manually override `edgecolor` when hatching is active — the `gen_bar` function handles it.
8. **White background mandatory**: This is a publication-quality figure generator for journal submissions. ALL output must use white background (`facecolor='white'`). Dark/black backgrounds are NEVER acceptable. Do not add dark themes or dark background options.

## Design Principles

1. **White background is non-negotiable.** This skill exists for journal submissions (Nature, Lancet, Science). `save_kwargs["facecolor"]` is hardcoded to `'white'`. Never add dark theme support.
2. **Hatching = darker lines on colored fill.** When `--hatch` is active, hatch lines are computed via `_darken_color(fc, 0.45)` — a darkened version of each bar's fill color. This guarantees visibility on any fill color without needing dark backgrounds.
3. **Okabe-Ito as default recommendation.** Always recommend `--theme okabe-ito` for colorblind safety. The `glm` theme is colorblind-safe too and suitable for tech blogs/presentations that still use white background.

## Negative Triggers (DO NOT trigger this skill for)

- SVG medical diagrams (→ medical-svg)
- Terminal/CLI charts (→ data-viz)
- Spectrogram/time-frequency (→ pywayne-plot)
- HTML slide presentations (→ html-presentation-restyler)
- Pure data analysis without visualization (→ data-analysis)

## File Structure

```
academic-figures/
├── SKILL.md                 ← English documentation (this file)
├── SKILL_ZH.md              ← Chinese documentation
├── scripts/
│   ├── gen_figure.py        ← Main generator (matplotlib+numpy)
│   └── detect_cjk_font.py   ← CJK font auto-detector
├── references/
│   ├── data-formats.md      ← JSON/CSV schema per chart type
│   ├── pitfalls.md          ← Common errors and white-bg rule
│   └── reverse-engineering-colors.md  ← Extract exact colors from reference images
```
```

## Version History

- **v1.5.0** (2026-06-17) — Added 3 new chart types: horizontal bar charts (hbar, with ratio annotations like "4.96x"), multi-panel composite figures (Panel A+B+C with GridSpec, any chart type per panel), architecture/flow diagrams (colored blocks, arrows, groupings, annotations); added GLM theme (muted/dusty palette pixel-extracted from GLM-5.2 blog: `#70A0D0` blue + `#D09050` orange); added bar hatching with BLACK lines on ALL bars (print-friendly, 9 patterns: `//`, `\\`, `||`, `--`, `++`, `xx`, etc.); added `--hatch`, `--show-ratio`, `--ratio-base`, `--horizontal` CLI flags; **white background mandatory** for all themes (publication standard); see `references/reverse-engineering-colors.md` for pixel extraction technique
- **v1.4.0** (2026-05-17) — Added 4 new chart types: Kaplan-Meier survival curves (log-rank test, risk tables, median survival, censor marks), ROC curves (AUC, 95% CI, optimal cutoff, multi-model comparison), stacked bar charts (compositional data, percentage labels), dual Y-axis line charts (clinical score + lab marker); expanded data validation for new types
- **v1.3.0** (2026-05-17) — Added Okabe-Ito colorblind-safe theme (Nature Methods standard); DPI upgraded 300→600 for line art; added PDF/TIFF/EPS output; enhanced forest plot (weight bubbles, I² heterogeneity, events/total, separator line); accessibility alt-text guidance; smart DPI by content type
- **v1.2.0** (2026-05-16) — Added version metadata, requires declaration, negative triggers, file structure docs
- **v1.1.0** — Added auto CJK detection, CSV long-format auto-conversion, empty data validation
- **v1.0.0** — Initial release: 7 chart types, 4 themes, CJK support, statistical annotations
