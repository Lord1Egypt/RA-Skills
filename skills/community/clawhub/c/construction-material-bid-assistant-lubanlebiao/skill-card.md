## Description: <br>
施工建材采招助手-鲁班乐标，当查询词包含建材、钢材、管材、机械或特定建筑材料型号时调用，必须调用价格趋势查询和Top品牌接口，输出建材历史单价和主要供应商名单。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thuanlynham-stack](https://clawhub.ai/user/thuanlynham-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and procurement analysts use this skill to query Lubanlebiao/ZLBX procurement data for construction materials, supplier discovery, bid searches, company analysis, brand rankings, and historical bid-price trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive ZLBX_API_KEY credential. <br>
Mitigation: Use a dedicated API key, store it only in the agent environment or approved configuration, and monitor quota usage. <br>
Risk: The skill can perform broader procurement intelligence, company contact lookup, competitor analysis, and lead-generation workflows beyond construction-material price lookup. <br>
Mitigation: Deploy it only for approved procurement-intelligence use cases and require user confirmation before expanding company searches or retrieving contact information. <br>
Risk: Procurement research may involve confidential or commercially sensitive topics. <br>
Mitigation: Avoid confidential procurement analysis unless approved by the organization responsible for the research. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thuanlynham-stack/construction-material-bid-assistant-lubanlebiao) <br>
- [Lubanlebiao/ZLBX API base](https://mcp-server.zhiliaobiaoxun.com/api_v2/{工具名}) <br>
- [ZLBX API key portal](https://ai.zhiliaobiaoxun.com/?ch=s35) <br>
- [api-search.md](references/api-search.md) <br>
- [api-company.md](references/api-company.md) <br>
- [api-market.md](references/api-market.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown or structured text summaries with API request examples and procurement-analysis guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ZLBX_API_KEY for authenticated read-only procurement API access.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
