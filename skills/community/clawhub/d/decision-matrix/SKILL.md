---
name: decision-matrix
slug: decision-matrix
description: "Multi-factor weighted decision matrix with sensitivity analysis for hard choices."
---

# Decision Matrix

Use this skill when the user faces a complex choice with multiple options and wants a systematic, quantified framework to evaluate trade-offs, test assumptions, and reach a defensible decision.

## Good triggers

- "I need to choose between two job offers — help me decide."
- "Which car should I buy? Evaluate options quantitatively."
- "Decide between renting and buying a home."
- "Compare software vendors for my team."
- "Should I relocate to City A or City B?"
- "Help me make a structured decision about my career path."

## Workflow

1. **List options.** Ask the user for 3-5 alternatives. If more than 5, suggest pre-filtering to the top contenders.

2. **Define criteria.** Ask the user to list the dimensions that matter for this decision. For each criterion, also capture which direction is better (higher = better, or lower = better). Examples: salary, commute time, growth potential, work-life balance, cost.

3. **Weight criteria (1-10).** Ask the user to assign importance weight to each criterion. Normalize to sum-to-100 percentages for clarity. Optional: flag criteria weighted > 9 as potential dealbreakers.

4. **Score each option per criterion (1-10).** Ask the user to rate each option against each criterion. If a criterion has objective data, suggest the score (e.g., salary in RMB scaled to 1-10).

5. **Compute weighted scores.** Calculate:
   ```
   WeightedScore(option) = Σ( score(option, criterion_i) × weight_i )
   ```
   Display as a heatmap:
   | Option | Criterion 1 (w=30%) | Criterion 2 (w=20%) | ... | Total |
   |--------|---------------------|---------------------|-----|-------|
   | A      | 8                   | 6                   |     | 7.2   |
   | B      | 5                   | 9                   |     | 6.8   |

6. **Sensitivity analysis.** For each criterion, vary the weight by ±20% and re-rank:
   - If the #1 option changes under any ±20% weight shift, flag as **unstable**
   - Report the "stress test" — which criteria cause the most rank volatility
   - Identify the **tipping point**: what weight change would flip rank 1 and 2

7. **Identify key differentiators.** Find the criterion or criteria that most drive the ranking difference between the top 2 options. These are the "swing factors" the user should examine most carefully.

8. **Deliver decision report.** Structure:
   - **Summary** — top-ranked option with total score
   - **Heatmap table** — original scores and weighted totals
   - **Sensitivity analysis** — stability flag, tipping point if any
   - **Key differentiators** — the 1-2 criteria separating the leaders
   - **Recommendation** — ranked list with rationale per option
   - **Caveats** — assumptions made, data gaps, subjective scores flagged

## Sample prompt

```
decision-matrix evaluate --options "Offer A,Offer B,Offer C" --criteria "薪资:8,发展空间:9,稳定性:6"
```
