## Description: <br>
优惠券查询助手，当用户询问优惠、折扣、红包时调用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GeraldAlexanderrw](https://clawhub.ai/user/GeraldAlexanderrw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to query platform coupons, food-delivery red packets, and product-category discounts, with results sourced from a third-party coupon aggregation service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts a third-party coupon aggregation service and may show external coupon links. <br>
Mitigation: Install and use it only if that service contact and external coupon-link flow are acceptable for the user or organization. <br>
Risk: The skill can update itself when the user explicitly asks for an upgrade. <br>
Mitigation: Request upgrades only intentionally, and review the installed release before continued use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/GeraldAlexanderrw/getcoupon) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text with coupon summaries, platform names, coupon links, status messages, and retry or upgrade guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coupon availability is time-sensitive and results may include external links that must be opened in the relevant platform app.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
