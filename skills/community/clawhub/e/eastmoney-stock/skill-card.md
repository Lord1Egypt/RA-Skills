## Description: <br>
Retrieves Chinese-language stock quotes, price changes, volume, and market ranking information for stock-related questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongchun2008](https://clawhub.ai/user/dongchun2008) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to answer stock-market lookup questions, including individual quotes, gainers and losers, sector rankings, and watchlist-style summaries. Outputs are for informational market-data convenience, not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market quotes or rankings may be delayed, unavailable, or inaccurate for time-sensitive decisions. <br>
Mitigation: Treat results as informational and verify important prices or rankings with a trusted market-data source. <br>
Risk: Queried stock symbols may be sent to Eastmoney and Sina Finance services. <br>
Mitigation: Avoid using the skill for sensitive watchlists or private trading intent that should not be shared with third-party data providers. <br>
Risk: Users may interpret stock lookup output as financial advice. <br>
Mitigation: Present the output as market-data convenience only and avoid recommendations to buy, sell, or hold securities. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dongchun2008/eastmoney-stock) <br>
- [Eastmoney quote API endpoint](http://push2.eastmoney.com/api/qt/clist/get) <br>
- [Eastmoney market grid](http://quote.eastmoney.com/center/gridlist.html) <br>
- [Sina Finance](http://finance.sina.com.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style text reports and JSON-like helper-script responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Market data may be delayed by a few minutes and should be verified before important decisions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
