## Description:

Track stock and crypto portfolios with CLI - real-time prices, P&L, dividend tracking, multiple portfolios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsoutar](https://clawhub.ai/user/rsoutar)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage local stock and crypto portfolios, check live prices and profit/loss, track dividends, manage multiple portfolios, and export portfolio data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional web UI exposes unauthenticated endpoints that can read or change locally stored financial records if the server is reachable.

Mitigation: Use the web UI only as a local personal tracker, avoid network exposure, and add authentication plus loopback binding before using it with sensitive records.

Risk: Price and dividend lookups send ticker symbols to Yahoo Finance and CoinGecko.

Mitigation: Use only ticker data you are comfortable sharing with those services, and apply local network controls where required.

Risk: Portfolio records are stored locally and may contain sensitive financial information.

Mitigation: Protect the local data directory with appropriate filesystem permissions and avoid running the skill on shared or untrusted machines.

Risk: CSV export can carry malformed or spreadsheet-interpreted values if exported data is opened in office tools.

Mitigation: Review CSV exports before sharing and add CSV escaping before relying on exports for sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rsoutar/skills/claw-portfolio)
- [Publisher profile](https://clawhub.ai/user/rsoutar)
- [CoinGecko API endpoint](https://api.coingecko.com/api/v3)
- [Yahoo Finance chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands, terminal text, local JSON storage, and CSV export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local portfolio files and optional web UI endpoints; price and dividend lookups may call Yahoo Finance and CoinGecko.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
