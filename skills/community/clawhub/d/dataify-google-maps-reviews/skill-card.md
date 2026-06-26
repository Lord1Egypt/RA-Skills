## Description: <br>
Collects Google Maps review and comment information from Google Maps URLs by creating Dataify Scraper API tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare and submit Dataify tasks that collect Google Maps reviews from one or more Google Maps URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Maps URLs and task parameters are sent to Dataify when a collection task is created. <br>
Mitigation: Show the exact parameters before each real API call and submit only after the user confirms them. <br>
Risk: The skill uses a Dataify API token, and passing tokens on the command line can expose credentials in local process or shell history. <br>
Mitigation: Prefer DATAIFY_API_TOKEN from an environment variable or secret manager, never echo the token, and avoid persistent token setup on shared machines. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-google-maps-reviews) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples and API task status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Dataify API token and confirmation of submitted Google Maps URLs and task parameters.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
