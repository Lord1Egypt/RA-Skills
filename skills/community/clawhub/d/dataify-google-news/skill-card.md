## Description: <br>
Turns a user's Google News request into a confirmed Dataify Scraper API form submission and returns the raw response body. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert Google News search requests into Dataify Scraper API parameters, preview and confirm the request, and execute the API call when a Dataify token is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API tokens may be exposed if users pass them directly on the command line or echo them in conversation. <br>
Mitigation: Prefer DATAIFY_API_TOKEN through agent or operating-system secret handling, and avoid repeating token values in user-facing output. <br>
Risk: Incorrect or unintended search parameters could trigger an unwanted external API call. <br>
Mitigation: Review the generated confirmation table and require explicit user confirmation before each real API call. <br>


## Reference(s): <br>
- [Dataify Google News API Reference](references/google_news_api.md) <br>
- [Dataify Scraper API endpoint](https://scraperapi.dataify.com/request) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-google-news) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown confirmation table followed by the raw Dataify API response body] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before real API calls and uses DATAIFY_API_TOKEN or an explicit token for authentication.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
