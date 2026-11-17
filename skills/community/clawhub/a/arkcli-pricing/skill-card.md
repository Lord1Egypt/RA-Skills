## Description:

查询火山引擎 ARK 基础模型的当前账号结算单价，以及 AgentPlan / CodingPlan 套餐订阅价格。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to look up current ARK foundation-model usage prices and AgentPlan or CodingPlan subscription prices, then explain returned prices, units, and account discounts accurately.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner notes that a model-selection example could affect billing or quota.

Mitigation: Confirm the intended model and possible billing or quota impact before running a model-selection example.

Risk: The audio-pricing guidance is contradictory and could lead to inaccurate pricing answers.

Mitigation: Resolve the audio-pricing instructions against current ARK pricing documentation, and report only returned charge items with their units and currency.

## Reference(s):

- [arkcli-pricing-models.md](artifact/references/arkcli-pricing-models.md)
- [arkcli-pricing-plans.md](artifact/references/arkcli-pricing-plans.md)
- [ClawHub release page](https://clawhub.ai/jasonstarlight/skills/arkcli-pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown pricing explanations with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports only pricing items returned by the current query, with their units and applicable model or plan details.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
