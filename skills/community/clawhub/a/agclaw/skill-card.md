## Description: <br>
AppGrowing advertising-material analysis assistant for strategy exploration and creative inspiration workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[youcloud](https://clawhub.ai/user/youcloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and advertising teams use this skill to send campaign-analysis prompts to AppGrowing/YouCloud, select the appropriate analysis mode, and receive advertising-material insights or creative direction as Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and advertising-analysis requests are sent to the AppGrowing/YouCloud service. <br>
Mitigation: Install only when that service use matches the organization's data-sharing policy, and avoid submitting confidential campaign or business data unless approved. <br>
Risk: The skill requires an AppGrowing/YouCloud API key and can accept a pasted key for a single request. <br>
Mitigation: Prefer configuring YOUCLOUD_API_KEY as an environment variable and avoid pasting credentials into chat unless the environment is trusted. <br>
Risk: The skill is available only to AppGrowing plans with API access. <br>
Mitigation: Confirm account entitlement and quota before relying on the workflow for production advertising analysis. <br>


## Reference(s): <br>
- [agclaw on ClawHub](https://clawhub.ai/youcloud/skills/agclaw) <br>
- [AppGrowing](https://appgrowing.cn/) <br>
- [Usage Examples](references/example.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with API-call guidance and returned analysis content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AppGrowing/YouCloud API key and may wait up to 600 seconds for the external analysis response.] <br>

## Skill Version(s): <br>
1.1.0 (source: server-resolved release metadata and openclaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
