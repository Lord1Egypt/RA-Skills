## Description: <br>
Retrieve and cite U.S. and international economic time-series data such as GDP, inflation, unemployment, and interest rates from the FRED database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simonpierreboucher02](https://clawhub.ai/user/simonpierreboucher02) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to answer economic data questions by selecting appropriate FRED series, retrieving observations through a configured FRED MCP server, and returning cited, numerically faithful summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a sensitive FRED API key configured outside the skill. <br>
Mitigation: Keep FRED_API_KEY only in the MCP server environment and never request, echo, log, or include it in agent output. <br>
Risk: The generic FRED passthrough tool can reach any FRED endpoint. <br>
Mitigation: Use it only for economic time-series data and validate endpoint names, parameters, units, and dates before reporting results. <br>
Risk: FRED data can be delayed, revised, or unsuitable for live trading questions. <br>
Mitigation: Cite each value with series ID, observation date, retrieval date, and URL, and route live market quotes, financial advice, or forecasts to more appropriate sources. <br>


## Reference(s): <br>
- [FRED API documentation](https://fred.stlouisfed.org/docs/api/fred/) <br>
- [Endpoints and tools reference](reference/endpoints.md) <br>
- [Series IDs, units, and frequency reference](reference/series-and-units.md) <br>
- [Response fields reference](reference/response-fields.md) <br>
- [Best practices reference](reference/best-practices.md) <br>
- [Citation generation prompt](prompts/citation-generation.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, API calls, configuration] <br>
**Output Format:** [Markdown guidance with structured tool-call patterns and citation templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured FRED MCP server with FRED_API_KEY kept in the server environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
