## Description: <br>
Automatically track tech company financial reports and generate investment summaries. Supports retrieving earnings calendars, market expectation comparisons, key metric interpretation, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to track earnings dates, compare EPS and revenue expectations with available market data, and generate Markdown summaries for portfolio or company review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial summaries and recommendations may be incomplete, stale, or unsuitable as the sole basis for investment decisions. <br>
Mitigation: Treat outputs as informational and verify the ticker, reporting period, data source, and current company filings before acting. <br>
Risk: The skill makes outbound requests for public market and earnings data, which can be delayed, incomplete, unavailable, or rate limited. <br>
Mitigation: Run it only where outbound public finance-data requests are allowed, and review any Data Unavailable or retrieval-error output before relying on the report. <br>


## Reference(s): <br>
- [Financial Report Tracker API Reference](references/api_reference.md) <br>
- [yfinance Library](https://pypi.org/project/yfinance/) <br>
- [Financial Modeling Prep API](https://site.financialmodelingprep.com/developer/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports with tables and command-line usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include ticker-specific earnings dates, EPS and revenue comparisons, metric summaries, and informational recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
