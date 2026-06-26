## Description: <br>
Analyze Chinese stock prices (A-shares, HK stocks) and provide investment recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cs995279497-byte](https://clawhub.ai/user/cs995279497-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to summarize public market data and recent context for A-share, Hong Kong, and US-listed stocks. It produces structured stock analysis with buy, hold, or sell-oriented guidance and a risk disclaimer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated buy, hold, or sell suggestions may be incorrect, incomplete, or unsuitable for a user's financial situation. <br>
Mitigation: Treat output as informal market analysis only and do not rely on it as the sole basis for investment decisions. <br>
Risk: Users may disclose sensitive brokerage credentials, account details, or private financial records while asking for analysis. <br>
Mitigation: Do not provide brokerage credentials or private financial records; use only public market information. <br>


## Reference(s): <br>
- [Popular Chinese Stocks Reference](references/china-stocks.md) <br>
- [Eastmoney](https://www.eastmoney.com) <br>
- [Xueqiu](https://xueqiu.com) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [Google Finance](https://www.google.com/finance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown stock-analysis report with tables, technical commentary, recommendation guidance, and risk disclaimer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public market information gathered by the agent; no executable code, credential access, or persistence is indicated by security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
