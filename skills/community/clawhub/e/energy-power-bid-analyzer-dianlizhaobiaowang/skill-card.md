## Description: <br>
能源电力采招分析仪-电力招标网，当查询词包含电网、电力、新能源、光伏、储能、风电时触发，需重点针对国网/南网等大型央企采购项目进行聚合，分析特定能源设备或工程的中标集中度。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thuanlynham-stack](https://clawhub.ai/user/thuanlynham-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement, sales, and market-analysis users can query bid notices, company participation, supplier concentration, brand pricing, and expiring projects for energy and power-sector opportunities. The skill helps an agent call a third-party procurement API and summarize returned bid, company, contact, and market data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends procurement, company, product, market, and contact queries to a third-party API using ZLBX_API_KEY. <br>
Mitigation: Install only where that data sharing is acceptable, protect the API key as a sensitive credential, and avoid submitting confidential query terms unless approved. <br>
Risk: The documented tools include broader procurement and company analysis than the energy-power description suggests. <br>
Mitigation: Constrain use to intended energy and power-sector searches and review query scope before relying on results. <br>
Risk: Returned project contact data may be sensitive business information. <br>
Mitigation: Handle contact details under applicable privacy, outreach, and data-retention rules, and avoid unsolicited profiling or outreach. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thuanlynham-stack/energy-power-bid-analyzer-dianlizhaobiaowang) <br>
- [标讯搜索类工具 API 详情](references/api-search.md) <br>
- [企业分析类工具 API 详情](references/api-company.md) <br>
- [市场分析类工具 API 详情](references/api-market.md) <br>
- [ZhiLiaoBiaoXun API key portal](https://ai.zhiliaobiaoxun.com/?ch=s38) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API Calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZLBX_API_KEY and sends procurement, company, product, and market queries to a third-party service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
