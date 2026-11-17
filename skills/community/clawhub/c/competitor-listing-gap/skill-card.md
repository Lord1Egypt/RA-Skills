## Description:

Compares a primary ASIN with authorized competitors across product-page fields, images, and review evidence to identify Listing gaps and verifiable improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and marketplace operators use this skill to compare their product listing with authorized competitors and identify evidence-based opportunities to improve listing expression.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This release also exposes ongoing paid monitoring, and some actions described as quote-only can spend credits.

Mitigation: Prefer a corrected package that enforces the comparison-only scope before connecting a funded ARI account. If using this version, require confirmation for every charge, use explicit quote commands, choose manual collection for one-time work, and review recurring monitoring plans; omitting --confirm does not reliably prevent spending.

## Reference(s):

- [Operation workflow](references/operation-workflow.md)
- [ARI CLI and API reference](references/reference.md)
- [ARI Operations](https://ari.funewa.com/zh/operations)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, Guidance]

**Output Format:** [Markdown comparison report with evidence and improvement suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are grounded in available listing and review data; the skill does not assess live prices, sales, inventory, orders, or actual return rates.]

## Skill Version(s):

1.5.3 (source: server-resolved release metadata, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
