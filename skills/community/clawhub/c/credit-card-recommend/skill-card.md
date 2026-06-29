## Description: <br>
信用卡推荐技能会根据用户的用卡场景、年费偏好、权益类型和卡等级，从中信信用卡公开数据源筛选并推荐合适的信用卡。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacky355](https://clawhub.ai/user/jacky355) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to narrow credit-card choices by benefits, annual-fee preference, card level, and keywords, then receive concise Chinese recommendations with card images, benefits, and application URLs. Agents can also use it to guide unclear requests with clickable choice prompts before presenting recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Application links include channel/referral-style sid parameters and may include a coarse platform tag on recognized clients. <br>
Mitigation: Show the full bare application URL, make the parameters visible to the user, and let users decide whether to open the link. <br>
Risk: Credit-card fees, eligibility, benefits, and application terms can change after the public data feed is fetched. <br>
Mitigation: Advise users to review current card fees, terms, and bank disclosures before applying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jacky355/credit-card-recommend) <br>
- [CITIC credit-card data feed](https://cs.citiccardcdn.citicbank.com/citiccard/cardshopcloud/eshop/appimg/cardshop/card/remain_first.json) <br>
- [API data reference](references/api_data.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Chinese Markdown recommendations with optional JSON-backed results and bare application URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include card image URLs, benefits, new-customer gift text, and application URLs with disclosed sid and platform parameters.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
