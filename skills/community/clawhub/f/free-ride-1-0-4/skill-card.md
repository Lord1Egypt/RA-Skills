## Description: <br>
Manages free AI models from OpenRouter for OpenClaw by ranking models, configuring fallbacks for rate-limit handling, and updating OpenClaw model settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taron-ai](https://clawhub.ai/user/taron-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure OpenClaw to route through OpenRouter free models, list and switch models, and maintain fallback model choices when rate limits occur. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change OpenClaw default model routing and fallback configuration. <br>
Mitigation: Back up ~/.openclaw/openclaw.json before running config-changing commands and review model settings after changes. <br>
Risk: The skill requires an OpenRouter API key. <br>
Mitigation: Use a dedicated OpenRouter API key and keep it out of source control and shared logs. <br>
Risk: The optional watcher can run ongoing automatic model rotation. <br>
Mitigation: Start freeride-watcher only when continuous model rotation is intended. <br>


## Reference(s): <br>
- [ClawHub Free Ride 1.0.4 page](https://clawhub.ai/taron-ai/free-ride-1-0-4) <br>
- [OpenRouter](https://openrouter.ai) <br>
- [OpenRouter API models endpoint](https://openrouter.ai/api/v1/models) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenRouter API key and may change OpenClaw default model and fallback settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
