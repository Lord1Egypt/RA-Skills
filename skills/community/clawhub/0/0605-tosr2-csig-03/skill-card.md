## Description:

Analyze stocks and cryptocurrencies using Yahoo Finance data, portfolio tracking, watchlist alerts, dividend analysis, stock scoring, viral trend detection, and rumor or early-signal scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect stocks and cryptocurrencies, compare tickers, manage portfolios and watchlists, review dividend metrics, and scan for market trends or early signals. Outputs are informational and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional X/Twitter scanners handle browser session tokens and pass the full local environment to a third-party CLI.

Mitigation: Review before installation, avoid running in environments with cloud or CI credentials, and prefer --no-social unless X/Twitter data is specifically required.

Risk: Portfolio and watchlist data is stored locally in plaintext.

Mitigation: Use non-sensitive portfolio/watchlist data and restrict access to the local files and runtime environment.

Risk: The skill produces informational market analysis that can be incorrect, delayed, or incomplete.

Mitigation: Treat outputs as informational only and consult a licensed financial advisor before making investment decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yinwuzhe/skills/0605-tosr2-csig-03)
- [Publisher Profile](https://clawhub.ai/user/yinwuzhe)
- [Yahoo Finance](https://finance.yahoo.com)
- [Usage Guide](docs/USAGE.md)
- [Hot Scanner Guide](docs/HOT_SCANNER.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, console text, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May store portfolio and watchlist data locally in plaintext.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 6.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
