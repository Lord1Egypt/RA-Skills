## Description: <br>
This skill turns a user's Google Trends request into a confirmed Dataify Scraper API form submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert natural-language Google Trends requests into validated Dataify API parameters, confirm the request, and call the bundled helper script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confirmed Google Trends query parameters are sent to Dataify. <br>
Mitigation: Use the skill only when sending those parameters to Dataify is acceptable, and review the pre-call confirmation table before approving the request. <br>
Risk: API tokens may be exposed if pasted into chat or command history. <br>
Mitigation: Prefer the DATAIFY_API_TOKEN environment variable and avoid passing tokens directly in conversation or command-line arguments when possible. <br>
Risk: Example values or undocumented defaults could produce an unintended query. <br>
Mitigation: Ask for missing required parameters and rely on the reference document or preview helper for defaults before calling the API. <br>


## Reference(s): <br>
- [Dataify Google Trends API Reference](references/google_trends_api.md) <br>
- [Dataify API endpoint](https://scraperapi.dataify.com/request) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-google-trends) <br>
- [Publisher profile](https://clawhub.ai/user/dataify-server) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown confirmation table, shell command invocation, and raw API response body] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before API calls and returns the API response body without summarizing or reshaping it.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
