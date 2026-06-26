## Description: <br>
建筑工程标讯洞察-筑龙标事，当针对基建、大型工程进行追踪查询或寻找潜在参标单位时调用，优先使用潜在供应商推荐和临期项目接口，为建筑行业用户提供前瞻性建议。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pkuycl](https://clawhub.ai/user/pkuycl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External construction, procurement, and business-development users use this skill to search bids, inspect bid details, analyze companies and competitors, identify expiring projects, and summarize market opportunities through the Zhiliaobiaoxun API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bid keywords, company names, bid URLs, and related search parameters are sent to the third-party Zhiliaobiaoxun API. <br>
Mitigation: Use the skill only when that data sharing is acceptable, keep query scope narrow, and avoid submitting confidential or unauthorized business information. <br>
Risk: Company matching can broaden analysis across headquarters, subsidiaries, and branch entities. <br>
Mitigation: Ask the agent to confirm matched companies before broad headquarters or subsidiary analysis when precision matters. <br>
Risk: Project contact details may be retrieved or shared during company and bid analysis. <br>
Mitigation: Retrieve or disclose contact details only for legitimate, authorized business purposes. <br>
Risk: The skill requires the sensitive ZLBX_API_KEY credential. <br>
Mitigation: Provide the key through the configured environment variable and avoid pasting or exposing it in prompts, logs, or shared outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pkuycl/architecture-bid-insight-zhulongbiaoshi) <br>
- [Zhiliaobiaoxun API endpoint](https://mcp-server.zhiliaobiaoxun.com/api_v2/{工具名}) <br>
- [Zhiliaobiaoxun API key registration](https://ai.zhiliaobiaoxun.com/?ch=s34) <br>
- [标讯搜索类工具 API 详情](references/api-search.md) <br>
- [企业分析类工具 API 详情](references/api-company.md) <br>
- [市场分析类工具 API 详情](references/api-market.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown] <br>
**Output Format:** [Markdown narrative with JSON request examples and API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZLBX_API_KEY and sends bid keywords, company names, bid URLs, and related search parameters to the Zhiliaobiaoxun API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
