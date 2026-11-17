# Book-derived example fixtures

The fixtures under `assets/data/` transcribe numeric values printed in figures from Cole Nussbaumer Knaflic, *Storytelling with Data: A Data Visualization Guide for Business Professionals* (Wiley, 2015). Page numbers below refer to the printed book pages. The bundled charts are new implementations of the book's recommendations, not facsimiles of the book artwork.

## Included examples

| Fixture | Printed pages | Structure | Recommended treatment |
|---|---:|---|---|
| `employee_survey.csv` | 47-49 | Seven categories, two years | Slopegraph with endpoint labels; use color only for focal changes. |
| `category_heatmap.csv` | 42 | Six categories × three series | Sequential heatmap with cell values and a percent legend. |
| `tax_rates.csv` | 50-52 | Two category magnitudes | Bars on a zero baseline; the apparent difference must not be exaggerated by truncation. |
| `headcount_waterfall.csv` | 55-56 | Start, signed changes, end | Reconciled waterfall: 100 + 30 + 8 - 12 - 10 = 116. |
| `supplier_market_share.csv` | 62-64 | Four shares summing to 100% | Sorted horizontal bars instead of a pie chart. |
| `revenue_sales_staff.csv` | 66-68 | Two measures across eight quarters | Two aligned panels instead of a dual-axis chart. |

## Exact values

- Employee survey, 2014 to 2015: Peers 85 to 96; Culture 80 to 91; Work environment 76 to 75; Leadership 59 to 62; Career development 49 to 45; Rewards & recognition 41 to 42; Performance management 33 to 33.
- Heatmap rows Category 1 through Category 6, columns A/B/C: 15/22/42, 40/36/20, 35/17/34, 30/29/26, 55/30/58, 11/25/49 percent.
- Tax rates: 35.0% and 39.6%.
- Supplier shares: Supplier A 34%, B 31%, D 26%, C 9%.
- Revenue in millions across 2013 Q1 to 2014 Q4: 0.5, 0.6, 0.7, 0.9, 0.6, 0.6, 0.8, 1.0. Sales employees: 82, 91, 105, 112, 111, 109, 110, 110.

Use these fixtures to test layout and code paths. For a scientific result, replace them with the user's own source data and update the source note.
