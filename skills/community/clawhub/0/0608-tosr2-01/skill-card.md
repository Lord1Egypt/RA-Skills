## Description: <br>
Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio management, watchlists, alerts, dividend analysis, stock scoring, trend scanning, and rumor detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run stock and crypto analysis workflows, inspect market trends, manage local portfolios and watchlists, and generate alerts or JSON outputs for follow-up decisions. The artifact states that outputs are informational and not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional X/Twitter social scanning may require AUTH_TOKEN and CT0 session cookies. <br>
Mitigation: Treat these values like account passwords, keep .env files out of source control, and use --no-social unless social scanning is needed. <br>
Risk: The skill contacts multiple third-party finance, news, crypto, SEC, and social data sources. <br>
Mitigation: Run it only in environments where those network calls are acceptable and review configured data sources before use. <br>
Risk: Portfolio, watchlist, and scan data may be stored locally. <br>
Mitigation: Avoid shared machines for sensitive portfolios and periodically inspect or delete local files under ~/.clawdbot/skills/stock-analysis. <br>
Risk: Financial analysis, rumor scoring, and market signals may be incomplete, delayed, or misleading. <br>
Mitigation: Use outputs for informational review only and verify important investment decisions with qualified financial advice and primary data sources. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/yinwuzhe/0608-tosr2-01) <br>
- [Yahoo Finance](https://finance.yahoo.com) <br>
- [Usage Guide](docs/USAGE.md) <br>
- [Hot Scanner](docs/HOT_SCANNER.md) <br>
- [Architecture](docs/ARCHITECTURE.md) <br>
- [Concept](docs/CONCEPT.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown-style guidance with shell commands, plus console text or JSON from Python scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local portfolio, watchlist, and scan/cache files under ~/.clawdbot/skills/stock-analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 6.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
