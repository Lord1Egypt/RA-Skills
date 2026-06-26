## Description: <br>
Prepares Dataify builder requests for TikTok scraper tools rooted at tiktok_comment_by-url, including tool selection, parameter collection, and curl command generation for scraperapi.dataify.com/builder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare Dataify builder calls for TikTok scraper workflows. It helps collect tool parameters, normalize saved option labels, and produce a curl request that can be run against the Dataify builder endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated curl commands can expose DATAIFY_API_TOKEN if pasted into chats, logs, screenshots, backups, or synced shell history. <br>
Mitigation: Keep the token in a secret manager or session-scoped environment variable, redact Authorization headers before sharing output, and avoid storing generated commands in persistent profiles or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-tiktok-comment-by-url) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify builder endpoint](https://scraperapi.dataify.com/builder) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated requests require a DATAIFY_API_TOKEN environment variable and user-supplied scraper parameter values.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
