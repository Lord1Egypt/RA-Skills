## Description: <br>
Analyze stocks and cryptocurrencies using Yahoo Finance data. Supports portfolio management, watchlists with alerts, dividend analysis, 8-dimension stock scoring, viral trend detection (Hot Scanner), and rumor/early signal detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run command-line stock and cryptocurrency analysis, compare tickers, track portfolios and watchlists, inspect dividend metrics, and scan trending or rumor-driven market signals. Outputs are informational and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Twitter/X scanning can require powerful browser session tokens or copied AUTH_TOKEN and CT0 values. <br>
Mitigation: Use --no-social when Twitter/X data is not needed; keep .env out of shared folders and source control, restrict file permissions, and remove or rotate tokens after use. <br>
Risk: Market, news, rumor, short-interest, and filing data may be delayed, incomplete, cached, or rate-limited. <br>
Mitigation: Treat outputs as informational research, verify important results against primary sources, and consult a licensed financial advisor before making investment decisions. <br>
Risk: Portfolio and watchlist features store user-entered holdings and alert data in local files. <br>
Mitigation: Avoid entering sensitive account details, protect the local data directory, and review stored JSON files before sharing logs or workspaces. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/0602-tosr2-01) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [CoinGecko](https://coingecko.com) <br>
- [SEC EDGAR](https://www.sec.gov/edgar) <br>
- [Google News](https://news.google.com) <br>
- [bird CLI](https://github.com/steipete/bird) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with optional JSON output from the included scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Some commands read live market, news, SEC, CoinGecko, Yahoo Finance, or optional Twitter/X data; portfolio and watchlist commands write local JSON files.] <br>

## Skill Version(s): <br>
6.2.0 (source: artifact SKILL.md frontmatter); ClawHub release version 1.0.1 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
