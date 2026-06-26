## Description: <br>
Connects to the Baselight MCP server to discover and query 50+ premium dataset sources and run live SQL queries against structured data from AI tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pjsousa79](https://clawhub.ai/user/pjsousa79) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers, analysts, and AI-tool users use this skill to connect an agent or IDE to Baselight, discover relevant structured datasets, inspect schemas, and run SQL queries that return results with the SQL used. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Query text and dataset-discovery requests are sent to the Baselight remote service. <br>
Mitigation: Use the skill only when that sharing is intended, and avoid sending secrets, private documents, or regulated personal data unless approved. <br>
Risk: Baselight authentication credentials may be exposed or overused if reused broadly. <br>
Mitigation: Use a revocable Baselight credential and rotate or revoke keys when access is no longer needed or exposure is suspected. <br>
Risk: Query limits and dataset freshness can affect result completeness or timeliness. <br>
Mitigation: Inspect schemas and dataset context first, scope queries carefully, include the SQL used, and explain assumptions in returned results. <br>


## Reference(s): <br>
- [Baselight MCP connection documentation](https://baselight.ai/docs/connecting-to-the-baselight-mcp-server/) <br>
- [Baselight app](https://baselight.app) <br>
- [ClawHub skill page](https://clawhub.ai/pjsousa79/baselight-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with SQL snippets, MCP connection details, query results, and troubleshooting notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include live SQL, result summaries, assumptions, and dataset-discovery guidance; query limits and dataset freshness vary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
