## Description: <br>
Fetch professional stock market data from Yahoo Finance (yfinance) and SEC EDGAR for quotes, historical prices, company financials, filings, insider transactions, options, dividends, news, profiles, and equity research workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1shadow1](https://clawhub.ai/user/1shadow1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to retrieve market data, company fundamentals, SEC filings, XBRL concepts, and related equity research data through command-line helpers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The SEC filing reader can fetch arbitrary or untrusted filing URLs, including non-SEC and local file URLs. <br>
Mitigation: Use only HTTPS SEC EDGAR URLs from expected filing paths, do not pass untrusted URLs to read-filing, and prefer a patched version that enforces this restriction. <br>
Risk: Market data and filing-derived outputs can be delayed, incomplete, or outside the skill's intended scope when sourced from non-SEC URLs. <br>
Mitigation: Confirm material financial conclusions against authoritative market or SEC sources before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1shadow1/finance-data) <br>
- [SEC company tickers endpoint](https://www.sec.gov/files/company_tickers.json) <br>
- [SEC EDGAR full-text search endpoint](https://efts.sec.gov/LATEST/search-index) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON outputs from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Finance helper commands print JSON to stdout; filing text output may be truncated by max character settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
