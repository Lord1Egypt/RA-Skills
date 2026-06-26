## Description: <br>
Manages free AI models from OpenRouter for OpenClaw by ranking models, configuring fallbacks for rate-limit handling, and updating OpenClaw model settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy27725](https://clawhub.ai/user/andy27725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure OpenClaw to use free OpenRouter models, refresh ranked model lists, switch primary models, and maintain fallbacks when rate limits occur. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change OpenClaw's persistent default model, fallback models, and model allowlist. <br>
Mitigation: Install and run mutating commands only when those configuration changes are intended, and back up ~/.openclaw/openclaw.json before use. <br>
Risk: The skill handles an OpenRouter API key and may read it from environment variables or OpenClaw configuration. <br>
Mitigation: Avoid printing or sharing the API key, and keep it in environment or OpenClaw configuration only where intended. <br>
Risk: The optional watcher can perform ongoing OpenRouter checks and automatic model rotation. <br>
Mitigation: Run freeride-watcher --daemon only when continuous monitoring and automatic rotation are desired. <br>


## Reference(s): <br>
- [ClawHub Free Ride release page](https://clawhub.ai/andy27725/free-ride-1-0-5) <br>
- [OpenRouter keys](https://openrouter.ai/keys) <br>
- [OpenRouter models API endpoint](https://openrouter.ai/api/v1/models) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update OpenClaw model defaults, fallback models, and model allowlist entries in ~/.openclaw/openclaw.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata also reports 1.0.5 and skill.json reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
