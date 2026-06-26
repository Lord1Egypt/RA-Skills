# 8-Dimension Stock Scoring Model

## Dimensions

| # | Dimension | Weight | Source | Scoring |
|:--|:----------|:------:|:-------|:--------|
| 1 | **Valuation** | Equal | PE, PB, PS | PE<15→8, <25→6, <40→4, else→2 |
| 2 | **Growth** | Equal | Revenue & earnings growth | (earningsGrowth + revenueGrowth) * 10 + 5 |
| 3 | **Profitability** | Equal | Profit margins | profitMargins * 30 + 3 |
| 4 | **Momentum** | Equal | 1-month price return | >10%→8, >0%→6, >-10%→4, else→2 |
| 5 | **Stability** | Equal | Beta | <0.8→8, <1.2→6, <1.8→4, else→2 |
| 6 | **Dividend** | Equal | Dividend yield | yield * 200 + 1 |
| 7 | **Analyst** | Equal | Recommendation mean | 11 - rec * 2 |
| 8 | **Volume Health** | Equal | Volume vs average | 0.8-1.5x→8, <2x→6, else→4 |

## Grading

| Score | Grade |
|:------|:------|
| 65-80 | A+ |
| 55-64 | A |
| 48-54 | B+ |
| 40-47 | B |
| 32-39 | C+ |
| <32 | C |

All scores 1-10 per dimension. Total max = 80.
