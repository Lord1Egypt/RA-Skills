## Description: <br>
Use when a user search Bing Shopping, find product or shopping results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn natural-language shopping searches into confirmed Dataify Bing Shopping API calls and return the API response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends shopping queries to Dataify and requires a Dataify API token. <br>
Mitigation: Use the skill only when sending the query to Dataify is acceptable, and provide tokens through a secure secret mechanism or temporary environment variable. <br>
Risk: Passing an API token with the documented --token command-line pattern can expose the token in shell history or process listings. <br>
Mitigation: Avoid command-line token arguments; prefer DATAIFY_API_TOKEN or a managed secret store. <br>
Risk: A live API call may use unintended request fields if parameters are inferred incorrectly. <br>
Mitigation: Review the generated parameter table and confirm it before any live API call. <br>


## Reference(s): <br>
- [Dataify Bing Shopping API Reference](references/api.md) <br>
- [Dataify API endpoint](https://scraperapi.dataify.com/request) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-bing-shopping) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown parameter tables, shell commands, and direct API response text or JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill requires user confirmation before live API calls and returns the script output directly.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
