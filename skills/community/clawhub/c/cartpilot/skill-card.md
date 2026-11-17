## Description:

Checkout-path optimization skill for mainland China shopping and local-delivery scenarios that decides whether to split orders, which coupons or threshold discounts are worth using, whether to favor the lowest total price, the smoothest checkout, or the fastest arrival, and outputs the optimal ordering path across Taobao, Tmall, JD, PDD, VIPSHOP, Meituan, elm, and similar platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use CartPilot to turn cart, coupon, threshold, fee, ETA, and budget details into decision-ready checkout plans. It compares the lowest total price, lowest-friction, and fastest-arrival routes while leaving login, coupon claiming, order submission, and payment to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checkout recommendations may affect purchases or expose private shopping details if the user shares sensitive account information.

Mitigation: Use only cart, coupon, fee, ETA, and screenshot details the user is comfortable sharing; keep login, coupon claiming, order submission, and payment under user control.

## Reference(s):

- [CartPilot ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/cartpilot)
- [CartPilot README](README.md)
- [CartPilot Release Notes](RELEASE.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, analysis]

**Output Format:** [Markdown with checkout plans and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a final call, lowest total price plan, lowest-friction plan, fastest-arrival plan, tradeoff explanation, and next step.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
