## Description: <br>
Turns Google Lens and reverse-image-search requests into Dataify Scraper API form submissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare and run Google Lens image-search requests through Dataify. The skill shows a parameter confirmation table before calling the API and returns the API response body directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image URLs and search parameters are sent to Dataify. <br>
Mitigation: Review the pre-call parameter table and avoid private or signed image URLs unless disclosure to Dataify is intended. <br>
Risk: DATAIFY_API_TOKEN is required for API calls. <br>
Mitigation: Store the token in a protected environment or secret manager, and do not print Authorization values in previews or final responses. <br>


## Reference(s): <br>
- [Dataify Google Lens API Reference](references/google_lens_api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/dataify-google-lens) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown parameter table followed by raw Dataify API response text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DATAIFY_API_TOKEN and sends the image URL plus selected search parameters to Dataify after user confirmation.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
