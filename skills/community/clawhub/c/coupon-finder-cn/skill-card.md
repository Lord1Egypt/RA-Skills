## Description: <br>
Automatically discovers and helps claim e-commerce coupons for Taobao, JD.com, Pinduoduo, and Meituan before shopping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[275254cl-hash](https://clawhub.ai/user/275254cl-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and shopping assistants use this skill to look up available coupons, compare discount combinations, claim coupons, and check upcoming coupon expirations before buying from supported Chinese e-commerce platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask an agent to claim coupons or act on e-commerce accounts without clear per-action consent boundaries. <br>
Mitigation: Require explicit user confirmation before claiming coupons, opening account-specific links, or taking any action that changes account state. <br>
Risk: Coupon status, reminders, and historical comparisons may involve account-specific shopping data or retained coupon history. <br>
Mitigation: Clarify what data is stored, allow users to disable reminders or history tracking, and provide deletion controls for stored coupon data. <br>
Risk: Coupon recommendations or claim links may be affected by affiliate or CPS incentives. <br>
Mitigation: Disclose affiliate behavior and let users review the final merchant, price, discount stack, and checkout terms before purchase. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/275254cl-hash/coupon-finder-cn) <br>
- [Publisher profile](https://clawhub.ai/user/275254cl-hash) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown coupon search results, discount comparisons, claim links, reminders, and optional shell commands when the agent needs required tools.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require python3 and curl; results depend on public coupon data and actual checkout availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
