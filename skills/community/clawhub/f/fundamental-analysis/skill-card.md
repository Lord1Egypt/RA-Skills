## Description: <br>
A-share listed company fundamental analysis for key valuation, profitability, growth, financial health, peer comparison, and structured report output using East Money and 10jqka data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to prepare A-share stock due diligence, earnings review, valuation checks, industry comparisons, and investment memo drafts. It gathers financial data from named public finance sources, computes common ratios, and produces structured Markdown analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial analysis may be incomplete, stale, or unsuitable as a sole basis for investment decisions. <br>
Mitigation: Treat generated reports as decision support, verify figures against current primary filings or market data, and apply qualified financial review before acting. <br>
Risk: The skill depends on external finance websites and APIs whose availability, schemas, and terms can change. <br>
Mitigation: Check source availability and attribution at run time, and fall back to official filings or alternate data providers when fetched data is missing or inconsistent. <br>
Risk: Network fetching with curl or web tools can expose requests to third-party data providers. <br>
Mitigation: Review requested URLs before execution, avoid sending credentials or private portfolio data, and use the optional referer setting only when appropriate for the environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhaocaixia888/fundamental-analysis) <br>
- [East Money Data Center](https://data.eastmoney.com) <br>
- [East Money Securities Data API](https://datacenter.eastmoney.com/securities/api/data/v1/get) <br>
- [East Money F10 Financial Analysis](http://f10.eastmoney.com/cwfx.html?code=sh600519) <br>
- [10jqka Stock Overview](https://basic.10jqka.com.cn/600519/) <br>
- [CNINFO Disclosure Search](http://www.cninfo.com.cn/new/disclosure/stock?stockCode=600519) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports with tables, analysis notes, and optional code or command snippets for data gathering and ratio calculation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use curl and the optional EASTMONEY_REFERER environment variable when fetching East Money data.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
