## Description: <br>
全国招标采购信息一站式查询与分析助手，帮助用户搜索招标、中标和采购公告，分析企业招投标活动、竞争对手、市场趋势、价格记录和潜在商机。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, procurement teams, sales teams, market analysts, and developers use this skill to query Chinese bidding and procurement data, inspect company bidding history, identify buyers and suppliers, compare competitors, and summarize market or price signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can auto-register a device-linked account by sending local device identifiers to zhiliaobiaoxun.com and storing an API key in ~/.zlbx/config.json. <br>
Mitigation: Prefer manually configuring a dedicated ZLBX_API_KEY; use auto-registration only after reviewing the account, device, and credential-storage implications. <br>
Risk: The skill may generate an auto-login recharge link when an automatically registered key has no remaining quota. <br>
Mitigation: Review payment and account-binding implications before following recharge links; use manually managed keys where account control is required. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/zhiliaobiaoxun/skills/china-national-bidding-zhongguozhaobiao) <br>
- [API overview](SKILL.md) <br>
- [Bidding search API reference](references/api-search.md) <br>
- [Company analysis API reference](references/api-company.md) <br>
- [Market analysis API reference](references/api-market.md) <br>
- [Automatic registration flow](references/auto-register.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown summaries with JSON request examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call zhiliaobiaoxun.com APIs and may persist an API key in ~/.zlbx/config.json when auto-registration is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
