## Description: <br>
Dataify Bing Images helps an agent prepare, preview, and, after user confirmation, send Bing Images search requests to the Dataify API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Use this skill when a user wants Bing image search results through Dataify, including parameter extraction from natural language, a complete request preview, user confirmation, and direct return of the API response. <br>

### Deployment Geography for Use: <br>
User-controlled agent runtime; the skill sends confirmed requests to Dataify's hosted API endpoint. <br>

## Known Risks and Mitigations: <br>
Risk: Passing a Dataify API token on the command line may expose it through shell history or process listings on some systems. <br>
Mitigation: Prefer providing the token through the DATAIFY_API_TOKEN environment variable or another secure environment mechanism. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-bing-images) <br>
- [Publisher profile](https://clawhub.ai/user/dataify-server) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown parameter preview tables, Python command invocations, API request configuration, and the raw Dataify API response text.] <br>
**Output Parameters:** [Search query, output format, market, country or region, offset, count, image size, color, image type, aspect, face filter, date filter, license filter, cache behavior, body format, timeout, and Dataify API token.] <br>
**Other Properties Related to Output:** [Requires user confirmation before a live API call and returns the script output directly without post-processing.] <br>

## Skill Version(s): <br>
1.1.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
