## Description: <br>
权威采招政策与标讯指南-元博网，当用户查询大型基础设施项目、重点政企采购或需要基于标讯进行宏观趋势盘点时调用，需调用聚合与分析接口，输出格式严谨、数据翔实的市场简报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pkuycl](https://clawhub.ai/user/pkuycl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and procurement analysts use this skill to search bid notices, analyze companies, identify market trends, and produce structured procurement market briefs from Yuanbowang/Zhiliaobiaoxun data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a ZLBX_API_KEY and sends company names, bid terms, filters, and related research queries to Yuanbowang/Zhiliaobiaoxun. <br>
Mitigation: Install only when third-party API use is acceptable, keep the API key in the configured environment variable, and avoid submitting sensitive queries unless authorized. <br>
Risk: Automatic company expansion can include related headquarters, branches, or subsidiaries in downstream analysis. <br>
Mitigation: For sensitive work, ask the agent to confirm matched legal entities before deep analysis or reporting. <br>
Risk: Company-contact and project-contact data may be returned during procurement analysis. <br>
Mitigation: Request or redistribute contact details only when there is a legitimate business reason. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pkuycl/authoritative-bid-policy-guide-yuanbowang) <br>
- [Yuanbowang API access](https://ai.zhiliaobiaoxun.com/?ch=s31) <br>
- [Bid search API reference](references/api-search.md) <br>
- [Company analysis API reference](references/api-company.md) <br>
- [Market analysis API reference](references/api-market.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown market briefs with structured API request examples and tabular procurement analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZLBX_API_KEY for read-only requests to the Yuanbowang/Zhiliaobiaoxun API; responses may include company contacts, bid details, market aggregates, and matched legal entities.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
