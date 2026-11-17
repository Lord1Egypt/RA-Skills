## Description:

Fetch professional stock market data from Yahoo Finance (yfinance) and SEC EDGAR for quotes, historical prices, financial statements, company profiles, filings, XBRL concepts, insider transactions, options chains, dividends, earnings, analyst recommendations, and news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1shadow1](https://clawhub.ai/user/1shadow1)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to retrieve market data and SEC filing information for equity research and financial due diligence. It helps agents produce commands and structured data lookups for public company analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A SEC filing command can fetch an arbitrary URL rather than only SEC filing pages.

Mitigation: Use read-filing only with URLs returned by the skill's SEC filings command, and prefer patching or policy controls that restrict it to SEC archive URLs before deployment.

Risk: Market data and filings may be delayed or incomplete for time-sensitive financial decisions.

Mitigation: Treat outputs as research inputs, confirm critical data against authoritative sources, and avoid relying on the skill as the sole basis for trading or compliance decisions.

## Reference(s):

- [ClawHub finance-data skill page](https://clawhub.ai/1shadow1/skills/finance-data)
- [SEC company tickers data](https://www.sec.gov/files/company_tickers.json)
- [SEC EDGAR full-text search API endpoint](https://efts.sec.gov/LATEST/search-index)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands call Yahoo Finance through yfinance and SEC EDGAR endpoints; read-filing output is capped by the requested max character limit.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
