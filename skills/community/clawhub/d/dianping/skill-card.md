## Description:

Helps users use Dianping (大众点评) to compare restaurants, reviews, deals, and local lifestyle merchants in China using practical fit, review quality, friction, and risk signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to make Dianping-based local commerce decisions, including store comparison, review analysis, group-buy evaluation, and service merchant vetting.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Logged-in Dianping coupon or order pages may expose account, order, or payment-adjacent information.

Mitigation: Use logged-in pages only when intentionally needed for coupon or order review, and avoid sharing unrelated account or payment information.

Risk: Dianping ratings, reviews, and group-buy listings can be misleading when reviews are sparse, incentivized, outdated, or when deals include restrictions or hidden costs.

Mitigation: Ground recommendations in recent low- and mid-score reviews, review count, concrete complaints, deal constraints, and the user's stated scenario before ranking options.

## Reference(s):

- [Dianping skill instructions](SKILL.md)
- [Deals and Group-buy](references/deals.md)
- [Restaurant and Cafe Selection](references/restaurants.md)
- [Review Analysis](references/reviews.md)
- [Local Services and Entertainment](references/services.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown prose with concise decision labels, reasons, risks, and rankings when comparing options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May answer with Chinese decision templates for Dianping use cases]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
