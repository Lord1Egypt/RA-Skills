## Description:

Calculate how discounts affect revenue, margin, conversion assumptions, and allowable acquisition cost so teams can see whether a promotion is actually worth running.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce, growth, and merchandising teams use this skill to compare baseline and discount scenarios before launching promotions. It helps evaluate revenue, margin, break-even pressure, conversion uplift assumptions, refund effects, AOV changes, and CAC tolerance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discount and margin calculations may produce incorrect business guidance if formulas or assumptions are wrong.

Mitigation: Review generated Python formulas and scenario assumptions before using outputs for pricing, promotion, or budget decisions.

Risk: Commercial inputs may include sensitive revenue, cost, margin, conversion, refund, or acquisition-cost data.

Mitigation: Avoid entering unnecessarily sensitive internal financial data unless the agent session is approved for that data.

Risk: Some workflow prompts are in Chinese, which may affect reviewability for teams that do not read Chinese.

Mitigation: Confirm that users and reviewers understand the clarification prompts or translate them before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leooooooow/skills/discount-impact-calculator)
- [Output Template](references/output-template.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code]

**Output Format:** [Markdown with scenario analysis and reusable Python code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include baseline versus discount comparisons, margin and break-even implications, CAC changes, key risks, recommendations, and a reusable Python script.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
