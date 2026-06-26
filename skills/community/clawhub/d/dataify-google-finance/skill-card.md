## Description: <br>
This skill turns a user's Google Finance request for stocks, indices, funds, currencies, or futures into a confirmed Dataify Scraper API form POST. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare and run Google Finance searches through Dataify after reviewing the resolved request parameters and confirming the API call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A Dataify API token can be exposed if pasted into chat or reused in visible commands. <br>
Mitigation: Prefer DATAIFY_API_TOKEN in the environment, avoid echoing tokens in responses, and use --token only when the user explicitly supplies a token for the call. <br>
Risk: An unintended paid or uncached API request could be made if parameters are inferred incorrectly. <br>
Mitigation: Show the complete pre-call Markdown parameter table, ask the user to confirm or modify it, and only execute the API call after explicit confirmation. <br>


## Reference(s): <br>
- [Dataify Google Finance API](references/google_finance_api.md) <br>
- [Dataify Google Finance on ClawHub](https://clawhub.ai/dataify-server/dataify-google-finance) <br>
- [dataify-server publisher profile](https://clawhub.ai/user/dataify-server) <br>
- [Dataify Scraper API endpoint](https://scraperapi.dataify.com/request) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown confirmation tables, shell commands, and raw API response bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the Dataify API response body directly after user confirmation; token handling depends on DATAIFY_API_TOKEN or a supplied token.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
