# Clinical Lab Parameter Trend Figure

> **何时读我**：临床检验指标趋势图（多次就诊数据）。
> **最短路径**：按「场景→命令」表直接取。
> **回 INDEX**：SKILL.md「文件索引与 30 秒路由」。

## When to Use

Case reports or case series showing longitudinal laboratory data (e.g., HLH diagnostic criteria tracking, treatment response monitoring). Standard in NEJM, Lancet, Blood, and pediatric rheumatology journals.

## The Pattern: N-Panel Grid, One Indicator Per Panel

**DO**: Each indicator gets its own panel with independent Y-axis.
**DON'T**: Put indicators with different magnitudes on the same Y-axis (CRP~200 vs Ferritin~1200 vs PLT~50 = unreadable).

### Layout Rules

| # Indicators | Grid | Example |
|-------------|------|---------|
| 2-3 | 1 row × N cols | (1,3) |
| 4-6 | 2 rows × 3 cols | (2,3) |
| 7-9 | 3 rows × 3 cols | (3,3) |

### Panel Anatomy (NEJM/Lancet Standard)

Each panel contains:
1. **Panel letter** (A, B, C...) as bold title, left-aligned
2. **Indicator English name** after letter: "A. WBC" or "A. Ferritin"
3. **Reference range shading**: light gray `axhspan()` between normal low and high
4. **Reference range lines**: dashed gray lines at normal limits
5. **Data line**: solid line with circle markers, Okabe-Ito color
6. **Value annotations**: numeric labels above each data point
7. **Unit on Y-axis**
8. **Hospital Day on X-axis** (D1, D2... or Day 1, Day 2...)
9. **No top/right spines**, light grid lines only

### Color Assignment (Okabe-Ito)

```python
COLORS = {
    'WBC':     '#E69F00',  # orange
    'Hb':      '#0072B2',  # blue
    'CRP':     '#D55E00',  # vermillion
    'PLT':     '#009E73',  # green
    '铁蛋白':   '#CC79A7',  # pink
    'D-二聚体': '#56B4E9',  # sky blue
    # Extend for more indicators using remaining Okabe-Ito colors
}
```

### Reference Ranges (Pediatric, 5 months)

These vary by age/sex/institution — always verify against the actual report:

| Indicator | Normal Range | Unit |
|-----------|------------|------|
| WBC | 4.3–14.2 | ×10⁹/L |
| Hb | 97–183 | g/L |
| CRP | <10 | mg/L |
| PLT | 183–614 | ×10⁹/L |
| Ferritin | 4.63–204.00 | ng/mL |
| D-dimer | 0.00–0.50 | μg/mL |
| Fibrinogen | 2.00–4.00 | g/L |
| Triglycerides | 0.3–1.7 | mmol/L |

### Y-Axis Scaling

```python
# Include both data AND reference range in Y-axis range
all_vals = list(ys) + [ref_lo, ref_hi]
ymin = min(all_vals) * 0.85
ymax = max(all_vals) * 1.15
```

### Template Script Structure

```python
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

fig = plt.figure(figsize=(12, 9), facecolor='white', dpi=300)
gs = GridSpec(n_rows, n_cols, figure=fig, hspace=0.35, wspace=0.30)

for idx, (key, letter, eng_name) in enumerate(panels_info):
    ax = fig.add_subplot(gs[idx // n_cols, idx % n_cols])
    # 1. Reference range shading
    ax.axhspan(ref_lo, ref_hi, alpha=0.12, color='gray')
    ax.axhline(ref_hi, color='#AAA', ls='--', lw=0.8)
    ax.axhline(ref_lo, color='#AAA', ls='--', lw=0.8)
    # 2. Data line + markers
    ax.plot(xs, ys, '-o', color=color, ms=6, lw=2,
            markeredgecolor='white', markeredgewidth=1.2)
    # 3. Value annotations
    for x, y in zip(xs, ys):
        ax.annotate(f'{y:.1f}', (x, y), xytext=(0, 10), ha='center')
    # 4. Panel title
    ax.set_title(f'{letter}. {eng_name}', fontweight='bold', loc='left')
    # 5. Clean spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
```

## Pitfalls

1. **Never share Y-axis across magnitudes** — the user explicitly rejected a 4-panel figure that mixed CRP (200) and Ferritin (1200) with Hb (80) on the same axis. Each indicator MUST have its own panel.
2. **Unicode superscripts in CJK fonts** — `×10⁹/L` will produce "Glyph missing" warnings. Use `r'$\times$10$^9$/L'` (LaTeX math) or plain `10^9/L`.
3. **External lab results** may arrive on different days than local labs. Map everything to a common "Hospital Day" timeline, merging same-day results.
4. **Sparse data is OK** — a panel with only 1-2 data points (e.g., Ferritin measured twice) is valid and still informative with the reference range shading.
