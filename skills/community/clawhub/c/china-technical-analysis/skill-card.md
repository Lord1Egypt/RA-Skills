## Description: <br>
Compute and analyze technical indicators (MACD, KDJ, RSI, Moving Averages, Bollinger Bands) for Chinese futures markets. Generate buy/sell signals and chart descriptions based on data from china-commodity-quotes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to calculate technical indicators for Chinese futures contracts, interpret trend and momentum conditions, and produce buy, sell, or neutral technical-analysis guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External Sina Finance market data may be unavailable, delayed, or incomplete. <br>
Mitigation: Verify quote data against independent sources before relying on the analysis. <br>
Risk: Technical indicators and composite buy/sell signals can be misleading if treated as guarantees. <br>
Mitigation: Use outputs as technical-analysis context only, combine them with fundamentals and news, and make independent risk decisions. <br>


## Reference(s): <br>
- [China Technical Analysis on ClawHub](https://clawhub.ai/zhaocaixia888/china-technical-analysis) <br>
- [Sina Finance daily futures K-line API example](https://stock2.finance.sina.com.cn/futures/api/jsonp.php/InnerFuturesNewService.getDailyKLine?symbol=IF0&datalen=60) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown technical-analysis report with optional shell commands and Python helper output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Depends on quote data from china-commodity-quotes and external Sina Finance endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
