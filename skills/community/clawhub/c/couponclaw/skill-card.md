## Description: <br>
Find verified coupons, compare cashback rates, and generate savings guidance for products and stores across China, the United States, the United Kingdom, Australia, Southeast Asia, and global direct-to-consumer brands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers and shopping agents use CouponClaw to search coupon and cashback sources, compare stacking options, and produce concise deal recommendations before checkout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad shopping triggers may route general shopping questions through a coupon and cashback lookup workflow. <br>
Mitigation: Invoke the skill explicitly for coupon, cashback, or daily-deal searches when broad routing is not desired. <br>
Risk: The skill asks an agent to open third-party coupon, cashback, and merchant pages based on user product or store queries. <br>
Mitigation: Use only non-sensitive shopping queries and review the extracted deals before relying on coupon codes, cashback rates, or final-price calculations. <br>


## Reference(s): <br>
- [CouponClaw on ClawHub](https://clawhub.ai/jiajiaoy/couponclaw) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with command examples and browser-navigation steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include coupon tables, cashback comparisons, source links, and final-price calculations in English or Chinese.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release metadata, package.json, README badge) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
