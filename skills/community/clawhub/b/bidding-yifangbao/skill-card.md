## Description: <br>
全网招中标分析助手 - 乙方宝。作为全网招中标分析助手，当用户需要查询招投标公告、分析中标结果或提炼企业画像时必须调用此技能。能够处理类似乙方宝平台的常见查询需求，重点输出结构化的标讯摘要和竞对关系分析，帮助用户简化投标前期的调研工作流。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business development teams use this skill to search tender notices, analyze winning bids, build company profiles, and identify competitors, buyers, suppliers, partners, contacts, pricing patterns, and renewal opportunities from Zhiliaobiaoxun/Yifangbao data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Zhiliaobiaoxun/Yifangbao API key. <br>
Mitigation: Use a dedicated ZLBX_API_KEY with appropriate account scope and avoid sharing it in prompts, logs, or public files. <br>
Risk: Queries may disclose procurement strategy, target company lists, or other sensitive business interests to the provider. <br>
Mitigation: Submit only queries that are acceptable to share with the provider and avoid confidential strategy details when they are not required. <br>
Risk: Returned contact names or phone data may be sensitive. <br>
Mitigation: Use contact data only for legitimate authorized business purposes and handle it according to applicable internal and legal requirements. <br>
Risk: Company-name matching can combine headquarters and subsidiaries, which may broaden the analysis scope. <br>
Mitigation: Specify exact legal entities when scope matters and review matched company lists before relying on the analysis. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liu-jiapeng/bidding-yifangbao) <br>
- [Zhiliaobiaoxun API Access](https://ai.zhiliaobiaoxun.com/?ch=s24) <br>
- [Zhiliaobiaoxun API Endpoint](https://mcp-server.zhiliaobiaoxun.com/api_v2/{工具名}) <br>
- [标讯搜索类工具 API 详情](references/api-search.md) <br>
- [企业分析类工具 API 详情](references/api-company.md) <br>
- [市场分析类工具 API 详情](references/api-market.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown analysis with structured summaries and JSON API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZLBX_API_KEY and may include tender, company, contact, price, and market-analysis data returned by the provider.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
