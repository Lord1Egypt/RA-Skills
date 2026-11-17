## Description:

信用卡推荐帮助用户根据年费偏好、权益类型和卡等级筛选中信信用卡，并返回推荐理由、权益摘要、卡面图片和申请链接。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacky355](https://clawhub.ai/user/jacky355)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to clarify credit-card preferences and compare CITIC credit cards by fees, benefits, card level, card images, and application links. The recommendations are for product discovery and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credit-card recommendations may be mistaken for financial advice or complete eligibility guidance.

Mitigation: Treat the output as product discovery only and verify annual fees, eligibility, rates, and application terms on the bank's official pages before applying.

Risk: Application links include sid/platform parameters and route users to bank application pages.

Mitigation: Review the destination URL before opening or applying, and only continue if the user is comfortable sharing information with the bank application flow.

Risk: Recommendations depend on the current public card-data endpoint and may become incomplete if the endpoint changes.

Mitigation: Rerun the skill for fresh data and confirm important card benefits and terms on the official bank pages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jacky355/skills/credit-card-recommend)
- [Credit card API data reference](references/api_data.md)
- [CITIC credit card data endpoint](https://cs.citiccardcdn.citicbank.com/citiccard/cardshopcloud/eshop/appimg/cardshop/card/remain_first.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown recommendations and JSON card records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include card image URLs, benefit summaries, new-customer gift text, and bank application URLs with sid/platform parameters.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
