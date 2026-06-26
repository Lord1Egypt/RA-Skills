## Description: <br>
Queries A-share stock quotes, K-line indicators, fund flows, financial data, ETF prices, Hong Kong company information, and macroeconomic data through a third-party HTTP API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wsyy002](https://clawhub.ai/user/wsyy002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to retrieve structured market, company, ETF, and macroeconomic data for market analysis, data backends, personal dashboards, AI trading assistants, and daily review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script silently uses a default token that differs from the documented trial token. <br>
Mitigation: Supply an explicit API key or token, prefer the documented header when possible, and review token handling before installing or running the script. <br>
Risk: Requests are sent to a third-party stock-data API that receives query parameters. <br>
Mitigation: Avoid sending confidential trading strategies or sensitive identifiers in requests, and review the service terms before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wsyy002/astock-api) <br>
- [A-Share Stock Data API homepage](https://api.jyfg.de5.net:2096) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured JSON API responses and formatted text summaries, with example curl and Python command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an API token; the bundled script includes a default token that differs from the documented trial token.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
