## Description:

Analyzes stocks and cryptocurrencies with Yahoo Finance data, portfolio and watchlist tooling, dividend metrics, trend scans, and rumor or early-signal detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run command-line stock and crypto analysis, maintain local portfolios and watchlists, and produce informational market research reports. It is not financial advice and should be used as a decision-support input rather than an execution authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags optional X/Twitter integration because it can involve live browser session credentials and broad local browser access.

Mitigation: Use the no-social mode or isolate the environment; do not keep live session cookies in a project .env file, avoid broad Full Disk Access, and verify or pin the bird CLI before use.

Risk: Portfolio and watchlist workflows can store holdings data locally and send tickers or holdings-derived requests to finance and news services.

Mitigation: Store only data you are comfortable keeping on the local machine and sharing indirectly with market data providers; protect local files according to their sensitivity.

Risk: Market data, short interest, insider activity, and news signals can be delayed, cached, rate-limited, or incomplete.

Mitigation: Verify time-sensitive data against authoritative sources before acting and treat generated recommendations as informational support, not financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/aaaaa)
- [Publisher profile](https://clawhub.ai/user/yinwuzhe)
- [Yahoo Finance](https://finance.yahoo.com)
- [Usage guide](docs/USAGE.md)
- [Technical architecture](docs/ARCHITECTURE.md)
- [Hot Scanner documentation](docs/HOT_SCANNER.md)
- [Concept and philosophy](docs/CONCEPT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Console text and optional JSON, typically surfaced in Markdown with inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local portfolio and watchlist data; optional social scanning requires additional X/Twitter setup.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 6.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
