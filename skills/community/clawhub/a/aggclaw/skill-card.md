## Description: <br>
AppGrowing Global intelligent ad creative analysis assistant. Connects to the Explore mode API to analyze user intent, find the most relevant overseas ad creatives, and deliver automated analysis. Includes Inspire mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youcloud](https://clawhub.ai/user/youcloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External AppGrowing Global users use this skill to route creative-analysis and creative-strategy prompts to AppGrowing Global modes for games, apps, short dramas, and ideation. It helps analyze overseas ad creatives and produce markdown analysis from the service response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User prompts, product names, and marketing context are sent to the AppGrowing Global external API under the user's account API key. <br>
Mitigation: Install and use the skill only when that data sharing is acceptable for the intended account, workflow, and AppGrowing Global terms. <br>
Risk: The skill depends on the YOUCLOUD_API_KEY credential for requests to the external service. <br>
Mitigation: Configure the API key only in the environment, avoid exposing it in prompts or logs, and rotate it if access is no longer needed. <br>


## Reference(s): <br>
- [Usage Examples](references/example.md) <br>
- [AppGrowing Global](https://appgrowing.net/) <br>
- [ClawHub Skill Page](https://clawhub.ai/youcloud/skills/aggclaw) <br>
- [Publisher Profile](https://clawhub.ai/user/youcloud) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown analysis returned from the AppGrowing Global API, with setup and error guidance when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires YOUCLOUD_API_KEY and sends user-initiated creative-analysis prompts to the AppGrowing Global API.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and openclaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
