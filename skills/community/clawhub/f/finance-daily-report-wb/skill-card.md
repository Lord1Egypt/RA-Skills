## Description: <br>
Generates an interactive HTML daily finance report for A-shares, Hong Kong stocks, major indices, sectors, capital flows, forex, commodities, news, and upcoming market events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch public market data and generate a local, browser-viewable daily finance report. It is suited for market overview requests, daily financial summaries, and Chinese-market style visual reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install Python dependencies and contact public market-data providers through AKShare. <br>
Mitigation: Use a virtual environment and run it in an environment where package installation and outbound market-data requests are permitted. <br>
Risk: Generated reports load Chart.js from a CDN when opened. <br>
Mitigation: Review the generated HTML or replace the CDN dependency before use in environments with strict network or dependency controls. <br>
Risk: Market data can be incomplete or unavailable, especially for current-day real-time data and upstream provider outages. <br>
Mitigation: Treat the report as informational, check source data when accuracy matters, and rely on the built-in graceful degradation indicators for missing modules. <br>
Risk: Finance summaries may be mistaken for investment advice. <br>
Mitigation: Present the report as market information only and preserve the report disclaimer that data does not constitute investment advice. <br>


## Reference(s): <br>
- [AKShare API Reference for Finance Daily Report](references/akshare_apis.md) <br>
- [Finance Daily Report HTML Template Notes](assets/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Interactive HTML report file with Markdown guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated HTML report is local and self-contained except for Chart.js, which is loaded from a CDN when opened.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
