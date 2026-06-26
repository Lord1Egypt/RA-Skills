## Description: <br>
A-share daily market analysis tool for market trends, sector rotation, capital flows, and hot-sector analysis, triggered by user questions about A-share行情,走势,分析,股市行情,今日A股,大盘分析, or 板块轮动. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FMouseBoy](https://clawhub.ai/user/FMouseBoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve Tavily-backed A-share market information and produce concise market, sector, funding-flow, hot-topic, and risk-summary reports. It is research support for market analysis, not a substitute for financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends A-share-related search terms to Tavily and requires a Tavily API key. <br>
Mitigation: Use a dedicated Tavily API key when appropriate and avoid entering sensitive holdings, account details, or proprietary research terms. <br>
Risk: Generated market analysis may be incomplete, stale, or unsuitable for investment decisions. <br>
Mitigation: Treat outputs as research support and verify market data and recommendations against authoritative financial sources before acting. <br>


## Reference(s): <br>
- [Tavily](https://tavily.com/) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>
- [ClawHub skill page](https://clawhub.ai/FMouseBoy/a-stock-investment) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, analysis, guidance] <br>
**Output Format:** [Markdown market analysis report with source listings from Tavily search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY and sends finance search queries to Tavily.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
