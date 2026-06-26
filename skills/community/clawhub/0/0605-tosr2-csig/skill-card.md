## Description: <br>
Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio tracking, watchlist alerts, dividend analysis, multi-factor stock scoring, trend scanning, and rumor or early signal detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect equities and cryptocurrencies, compare tickers, monitor portfolios and watchlists, review dividend metrics, and surface market trends or early rumor signals. Outputs are informational and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can call external market and news services and optionally use X/Twitter session credentials. <br>
Mitigation: Use a dedicated account or safer API/OAuth flow, avoid shared .env files, and review the Bird CLI before enabling Twitter/X integration. <br>
Risk: Broadly loaded environment secrets may be forwarded to an external CLI. <br>
Mitigation: Keep unrelated secrets out of the skill environment and provide only the minimum credentials required for the selected command. <br>
Risk: Portfolio and watchlist commands can mutate local data files. <br>
Mitigation: Back up local portfolio and watchlist data before running mutation commands. <br>
Risk: Market data, social signals, and rumor scans can be delayed, incomplete, or misleading. <br>
Mitigation: Verify outputs against authoritative sources and treat results as informational rather than financial advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/0605-tosr2-csig) <br>
- [Publisher profile](https://clawhub.ai/user/yinwuzhe) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [CoinGecko](https://coingecko.com) <br>
- [CNN Fear and Greed Index](https://money.cnn.com/data/fear-and-greed/) <br>
- [SEC EDGAR](https://www.sec.gov/edgar) <br>
- [Google News](https://news.google.com) <br>
- [Twitter/X](https://x.com) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-style text, console output, and optional JSON from analysis scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read market and news data from external services and may write local portfolio or watchlist JSON files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
