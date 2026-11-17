## Description:

Manages free AI models from OpenRouter for OpenClaw, automatically ranks models by quality, configures fallbacks for rate-limit handling, and updates openclaw.json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tigertamvip](https://clawhub.ai/user/tigertamvip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to discover free OpenRouter models, set a preferred free model, and configure fallback model routing for rate-limit handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change the OpenClaw default model and fallback routing.

Mitigation: Review and back up ~/.openclaw/openclaw.json before running configuration-changing commands.

Risk: The skill can store model cache and watcher state under ~/.openclaw and optionally run a daemon for model rotation.

Mitigation: Run commands manually first and use daemon mode only after confirming the configured behavior.

Risk: The skill uses an OpenRouter API key when requesting model data or testing model availability.

Mitigation: Use a scoped or replaceable OpenRouter key and manage it through the documented environment or OpenClaw config path.

## Reference(s):

- [Free Ride 1 on ClawHub](https://clawhub.ai/tigertamvip/skills/free-ride-1)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenRouter API Keys](https://openrouter.ai/keys)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks and concise status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may fetch OpenRouter model data and update local OpenClaw JSON configuration, model cache, and watcher state when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact setup.py also reports 1.0.0, while artifact skill.json and _meta.json differ)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
