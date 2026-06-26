## Description: <br>
Analyze stocks and cryptocurrencies using Yahoo Finance data. Supports portfolio management, watchlists with alerts, dividend analysis, 8-dimension stock scoring, viral trend detection (Hot Scanner), and rumor/early signal detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze US stocks and cryptocurrencies, monitor portfolios and watchlists, review dividend metrics, and scan market, news, and social sources for trends or early signals. Outputs are informational and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional social scanning can require live X/Twitter session credentials. <br>
Mitigation: Prefer scans with --no-social unless social signals are required; use a throwaway account if credentials are used. <br>
Risk: Portfolio and watchlist commands persist local financial-tracking data. <br>
Mitigation: Review local state paths before use and avoid storing sensitive or unnecessary personal financial details. <br>
Risk: The skill queries external market, news, SEC, Reddit, and optional X/Twitter sources. <br>
Mitigation: Run it only in an environment where those network calls are acceptable and review outputs before acting on them. <br>
Risk: A .env file may be used for X/Twitter tokens. <br>
Mitigation: Keep .env out of repositories and do not place unrelated secrets in the same file. <br>
Risk: Financial analysis output may be incomplete, delayed, or misleading. <br>
Mitigation: Treat outputs as informational only and consult qualified financial advice before making investment decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yinwuzhe/0605-cisg-tosr2) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [CoinGecko](https://coingecko.com) <br>
- [SEC EDGAR](https://www.sec.gov/edgar) <br>
- [Google News](https://news.google.com) <br>
- [X](https://x.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text, with optional JSON output for scanner automation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist local portfolio and watchlist files and may query external market, news, SEC, Reddit, and optional X/Twitter sources.] <br>

## Skill Version(s): <br>
6.2.0 (source: SKILL.md frontmatter); ClawHub release 1.0.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
