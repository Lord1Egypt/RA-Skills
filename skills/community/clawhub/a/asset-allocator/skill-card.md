## Description:

资产配置师 helps agents draft lifecycle-based asset allocation plans, periodic investment schedules, and rebalancing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lj22503](https://clawhub.ai/user/lj22503)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create educational asset allocation examples based on age, risk tolerance, investment horizon, available assets, periodic investing, and rebalancing rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce actionable investment plans, including fund names, percentages, automatic-investing suggestions, and rebalancing instructions.

Mitigation: Treat outputs as educational examples only and require independent review for math, taxes, fees, jurisdiction, liquidity needs, loss tolerance, and suitability.

Risk: The calculator can recommend allocating more money than the user has.

Mitigation: Check that total allocation amounts do not exceed available assets before using any generated plan.

## Reference(s):

- [资产配置参考](references/allocation-theory.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands]

**Output Format:** [Markdown guidance with tables, examples, JSON-like structures, and optional Python calculator output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Educational investment-planning output may include fund names, allocation percentages, rebalancing actions, and periodic investment amounts.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
