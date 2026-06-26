## Description: <br>
Analyze Chinese stock prices (A-shares, HK stocks) and provide investment recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bingze00000](https://clawhub.ai/user/bingze00000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and finance-focused agent users can use this skill to request structured public-market commentary for Chinese A-share, Hong Kong, and selected US-listed stocks. The skill guides the agent to gather current public price and news context, summarize technical signals, and present buy, hold, or sell posture with a risk disclaimer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated buy, hold, or sell recommendations may be inaccurate, incomplete, stale, or unsuitable for a user's financial situation. <br>
Mitigation: Verify prices and news with trusted financial sources and treat the output as public-market commentary, not professional investment advice. <br>
Risk: Market data gathered through web search can vary by source, market hours, and reporting delay. <br>
Mitigation: Cross-check time-sensitive price, volume, and news facts against authoritative financial data sources before acting. <br>


## Reference(s): <br>
- [Popular Chinese Stocks Reference](artifact/references/china-stocks.md) <br>
- [Eastmoney](https://www.eastmoney.com) <br>
- [Xueqiu](https://xueqiu.com) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [Google Finance](https://www.google.com/finance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown stock-analysis report with tables, technical commentary, recommendation rationale, and risk disclaimer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public market data and news context gathered during the agent session; no code execution, credentials, persistence, or hidden system access is indicated by security evidence.] <br>

## Skill Version(s): <br>
1.0.1 (source: artifact _meta.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
