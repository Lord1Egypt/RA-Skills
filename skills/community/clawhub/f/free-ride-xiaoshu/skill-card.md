## Description:

Manages free AI models from OpenRouter for OpenClaw, ranks models by quality, configures fallbacks for rate-limit handling, and updates OpenClaw model configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaomaju-888](https://clawhub.ai/user/xiaomaju-888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure OpenClaw for OpenRouter free models, ranked fallbacks, model switching, and optional rate-limit rotation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify OpenClaw model configuration.

Mitigation: Back up ~/.openclaw/openclaw.json and review model-related changes before running mutating commands.

Risk: The skill uses an OpenRouter API key.

Mitigation: Use a non-printing presence check, avoid pasting or printing the key, and keep the key in environment or OpenClaw configuration storage.

Risk: The optional watcher can automatically rotate models.

Mitigation: Run the watcher only when automatic model changes are desired and check status before enabling daemon mode.

Risk: Editable installation can execute local Python code and dependencies.

Mitigation: Prefer pinned or isolated installation and review the dependency list before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaomaju-888/skills/free-ride-xiaoshu)
- [OpenRouter](https://openrouter.ai)
- [OpenRouter API models endpoint](https://openrouter.ai/api/v1/models)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that install the CLI, call OpenRouter, and update OpenClaw model configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
