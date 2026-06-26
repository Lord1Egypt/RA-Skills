## Description: <br>
Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio management, watchlists and alerts, dividend analysis, stock scoring, viral trend detection, and rumor or early-signal detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze public market tickers and crypto assets, compare securities, manage local portfolios and watchlists, review dividend metrics, and scan for trending or early market signals. Outputs should support research and monitoring, not replace professional financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Twitter/X integration can require live session credentials such as auth_token and ct0. <br>
Mitigation: Leave social scanning disabled unless needed; if enabled, store credentials outside shared repositories, protect and rotate them, and avoid granting broad browser or disk permissions. <br>
Risk: The skill makes network requests for analyzed tickers, portfolio entries, market data, news, SEC data, crypto data, and optional social signals. <br>
Mitigation: Use the skill only when those requests are acceptable for the assets being reviewed, and prefer --fast or --no-social modes when enrichment is unnecessary. <br>
Risk: Portfolio and watchlist data are stored locally and may contain sensitive financial interests. <br>
Mitigation: Keep local portfolio and watchlist files out of synced folders and source repositories, and apply normal local file protections. <br>
Risk: Financial market data and rumor signals may be delayed, incomplete, or misleading. <br>
Mitigation: Treat results as research inputs, verify material facts against authoritative sources, and do not use outputs as sole investment advice. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yinwuzhe/0602-tosr2-06) <br>
- [Publisher profile](https://clawhub.ai/user/yinwuzhe) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [README](README.md) <br>
- [Usage Guide](docs/USAGE.md) <br>
- [Hot Scanner Guide](docs/HOT_SCANNER.md) <br>
- [Architecture](docs/ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text, with optional JSON output from scanner scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run local Python scripts through uv, write local portfolio and watchlist JSON files, and make network requests to market, news, SEC, crypto, and optional social data sources.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata); artifact frontmatter reports 6.2.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
