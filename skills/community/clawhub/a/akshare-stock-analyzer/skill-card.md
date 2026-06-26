## Description: <br>
Akshare-Stock-Analyzer helps agents fetch A-share stock or ETF market data and produce short-term technical trend, signal, score, and risk summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YuanfuC](https://clawhub.ai/user/YuanfuC) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze A-share stocks and ETFs from natural-language requests, including intraday snapshots, recent daily trends, buy/sell/hold signals, scores, and technical risk context. The output is technical reference material only and is not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches public market data through external providers, so network errors, provider outages, or delayed data can affect analysis quality. <br>
Mitigation: Run it in a controlled Python environment, handle fetch failures explicitly, and avoid presenting results when upstream data cannot be retrieved. <br>
Risk: Buy, sell, hold, score, and risk outputs may be mistaken for investment advice. <br>
Mitigation: Present outputs as short-term technical reference only and remind users to combine them with fundamentals, news, position sizing, and personal risk tolerance. <br>
Risk: The release includes Python scripts and unpinned third-party dependencies. <br>
Mitigation: Review the scripts before execution and install dependencies in a virtual environment before running setup_env.py. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/YuanfuC/akshare-stock-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/YuanfuC) <br>
- [README.en.md](artifact/README.en.md) <br>
- [README.md](artifact/README.md) <br>
- [AnalysisResult field reference](artifact/scripts/analyze_result.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Concise Markdown or plain text with optional JSON-like analysis fields and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include trend, weekly_change_pct, today_change_pct, signal, score, moving-average context, MACD, RSI, reversal hints, and risk level.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
