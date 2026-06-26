## Description: <br>
Use when the user asks to search DuckDuckGo or fetch DuckDuckGo results through Dataify. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to preview DuckDuckGo search parameters, call the Dataify DuckDuckGo Search API after confirmation, and return the API response to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and a Dataify API token may be sent to a third-party service. <br>
Mitigation: Install only when Dataify handling is acceptable, use a scoped token stored in a secret manager or environment variable, and avoid sensitive searches. <br>
Risk: The API call can run with user-provided search parameters and return raw service output. <br>
Mitigation: Preview the complete parameter table, obtain user confirmation before calling the API, and review returned content before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-duckduckgo-search) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify DuckDuckGo Search API endpoint](https://scraperapi.dataify.com/request) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, markdown, JSON, text] <br>
**Output Format:** [Markdown preview table followed by raw API stdout when confirmed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Dataify API token; search_assist cannot be sent with m, and m is clamped to 1..50.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
