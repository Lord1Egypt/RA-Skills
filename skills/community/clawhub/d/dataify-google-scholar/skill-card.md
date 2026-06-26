## Description: <br>
Turns a user's Google Scholar request into a Dataify Scraper API call after confirming request parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare and run Google Scholar searches through Dataify, including parameter parsing, pre-call confirmation, token handling, and direct return of the API response body. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a Dataify API token and documents a token-passing pattern that can expose credentials. <br>
Mitigation: Prefer DATAIFY_API_TOKEN from a session-scoped environment or secret manager, avoid echoing tokens, and do not pass tokens in reusable shell history when alternatives are available. <br>
Risk: Incorrect or unintended query parameters can change the Google Scholar request sent to Dataify. <br>
Mitigation: Review the generated parameter table carefully and require explicit confirmation before every API call. <br>


## Reference(s): <br>
- [Dataify Google Scholar API Reference](references/google_scholar_api.md) <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-google-scholar) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify Scraper API endpoint](https://scraperapi.dataify.com/request) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Markdown parameter table, shell command examples, and direct API response body] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Dataify API token; asks for user confirmation before making live API calls.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
