## Description: <br>
Turns a user's Google Flights request into a confirmed Dataify Scraper API form POST and returns the API response body. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert flight-search requests into Dataify Google Flights API parameters, review a confirmation table, and call Dataify only after explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Flight-search details are sent to Dataify when an API call is confirmed. <br>
Mitigation: Install and use the skill only when sending those search details to Dataify is acceptable. <br>
Risk: Dataify API tokens can be exposed if typed into chat or passed directly on the command line. <br>
Mitigation: Prefer a secure environment variable or secret manager, and never echo Authorization values in confirmation tables or responses. <br>
Risk: Incorrect or unintended flight parameters could produce unwanted API calls or misleading results. <br>
Mitigation: Review the complete pre-call Markdown confirmation table and approve the call only after the parameters are correct. <br>


## Reference(s): <br>
- [Dataify Google Flights API Reference](references/google_flights_api.md) <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-google-flights) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, text, json] <br>
**Output Format:** [Markdown confirmation table followed by the raw Dataify API response body when a call is confirmed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill requires explicit user confirmation before API calls and must not echo Authorization values.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
