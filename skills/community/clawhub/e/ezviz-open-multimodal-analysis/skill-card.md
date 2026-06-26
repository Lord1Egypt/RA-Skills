## Description: <br>
Analyzes Ezviz camera snapshots by capturing device images and sending selected image URLs to Ezviz AI agent services for multimodal understanding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ezviz-Open](https://clawhub.ai/user/Ezviz-Open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run AI analysis over Ezviz camera views for scene understanding, object detection, behavior review, and monitoring workflows. It is intended for environments where the user has valid Ezviz credentials and permission to process the selected camera imagery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected camera snapshots, image URLs, device identifiers, prompts, and Ezviz credentials are sent to Ezviz cloud endpoints. <br>
Mitigation: Use only with authorized cameras, verify the configured device serials, and ensure the deployment meets privacy and data handling requirements. <br>
Risk: Ezviz credentials may be read from local OpenClaw config files when environment variables are absent. <br>
Mitigation: Prefer explicit environment variables and keep Ezviz credentials isolated from unrelated local service credentials. <br>
Risk: Access tokens are cached in the system temp directory by default. <br>
Mitigation: Disable token caching with EZVIZ_TOKEN_CACHE=0 on shared or high-security machines and use least-privilege, rotated Ezviz credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ezviz-Open/ezviz-open-multimodal-analysis) <br>
- [Ezviz API reference](references/ezviz-agent-api.md) <br>
- [Ezviz AccessToken API](https://openai.ys7.com/help/81) <br>
- [Ezviz device capture API](https://openai.ys7.com/help/687) <br>
- [Ezviz intelligent agent analysis API](https://openai.ys7.com/help/5006) <br>
- [Ezviz AI agent console](https://openai.ys7.com/console/aiAgent/aiAgent.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Console text with JSON analysis results and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analysis content depends on the configured Ezviz AI agent prompt and the captured camera image.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
