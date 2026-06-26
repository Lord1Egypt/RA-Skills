## Description: <br>
Doubao Ai Toolkit gives agents command templates and configuration guidance for using ByteDance Doubao and Volcengine Ark CLIs for image, video, speech, chat, search, and embedding tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cryptocxf](https://clawhub.ai/user/cryptocxf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to choose and compose Doubao/Ark CLI commands for media generation, speech processing, chat, search, embeddings, and API-key setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands require ARK_API_KEY and may expose credentials if keys are placed directly in shell history, scripts, or shared logs. <br>
Mitigation: Prefer environment variables or a secret manager, avoid inline API keys, and review generated commands before execution. <br>
Risk: Audio, image, video, and text inputs may be uploaded to Doubao/Ark services for processing. <br>
Mitigation: Do not send confidential or regulated content unless the user's organization permits that provider to process it. <br>
Risk: The skill depends on third-party npm CLI packages and external AI services. <br>
Mitigation: Install only from trusted package sources and verify the Doubao/Ark service and package behavior before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cryptocxf/doubao-ai-toolkit) <br>
- [Volcengine Ark API key console](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI command templates and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes examples that may reference ARK_API_KEY and third-party Doubao/Ark services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
