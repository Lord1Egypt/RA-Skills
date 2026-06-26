## Description: <br>
Turns a user's Google Videos request into a confirmed Dataify Scraper API form submission. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to prepare and run Google Videos searches through Dataify, with a parameter confirmation table before any API call. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google Videos search parameters are sent to Dataify. <br>
Mitigation: Install and use the skill only when that data flow is intended, and avoid entering secrets or private data in search fields. <br>
Risk: Passing a Dataify token on the command line can expose it through shell history or process inspection. <br>
Mitigation: Prefer DATAIFY_API_TOKEN for authentication and avoid echoing token values in conversation or logs. <br>
Risk: The skill returns the raw API response body directly. <br>
Mitigation: Review returned content before relying on it or forwarding it to downstream tools. <br>


## Reference(s): <br>
- [Google Videos API Reference](artifact/references/google_videos_api.md) <br>
- [Dataify Scraper API Endpoint](https://scraperapi.dataify.com/request) <br>
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/dataify-google-videos) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, JSON, guidance] <br>
**Output Format:** [Markdown confirmation tables and raw Dataify API response bodies, typically JSON or HTML depending on request parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Dataify API token and returns the API response body directly after user confirmation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
