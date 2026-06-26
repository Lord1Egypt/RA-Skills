## Description: <br>
When users search for information using Google AI Model, this skill is employed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert Google AI Mode search requests into Dataify Scraper API calls. The skill prepares parameters, obtains user confirmation, and returns the Dataify API response body directly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and request parameters are sent to Dataify's API. <br>
Mitigation: Install and use the skill only when sending search queries to Dataify is intended and a valid Dataify token is available. <br>
Risk: Passing a Dataify token on the command line can expose it through local shell or process history. <br>
Mitigation: Prefer the DATAIFY_API_TOKEN environment variable over command-line token arguments. <br>
Risk: Raw API responses may contain content that should not be shared unchanged. <br>
Mitigation: Review returned API responses before sharing them outside the conversation or workflow. <br>


## Reference(s): <br>
- [Dataify Google AI Mode API Reference](references/google_ai_mode_api.md) <br>
- [Dataify Dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/dataify-google-ai-mode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown confirmation tables, shell command examples, configuration guidance, and raw API response text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Dataify API token; API responses are returned unchanged.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
