## Description: <br>
Collects Google Shopping product information by keyword through the Dataify Scraper API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to prepare and confirm Google Shopping keyword collection parameters, then create Dataify collection tasks through the Dataify Builder API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags unrelated Instagram Reel scraping trigger phrases in an otherwise Google Shopping-focused skill. <br>
Mitigation: Use the skill only for Dataify Google Shopping keyword collection and do not rely on it for Instagram Reel scraping. <br>
Risk: Token-handling examples can expose credentials more than necessary, especially when tokens are passed as command-line arguments. <br>
Mitigation: Prefer DATAIFY_API_TOKEN from the environment, avoid echoing tokens, and pass a user-provided token only after explicit confirmation. <br>
Risk: A real API call creates a Dataify collection task using submitted parameters. <br>
Mitigation: Review the Markdown confirmation table carefully and require explicit user approval before calling the API. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/dataify-google-shopping-keywords) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify Login](https://dashboard.dataify.com/login?utm_source=skill) <br>
- [Dataify Builder API Endpoint](https://scraperapi.dataify.com/builder?platform=1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown confirmation tables, inline shell commands, and JSON text from API helper responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before real API calls and uses DATAIFY_API_TOKEN or a user-provided token for authenticated requests.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
