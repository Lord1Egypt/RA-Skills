## Description: <br>
Analyzes stocks and cryptocurrencies using Yahoo Finance data, portfolio and watchlist tools, dividend checks, stock scoring, trend detection, and rumor scanning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run stock and crypto analysis, compare tickers, track portfolios and watchlists, review dividends, scan market trends, and detect early rumor signals. Outputs are informational and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional X/Twitter social scanning handles AUTH_TOKEN and CT0 session cookies and can expose broad local environment secrets to an external CLI. <br>
Mitigation: Use stock analysis, portfolio, watchlist, and hot scanning with --no-social by default; avoid supplying X/Twitter session cookies unless necessary, restrict .env file permissions, and use a dedicated low-risk account when social scanning is needed. <br>
Risk: BUY, HOLD, SELL, rumor, and impact-scoring outputs can be mistaken for trading advice. <br>
Mitigation: Treat all outputs as informational, review source data independently, and consult a licensed financial advisor before making investment decisions. <br>
Risk: Market, news, and social sources can lag, change format, be rate-limited, or return incomplete data. <br>
Mitigation: Cross-check important results against primary sources and prefer fast or no-social modes when external feeds are unreliable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yinwuzhe/skills/csig-skill-0625) <br>
- [Publisher profile](https://clawhub.ai/user/yinwuzhe) <br>
- [Skill README](artifact/README.md) <br>
- [Usage Guide](artifact/docs/USAGE.md) <br>
- [Hot Scanner Documentation](artifact/docs/HOT_SCANNER.md) <br>
- [Architecture Documentation](artifact/docs/ARCHITECTURE.md) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [CoinGecko](https://coingecko.com) <br>
- [Google News](https://news.google.com) <br>
- [bird CLI](https://github.com/steipete/bird) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, Markdown guidance, JSON reports, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local portfolio, watchlist, cache, and optional .env-backed social-scanner state.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence); artifact frontmatter reports 6.2.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
