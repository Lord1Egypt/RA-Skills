## Description: <br>
Provides Volcengine Doubao API helpers for image generation and editing, video generation, visual understanding, task management, and configuration setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AI-Lychee](https://clawhub.ai/user/AI-Lychee) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and content teams use this skill to connect agents to Doubao Seedream, Seedance, and Seed Vision workflows for generating media, analyzing images, tracking asynchronous jobs, and managing Volcengine configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image inputs, and generation requests are sent to Volcengine/Doubao APIs. <br>
Mitigation: Use the skill only with data approved for external API processing and avoid submitting sensitive or regulated content unless the deployment has appropriate approvals. <br>
Risk: API keys may be exposed if stored in committed config files or logs. <br>
Mitigation: Prefer ARK_API_KEY as an environment variable, keep .env and .volcengine config files out of version control, and use restrictive file permissions for local config. <br>
Risk: Generated media downloads and task history can be written to local output directories. <br>
Mitigation: Set the output directory deliberately, review downloaded files before reuse, and clean local task or state history when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/AI-Lychee/doubao-seedream-seedance-skill) <br>
- [Volcengine Ark console](https://console.volcengine.com/ark) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with prompts, code snippets, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or retrieve local image and video result files through Volcengine/Doubao APIs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
