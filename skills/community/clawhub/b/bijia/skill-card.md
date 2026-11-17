## Description:

全网商品比价工具，一键对比淘宝京东拼多多抖音等各平台同款商品价格，结合优惠券和返利计算真实最低到手价。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill before purchasing to compare prices, coupons, rebates, and price history across major Chinese commerce platforms and identify the lowest estimated final price.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad shopping and price-comparison triggers may activate the skill when the user did not intend to start a purchase workflow.

Mitigation: Review trigger terms before deployment and narrow them if accidental activation would disrupt normal shopping or research conversations.

Risk: Price, coupon, rebate, and purchase recommendations may be incomplete or stale at buying time.

Mitigation: Independently verify final seller price, coupon eligibility, rebate terms, shipping, and return conditions before purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangshan101-coder/skills/bijia)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown price-comparison report with ranked platform prices and a purchase recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include listed price, coupon and rebate assumptions, price history, savings estimate, and recommendation rationale.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
