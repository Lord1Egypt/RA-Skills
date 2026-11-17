## Description:

Calculate ecommerce break-even thresholds from price, cost, shipping, advertising, returns, and overhead assumptions so operators can make launch, hold, scale, or optimization decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce operators, marketers, and finance-adjacent teams use this skill to model contribution margin, break-even units, break-even CPA, break-even ROAS, discount impact, and sensitivity scenarios before launching or scaling products.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses sensitive ecommerce cost, margin, return, and advertising-performance inputs.

Mitigation: Use only approved agent environments for business data, minimize sensitive detail where possible, and avoid including credentials, customer personal data, or confidential source documents unless authorized.

Risk: Break-even output can be mistaken for formal accounting, tax, legal, valuation, cash-flow, or board-level finance work.

Mitigation: Treat results as decision-support analysis, and route formal finance, tax, legal, compliance, valuation, or board-reporting uses to qualified reviewers and authoritative systems.

Risk: Missing or low-confidence inputs can produce misleading launch, hold, scale, or optimization recommendations.

Mitigation: Label every assumption by confidence, run sensitivity analysis on uncertain inputs, and use the included model checklist before relying on the recommendation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leooooooow/skills/break-even-calculator-ecommerce)
- [Cost Breakdown Guide](artifact/references/cost-breakdown-guide.md)
- [Output Template](artifact/references/output-template.md)
- [Sensitivity Analysis Template](artifact/references/sensitivity-template.md)
- [Break-even Model Quality Checklist](artifact/assets/model-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown structured analysis with assumptions tables, unit-economics calculations, break-even results, sensitivity scenarios, and decision recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should show math explicitly, separate variable and fixed costs, label assumptions by confidence, and flag decision risks such as thin margins or uncertain inputs.]

## Skill Version(s):

1.1.0 (source: server release metadata, created 2026-03-30)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
