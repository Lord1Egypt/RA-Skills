## Description:

Alibaba ecosystem shopping assistant. Input a buying need or product link; choose between Taobao, Tmall, and 1688, compare platform fit, seller trust, visible price, MOQ, returns, and authenticity risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping assistants use this skill to compare Alibaba ecosystem platforms, evaluate sellers, estimate visible prices and discounts, and prepare purchase guidance while keeping payment and final order submission under user control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags a mismatch between the advertised no-login boundary and skill behavior that can use logged-in shopping sessions for cart, coupon, address, and order-preview actions.

Mitigation: Require clear user consent before any logged-in shopping action, show the effect of each action before proceeding, and keep payment and final order submission user-controlled.

Risk: Cart, coupon, address, and order-preview operations may expose account-level shopping data or change the user's shopping state.

Mitigation: Use public pages whenever possible, avoid collecting credentials or payment details, stop for CAPTCHA or identity checks, and ask the user to verify prices, stock, coupons, delivery, and after-sales terms before purchase.

## Reference(s):

- [Alibaba Shopping Assistant on ClawHub](https://clawhub.ai/harrylabsj/skills/alibaba-shopping)
- [Browser Workflow for Alibaba Shopping](references/browser-workflow.md)
- [Platform Guide](references/platform-guide.md)
- [Store Types Guide](references/store-types.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown with comparison tables, shopping guidance, and optional browser command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product comparisons, seller trust signals, price breakdowns, coupon notes, logistics notes, and user-controlled checkout handoff instructions.]

## Skill Version(s):

2.1.0 (source: server release evidence, package.json, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
