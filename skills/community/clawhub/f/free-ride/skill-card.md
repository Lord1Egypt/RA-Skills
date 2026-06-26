## Description: <br>
Manages free AI models from OpenRouter for OpenClaw by ranking available free models, configuring fallbacks for rate-limit handling, and updating OpenClaw model configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaivpidadi](https://clawhub.ai/user/shaivpidadi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure OpenClaw with free OpenRouter-hosted models, ranked fallbacks, and optional rotation when rate limits interrupt agent use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change OpenClaw default and fallback model routing. <br>
Mitigation: Back up ~/.openclaw/openclaw.json before running commands that update configuration, and review model settings before restarting OpenClaw. <br>
Risk: The optional watcher can keep changing model settings as a background process. <br>
Mitigation: Run freeride-watcher only when continuous automatic rotation is intended, and supervise or stop the process when unattended rotation is no longer needed. <br>
Risk: The skill requires an OpenRouter API key. <br>
Mitigation: Store OPENROUTER_API_KEY as a secret, avoid sharing logs or shell history that expose it, and rotate the key if disclosure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaivpidadi/free-ride) <br>
- [Publisher profile](https://clawhub.ai/user/shaivpidadi) <br>
- [OpenRouter API keys](https://openrouter.ai/keys) <br>
- [OpenRouter model API](https://openrouter.ai/api/v1/models) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and OpenClaw configuration changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OpenRouter API key and may write OpenClaw model, fallback, cache, and watcher state files.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
