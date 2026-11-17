## Description:

Manages free AI models from OpenRouter for OpenClaw by ranking models, configuring fallbacks for rate-limit handling, and updating OpenClaw model configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taron-ai](https://clawhub.ai/user/taron-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure OpenRouter free models, add ranked fallbacks, and keep model access resilient when free-tier rate limits occur.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads or uses an OpenRouter API key, and the artifact instructions include checking the key in a way that could print it.

Mitigation: Use presence-only checks for OPENROUTER_API_KEY, avoid printing secrets into chat or logs, and rotate the key if exposure is suspected.

Risk: The skill can rewrite OpenClaw model configuration and the optional watcher can continue changing the active model.

Mitigation: Back up ~/.openclaw/openclaw.json before running configuration commands, review resulting model changes, and run the watcher only when persistent automatic rotation is acceptable.

Risk: Free model availability and ranking depend on OpenRouter responses and may change over time.

Mitigation: Review the selected primary and fallback models with freeride status or the OpenClaw status command before relying on the configuration.

## Reference(s):

- [OpenRouter](https://openrouter.ai)
- [OpenRouter Models API](https://openrouter.ai/api/v1/models)
- [OpenRouter API Keys](https://openrouter.ai/keys)
- [OpenClaw Repository](https://github.com/openclaw/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/taron-ai/skills/free-ride-1-0-4)
- [Publisher Profile](https://clawhub.ai/user/taron-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to run local CLI commands that read an OpenRouter API key, update OpenClaw model settings, and restart the OpenClaw gateway.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
