## Description:

Summarizes observable changes in authorized competitor product snapshots over supported daily or weekly periods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and market researchers use this skill to review authorized competitors' observable product snapshot changes over supported daily or weekly periods. It summarizes product fields such as price, ranking, rating, title, bullets, and images; it does not establish sales, inventory, advertising, orders, or actual return rates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server security evidence flags broader paid actions and conflicting assurances about charges and confirmation, so the declared watch-only scope and billing behavior need review.

Mitigation: Before authorizing monitoring, verify paid-action confirmation settings and recurring refresh costs; prefer a corrected watch-only release with enforced command restrictions and consistent billing instructions.

## Reference(s):

- [ARI Operations](https://ari.funewa.com/zh/operations)
- [ClawHub release page](https://clawhub.ai/funewa/skills/competitor-change)
- [Monitoring workflow](references/watch-workflow.md)
- [Monitoring reference](references/reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands]

**Output Format:** [Markdown summaries with observable product changes and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic snapshot comparisons; does not provide real-time monitoring or infer sales, inventory, advertising, orders, or actual return rates.]

## Skill Version(s):

1.5.3 (source: server release evidence, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
