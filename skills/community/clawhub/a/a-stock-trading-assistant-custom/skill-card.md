## Description: <br>
A Stock Trading Assistant Custom helps agents answer China mainland A-share market questions with real-time quotes, individual stock analysis, market sentiment, hot-sector tracking, trading strategy guidance, and price alert support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[c595390153-a11y](https://clawhub.ai/user/c595390153-a11y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to analyze China mainland A-share stocks, market indexes, sector momentum, and trading scenarios. It is intended to support market research and decision preparation, not to replace independent financial judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock codes and market queries may be sent to public third-party finance sites. <br>
Mitigation: Use the skill only when that disclosure is acceptable, and avoid entering sensitive portfolio context unless needed. <br>
Risk: Configured price alerts can persist locally in a watchlist file. <br>
Mitigation: Review or delete the watchlist when alerts are no longer needed. <br>
Risk: Market data and generated trading guidance may be incomplete, delayed, or unsuitable for a user's circumstances. <br>
Mitigation: Verify data independently and treat outputs as decision support rather than financial advice. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/c595390153-a11y/a-stock-trading-assistant-custom) <br>
- [Stock Analysis Reference](references/analysis.md) <br>
- [Data Sources Reference](references/data-sources.md) <br>
- [Sina Finance Quotes API](http://hq.sinajs.cn/list=sh600519) <br>
- [Eastmoney Quote API](http://push2.eastmoney.com/api/qt/stock/get?secid={market}.{code}&fields=f43,f44,f45,f46,f47,f48,f57,f58,f60,f107,f169,f170,f171,f530) <br>
- [Tonghuashun Quote Endpoint](https://d.10jqka.com.cn/v4/time/hs_{code}/today.js) <br>
- [Xueqiu](https://xueqiu.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with tables, structured analysis, optional shell commands, and optional JSON from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stock and market data should include source attribution and fetch time when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
