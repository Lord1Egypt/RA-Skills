## Description: <br>
Fetches 18 financial indicators from CNBC, including macroeconomic, index ETF, and U.S. equity quotes, and stores them in a local SQLite database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loonslo](https://clawhub.ai/user/loonslo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance operators use this skill to refresh a local SQLite database with market indicators for monitoring, analysis, or downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence reports conflicts about whether the skill is CNBC-only and keyless or requires Finnhub credentials. <br>
Mitigation: Confirm the active data source and credential requirements before use; pass any required key via environment variable rather than command-line arguments or scheduled-job text. <br>
Risk: The skill writes finance data and logs to local storage and may be run on a schedule. <br>
Mitigation: Use explicit user-writable database and log paths, review retention and cleanup expectations, and enable scheduling only after confirming cadence and storage behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loonslo/fin-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/loonslo) <br>
- [CNBC SPY quote page](https://www.cnbc.com/quotes/SPY) <br>
- [Finnhub registration](https://finnhub.io/register) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output is console text plus SQLite database and log files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, a user-provided SQLite database path, and may use FINNHUB_API_KEY depending on the verified workflow.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
