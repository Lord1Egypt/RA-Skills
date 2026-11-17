# Value measurement rules

## Indicator tree

```text
business goals
└── Business outcome metrics (what ultimately changed)
├── User task indicators (whether work is improved)
├── Adoption metrics (who continues to use)
├── Technical/quality indicators (whether the solution is reliable)
└── Risk and cost indicators (expenses and negative impacts)
```## Indicator definition card```markdown
- Indicator name:
- Decision-making purposes:
- Definition/Formula:
- Numerator/denominator:
- Baseline/Target:
- Crowd and time window:
- Data source and owner:
- Possible deviations:
- Evidence status: Customer confirmed / FDE inferred / Pending verification / Not supported
```

## Baseline and Control

Prioritize the use of historical data of the same process before POC; secondly use batch launch, similar teams or similar task comparison. When it is impossible to establish a comparison, use before-and-after comparison and identify confounding factors such as season, personnel, policy and business volume changes.

Don’t just compare average results “with AI” and “without AI”; break down the differences by user, task difficulty, and human review.

## Cost and ROI

Total costs include at least: model/API, infrastructure, integrations, data preparation, manual review, training, support, operations, security compliance, and error/incident expected costs.

```text
Net revenue = Recognizable revenue – Total incremental costs
ROI = Net Benefit / Total Incremental Cost
```

When benefits cannot be monetized, unit task cost, time, quality, risk, or capacity changes are reported without imposing a dollar amount.

## Prevent over-attribution

- Whether the metric change preceded adoption;
- Whether there are any changes in processes, personnel, policies, business volume or systems during the same period;
- Whether the value comes from only a few expert users;
-Whether the labor cost has been omitted;
- Whether negative results and non-adopting populations are excluded;
- Whether the customer business leader agrees with the metric definition and conclusion.
