## Description: <br>
稻哲纪烤羊排智能客服Skill。当用户询问关于稻哲纪烤羊排的任何信息时触发：包括营业时间、门店地址、招牌菜推荐、菜品介绍、价格、外卖配送、团购套餐、会员福利、停车、Wi-Fi等。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liubuq-sys](https://clawhub.ai/user/liubuq-sys) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External customers and restaurant staff use this skill to answer questions about 稻哲纪烤羊排 locations, hours, menu items, prices, delivery, group-buying offers, membership benefits, and dining policies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installers may add daily background updates. <br>
Mitigation: Prefer a manual, pinned install and remove or skip the cron or Scheduled Task auto-updater. <br>
Risk: Installation can overwrite an existing daozheji-grill skill directory. <br>
Mitigation: Back up any existing skill directory before installing or updating. <br>
Risk: Broad activation triggers may cause the skill to respond when the user does not clearly mean this restaurant. <br>
Mitigation: Narrow activation triggers so responses occur only for clear 稻哲纪烤羊排 restaurant requests. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liubuq-sys/daozheji-grill) <br>
- [门店基础信息](references/business-info.md) <br>
- [完整菜品库](references/services.md) <br>
- [团购套餐与优惠活动](references/promotions.md) <br>
- [专项FAQ](references/faq.md) <br>
- [品牌介绍](references/brand.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance] <br>
**Output Format:** [Natural-language conversational responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Depends on readable reference files for current restaurant facts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, CHANGELOG, version.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
