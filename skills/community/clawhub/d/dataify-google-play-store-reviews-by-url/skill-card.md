## Description: <br>
Prepare Dataify builder requests for the play.google.com scraper family rooted at google-play-store_reviews_by-url, guiding users through tool selection and generating scraperapi.dataify.com builder curl requests with DATAIFY_API_TOKEN. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare Dataify builder calls for Google Play Store review and information scraper tools, including collecting parameter values and producing ready-to-run curl commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose a Dataify API token in saved shell settings or generated curl output. <br>
Mitigation: Use a session-scoped token or secret manager, avoid storing long-lived tokens in shell startup files, and do not share generated curl output that includes the real token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-google-play-store-reviews-by-url) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify builder endpoint](https://scraperapi.dataify.com/builder) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated curl commands may include a bearer token when the helper reads DATAIFY_API_TOKEN.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
