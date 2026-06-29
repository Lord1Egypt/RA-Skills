## Description: <br>
AI 招投标分析师用自然语言调度知了标讯招中标数据接口，生成商机研判、市场洞察、竞对画像和投标决策分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business development, bidding, procurement sourcing, and market analysis users can use this skill to search tender and award data, analyze buyers and suppliers, profile companies, identify competitors, and produce structured opportunity reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically register a device, send local device and user identifiers, and save an API key when no API key is already configured. <br>
Mitigation: Prefer manually setting ZLBX_API_KEY; allow automatic registration only after explicit consent to identifier collection and local key storage. <br>
Risk: The skill can generate login or recharge links when quota is exhausted. <br>
Mitigation: Review links before opening them and use the publisher's normal account or billing flow when automatic login is not appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhiliaobiaoxun/skills/ai-tender-bid-analyst) <br>
- [Bid Search API Reference](references/api-search.md) <br>
- [Company Analysis API Reference](references/api-company.md) <br>
- [Market Analysis API Reference](references/api-market.md) <br>
- [Automatic Registration Flow](references/auto-register.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown analysis reports with structured summaries and JSON API request/response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ZLBX_API_KEY or a locally stored API key to query external tender, company, and market-analysis APIs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
