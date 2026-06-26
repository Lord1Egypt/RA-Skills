## Description: <br>
Fetch scheduled upcoming economic events and data releases from FMP API for specified date ranges with impact assessment in chronological markdown format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and market analysts use this skill to fetch upcoming economic calendar events from the FMP API and turn them into chronological markdown reports with impact notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: FMP API keys can be exposed if durable credentials are passed directly on the command line. <br>
Mitigation: Prefer providing FMP_API_KEY through a secret or environment mechanism and avoid logging command invocations that contain credentials. <br>
Risk: Packaged metadata does not exactly match the registry identity. <br>
Mitigation: Verify the ClawHub publisher handle, page URL, and release version before deployment. <br>


## Reference(s): <br>
- [Economic Calendar Fetcher Zc on ClawHub](https://clawhub.ai/lean-zhouchao/economic-calendar-fetcher-zc) <br>
- [Publisher profile: lean-zhouchao](https://clawhub.ai/user/lean-zhouchao) <br>
- [FMP Economic Calendar API Documentation](references/fmp_api_documentation.md) <br>
- [Financial Modeling Prep Economic Calendar API](https://financialmodelingprep.com/api/v3/economic_calendar) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown reports, JSON event data, and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an FMP API key; date ranges are limited to 90 days by the API documentation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
