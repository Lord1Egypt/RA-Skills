## Description: <br>
Dataify Google Images turns a user's Google Images request into a confirmed Dataify Scraper API form submission and returns the API response body. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run Google Images searches through Dataify after reviewing the complete request parameter table and explicitly approving the API call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and supplied location fields are sent to Dataify when the user approves an API call. <br>
Mitigation: Review the confirmation table before approval and avoid submitting sensitive queries or location values. <br>
Risk: Supplying the Dataify API token on the command line can expose it in local shell history or process listings. <br>
Mitigation: Prefer setting DATAIFY_API_TOKEN in the environment rather than passing the token with --token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-google-images) <br>
- [Dataify Google Images API reference](references/google_images_api.md) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown confirmation table followed by the raw Dataify API response body after approval] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Dataify API token; the skill requires explicit user confirmation before external API calls.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
