## Description: <br>
工程建设招投标分析-建设通，当搜索词包含工程、施工、建筑、市政、监理、设计等建筑业专属词汇时触发，聚焦工程项目金额、中标单位资质背景，重点提取建筑类项目核心字段并进行业绩汇总。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pkuycl](https://clawhub.ai/user/pkuycl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query Jianshetong/ZLBX tender APIs for construction procurement search, bid detail retrieval, company tender history, competitor analysis, and market intelligence. It is most useful when an agent needs structured summaries of project amounts, purchasing entities, winning bidders, qualifications, and related business opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive ZLBX_API_KEY for third-party API access. <br>
Mitigation: Use a dedicated limited API key, store it only in the agent environment, and rotate or revoke it if exposed. <br>
Risk: The API scope is broader than construction tender summaries and can query company contacts, market intelligence, and lead-generation data. <br>
Mitigation: Enable the skill only for workflows that need this broader procurement intelligence and require confirmation before contact lookups, company matching, or lead-generation queries. <br>
Risk: Submitting confidential strategy, deal terms, or sensitive business context to the third-party service may expose private information. <br>
Mitigation: Limit prompts and API parameters to the minimum tender, company, region, date, and product filters needed for the task. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pkuycl/construction-tender-analyzer-jianshetong) <br>
- [标讯搜索类工具 API 详情](references/api-search.md) <br>
- [企业分析类工具 API 详情](references/api-company.md) <br>
- [市场分析类工具 API 详情](references/api-market.md) <br>
- [ZLBX API key application page](https://ai.zhiliaobiaoxun.com/?ch=s33) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples and structured API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZLBX_API_KEY and calls third-party HTTP APIs; responses may include company, contact, tender, bid, and market intelligence data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
