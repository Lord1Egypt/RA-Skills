## Description:

Fixes OpenClaw's OpenRouter model prefix routing bug for reliable automatic fallback switching using free AI models with proper prefixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rongtianhua](https://clawhub.ai/user/rongtianhua)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure OpenRouter free models, ranked fallbacks, and corrected OpenRouter model prefixes so model routing remains reliable after rate limits or fallback changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify OpenClaw model settings in ~/.openclaw/openclaw.json.

Mitigation: Back up ~/.openclaw/openclaw.json and review primary and fallback model entries before restarting the gateway.

Risk: The skill may use an OpenRouter key discovered in another local OpenClaw agent profile.

Mitigation: Set a dedicated OPENROUTER_API_KEY explicitly and review local agent profile access before running auto or watcher commands.

Risk: The install dependency specification is mutable.

Mitigation: Install in a controlled environment and pin or review resolved dependencies before deployment.

Risk: The watcher can make OpenRouter chat completion health-check calls and rotate models automatically.

Mitigation: Run the watcher only when automatic rotation is intended and monitor watcher state plus OpenClaw configuration changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rongtianhua/skills/free-ride-prefix-fix)
- [OpenClaw Project](https://github.com/openclaw/openclaw)
- [OpenRouter Keys](https://openrouter.ai/keys)
- [OpenRouter Models API](https://openrouter.ai/api/v1/models)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an OpenRouter API key and can update OpenClaw model configuration.]

## Skill Version(s):

1.0.8 (source: server release evidence, skill.json, setup.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
