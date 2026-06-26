## Description: <br>
This skill helps agents query Jianyu/Zhiliaobiaoxun bidding data for tender search, company analysis, market aggregation, price trends, and potential bidder recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liu-jiapeng](https://clawhub.ai/user/liu-jiapeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement, sales, market intelligence, and bid teams use this skill to find tender opportunities, analyze buyers and suppliers, compare competitors, inspect company bidding activity, and summarize market trends from Jianyu/Zhiliaobiaoxun data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Procurement searches and returned contact details can include sensitive business information. <br>
Mitigation: Avoid submitting confidential strategy or non-public deal information, and treat returned contact information as sensitive business contact data. <br>
Risk: The skill requires a ZLBX_API_KEY and sends procurement queries to the Jianyu/Zhiliaobiaoxun service. <br>
Mitigation: Install only if you trust the service for these searches, and use a dedicated API key with appropriate access controls. <br>
Risk: Broad company-name matching can mix related entities when a user needs exact-company results. <br>
Mitigation: Ask for exact-company searches when entity scope matters, especially for legal, competitive, or account-specific analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liu-jiapeng/bidding-search-jianyu) <br>
- [Jianyu API service](https://mcp-server.zhiliaobiaoxun.com/api_v2/{tool_name}) <br>
- [Jianyu API key portal](https://ai.zhiliaobiaoxun.com/?ch=s23) <br>
- [Bid search API reference](references/api-search.md) <br>
- [Company analysis API reference](references/api-company.md) <br>
- [Market analysis API reference](references/api-market.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, api calls, guidance] <br>
**Output Format:** [Markdown summaries, tables, query plans, and API request guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ZLBX_API_KEY for authenticated third-party API requests and emphasizes clear tables or charts for data analysis.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
