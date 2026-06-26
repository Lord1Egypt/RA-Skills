## Description: <br>
Manages free AI models from OpenRouter for OpenClaw, ranks available models, configures fallbacks for rate-limit handling, and updates openclaw.json. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaomaju-888](https://clawhub.ai/user/xiaomaju-888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure OpenClaw to route requests through OpenRouter free models, set a ranked primary model, and maintain fallback models when rate limits occur. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change the OpenClaw primary model, fallback models, and model allowlist. <br>
Mitigation: Back up ~/.openclaw/openclaw.json before running configuration commands and verify the active model with OpenClaw status commands after restart. <br>
Risk: The skill requires an OpenRouter API key and reads it from the environment or OpenClaw config. <br>
Mitigation: Keep the API key in a local environment variable or OpenClaw config, avoid printing or sharing it, and rotate it if exposed. <br>
Risk: The optional watcher can make ongoing OpenRouter health checks and automatically rotate models. <br>
Mitigation: Run freeride-watcher --daemon only when continuous monitoring and automatic rotation are intended, and use watcher status or cooldown controls to review behavior. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xiaomaju-888/free-ride-xiaoshu) <br>
- [OpenClaw project](https://github.com/openclaw/openclaw) <br>
- [OpenRouter](https://openrouter.ai) <br>
- [OpenRouter API keys](https://openrouter.ai/keys) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands and CLI instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can update OpenClaw model settings and may create FreeRide cache or watcher state files under ~/.openclaw.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
