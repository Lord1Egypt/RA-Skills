## Description:

Manages AI models from SkillBoss API Hub for OpenClaw, ranks free models by quality, configures fallbacks for rate-limit handling, and updates openclaw.json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to discover free model options, configure a primary model, and maintain fallback models when rate limits interrupt work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The executable code sends SKILLBOSS_API_KEY to api.heybossai.com while README.md describes OpenRouter credentials.

Mitigation: Confirm the intended service identity before use and use only a limited SkillBoss key you are comfortable sending to that endpoint.

Risk: Mutating commands persistently change ~/.openclaw/openclaw.json model defaults, fallback models, and model allowlist entries.

Mitigation: Back up openclaw.json and review the proposed model configuration before restarting the OpenClaw gateway.

Risk: Installation uses editable Python packaging with an unpinned requests dependency.

Mitigation: Install in an isolated environment, pin dependencies for managed deployments, and avoid running installation as root or administrator.

Risk: The optional freeride-watcher command is advertised, but artifact/watcher.py is empty.

Mitigation: Do not rely on watcher-based auto-rotation until the publisher ships and validates that implementation.

## Reference(s):

- [abe-freeride ClawHub listing](https://clawhub.ai/abeltennyson/skills/abe-freeride)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [OpenRouter keys](https://openrouter.ai/keys)
- [SkillBoss API endpoint used by artifact](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update OpenClaw model configuration and local model cache when CLI commands are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and setup.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
