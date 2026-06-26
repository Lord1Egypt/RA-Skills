## Description: <br>
优惠券查询与领取技能，覆盖外卖券、酒店券、打车券、咖啡券、电影票、超市券等多场景，并根据用户需求匹配活动链接。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ayue-oss](https://clawhub.ai/user/ayue-oss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to match coupon, discount, and promotional-link requests against a bundled activity list for food delivery, travel, rides, coffee, movies, retail, and related scenarios. It can also return a Feishu form link for users who want to submit new coupon activities for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill returns third-party promotional links and an external Feishu submission form. <br>
Mitigation: Verify link destinations before opening them or entering information, and treat the submission form as an external site for voluntary coupon details. <br>
Risk: Coupon data may become stale or may not match a user's current eligibility, location, or platform account conditions. <br>
Mitigation: Confirm promotional terms on the destination platform before relying on the offer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ayue-oss/coupon-finder) <br>
- [Publisher profile](https://clawhub.ai/user/ayue-oss) <br>
- [Activity submission form](https://my.feishu.cn/share/base/form/shrcn4ERBYeALeE2cF8SMPIqHUE) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown-formatted text or JSON query results containing matching activity names, descriptions, tags, and promotional links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are ranked from a local bundled activity dataset and limited by the query limit parameter, defaulting to 5.] <br>

## Skill Version(s): <br>
1.0.5 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
