## Description: <br>
Turns a user's Google Local, nearby search, or place search request into a Dataify Scraper API form POST. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare and run Dataify Google Local searches with a pre-call parameter preview and explicit confirmation before API execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local search terms and possible location details are sent to Dataify/Google Local when the API call is approved. <br>
Mitigation: Review the pre-call confirmation table carefully and avoid submitting sensitive personal locations or private search terms. <br>
Risk: The skill requires a sensitive Dataify API token. <br>
Mitigation: Use a dedicated Dataify API token where possible and avoid echoing credentials in conversation or logs. <br>
Risk: Users who do not read Chinese may miss details in the confirmation prompt or generated table. <br>
Mitigation: Review each field name, current value, default, and description before confirming the request. <br>


## Reference(s): <br>
- [Dataify Google Local API](artifact/references/google_local_api.md) <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-google-local) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API response] <br>
**Output Format:** [Markdown parameter previews and raw API response bodies, typically JSON or HTML depending on the requested output mode.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Dataify API token and explicit user confirmation before live API calls.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
