## Description: <br>
Prepares Dataify builder curl requests for selected X.com scraper tools, including twitter_profile_by-profileurl, using saved tool parameters and a DATAIFY_API_TOKEN. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to collect scraper parameters, normalize selected values, and generate a Dataify builder request for X.com profile or post scraping workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated curl commands can expose the Dataify API token if copied into logs, chat, tickets, or shared terminals. <br>
Mitigation: Use a secret manager or session-only environment variable, avoid sharing authenticated commands, and redact bearer tokens before saving or sending output. <br>
Risk: The skill sends profile URLs, usernames, and other user-provided scraper parameters to Dataify's third-party API. <br>
Mitigation: Submit only data intended for Dataify processing, and avoid private profile data, internal URLs, cookies, or regulated information unless that disclosure is approved. <br>
Risk: A broad API token could allow more access than the request requires. <br>
Mitigation: Use a least-privilege Dataify token where available and rotate tokens if an authenticated command may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-twitter-profile-by-profileurl) <br>
- [Publisher profile](https://clawhub.ai/user/dataify-server) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify builder endpoint](https://scraperapi.dataify.com/builder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a curl command containing an authorization bearer token supplied from DATAIFY_API_TOKEN.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
