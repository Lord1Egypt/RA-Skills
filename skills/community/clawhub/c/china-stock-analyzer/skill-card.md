## Description: <br>
Analyzes Chinese A-share stocks and ETFs by fetching public market data, calculating MA, MACD, and RSI indicators, and producing short-term trend, signal, score, and risk summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanfuc](https://clawhub.ai/user/yuanfuc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect short-term technical conditions for A-share stocks and ETFs, including intraday snapshots, recent daily trends, buy/sell/hold signals, 0-10 scores, and technical risk hints. The output is technical reference only and is not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock names or tickers may be sent to external public market-data providers. <br>
Mitigation: Use only symbols or names that are appropriate to share with those providers, and avoid sending confidential portfolio context. <br>
Risk: Dependency setup can install Python packages into the active interpreter. <br>
Mitigation: Run setup and analysis scripts in a virtual environment and review dependency installation before execution. <br>
Risk: Buy, sell, hold, score, and risk outputs are technical signals that may be incorrect, delayed, or incomplete. <br>
Mitigation: Treat outputs as technical reference, not investment advice, and combine them with independent research and user risk tolerance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanfuc/china-stock-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/yuanfuc) <br>
- [Sina Finance](https://finance.sina.com.cn) <br>
- [Sina real-time quote endpoint](https://hq.sinajs.cn/list={codes_str}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries and JSON-like analysis fields, with optional shell commands for bundled Python scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes trend, weekly_change_pct, today_change_pct, signal, score, MA/MACD/RSI context, reversal hints, and risk level when data is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
