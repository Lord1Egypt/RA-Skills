## Description: <br>
美团优惠券 helps users search nationwide Meituan coupons for chain brands by brand name or category keyword, returning coupon listings sorted by sales volume. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-shopping](https://clawhub.ai/user/cn-shopping) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to find brand, restaurant, beverage, snack, retail, and local-service coupons that are advertised as usable nationwide across supported Chinese cities. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Coupon search terms are sent to the skill publisher's Tencent Cloud proxy. <br>
Mitigation: Use only non-sensitive brand or category search terms, and avoid entering personal details, account information, precise private locations, or unrelated text. <br>
Risk: Coupon results can include referral purchase links. <br>
Mitigation: Review the destination, merchant details, coupon terms, and final checkout price before purchasing. <br>
Risk: Live coupon availability, price, and city coverage can change after results are returned. <br>
Mitigation: Confirm that the coupon is still available and valid for the intended location before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cn-shopping/skills/brand-coupons) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text with coupon entries, prices, images, pagination hints, and referral purchase links.] <br>
**Output Parameters:** [1D; keyword is required and page is optional.] <br>
**Other Properties Related to Output:** [Filters for coupons available in at least 50 cities and sorts displayed results by sales volume.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
