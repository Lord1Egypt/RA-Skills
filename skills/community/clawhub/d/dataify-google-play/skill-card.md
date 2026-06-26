## Description: <br>
Turns Google Play search, ranking, category, and device browsing requests into confirmed Dataify Scraper API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to prepare Google Play app-store searches, rankings, category browsing, and device-specific requests for Dataify. It shows a required parameter confirmation table before making a real API call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Play search terms and request parameters are sent to Dataify during real API calls. <br>
Mitigation: Review the confirmation table before approving a call and avoid sending sensitive search terms or parameters. <br>
Risk: API tokens can be exposed when passed directly on a command line. <br>
Mitigation: Prefer DATAIFY_API_TOKEN in the environment over passing tokens with --token. <br>
Risk: The skill returns raw API responses without summarizing or reshaping them. <br>
Mitigation: Review downstream handling expectations before using the raw JSON or HTML response in another workflow. <br>


## Reference(s): <br>
- [Dataify Google Play API Reference](references/google_play_api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/dataify-google-play) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Markdown confirmation tables, shell commands, and raw Dataify API response bodies, usually JSON or HTML depending on the requested output mode.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DATAIFY_API_TOKEN for real API calls; returns the API response without post-processing.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
