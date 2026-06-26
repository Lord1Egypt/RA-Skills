## Description: <br>
Fetches free stock quotes and company news for US, Hong Kong, and China A-share symbols using Yahoo, Finnhub, Tencent, EastMoney, and optional AkShare data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antaeus001](https://clawhub.ai/user/antaeus001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retrieve market quotes and company news for US, Hong Kong, Shanghai, and Shenzhen equities from free external finance data providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock symbols, company names, and news queries are sent to external finance data providers. <br>
Mitigation: Use the skill only for queries that may be shared with Yahoo, Finnhub, Tencent, EastMoney, and optional AkShare-backed services. <br>
Risk: Tencent quote requests use HTTP transport. <br>
Mitigation: Avoid sending sensitive queries through that provider path and prefer HTTPS-backed providers when transport confidentiality is required. <br>
Risk: FINNHUB_API_KEY and proxy environment variables affect outbound requests. <br>
Mitigation: Configure API keys and proxies only in trusted environments and limit proxy scope to the intended agent process where possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/antaeus001/free-stock-global-quotes-news) <br>
- [Finnhub](https://finnhub.io) <br>
- [Yahoo Finance](https://finance.yahoo.com/) <br>
- [Yahoo Finance chart API](https://query1.finance.yahoo.com/v8/finance/chart) <br>
- [EastMoney Push2 quote API](https://push2.eastmoney.com/api/qt/stock/get) <br>
- [Tencent quote endpoint](http://qt.gtimg.cn/q={t_code}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown text or JSON emitted by Python command-line scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Quote output may include symbol, company name, currency, price, previous close, day change, and change percentage; news output may include headline, source, timestamp, summary, and URL.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
