## Description:

比货全网商品对比工具，从价格、品质、评价、返利等多维度对比同类商品，帮助用户做出最优购买决策。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to compare similar products across price, quality, ratings, rebates, sales, brand reputation, and after-sales factors before making purchase decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Chinese shopping-comparison triggers could activate the skill during adjacent purchase discussions.

Mitigation: Use scoped trigger phrases and confirm that the user wants a product comparison before producing buying guidance.

Risk: Shopping recommendations may be misleading when product prices, ratings, rebate rates, or availability are outdated or incomplete.

Mitigation: State when current marketplace data is unavailable and ask the user to provide product links or recent prices before ranking options.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangshan101-coder/skills/bihuo)
- [ClawHub publisher profile](https://clawhub.ai/user/fangshan101-coder)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown shopping comparison report with ranked recommendations and concise analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language consumer shopping comparison guidance]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
