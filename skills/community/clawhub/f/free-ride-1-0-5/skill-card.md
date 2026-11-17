## Description:

Manages free AI models from OpenRouter for OpenClaw by ranking available free models, configuring fallbacks for rate-limit handling, and updating openclaw.json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andy27725](https://clawhub.ai/user/andy27725)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure OpenClaw with OpenRouter free models, choose primary and fallback models, and refresh or inspect model availability. It is useful when reducing model costs or handling rate limits across free model tiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent OpenClaw model configuration changes can alter the user's default model and fallback list.

Mitigation: Back up ~/.openclaw/openclaw.json before use and review the primary and fallback settings before restarting OpenClaw.

Risk: The optional watcher can automatically rotate models during rate limits.

Mitigation: Run the watcher only when automatic rotation is desired, and check watcher status before relying on automatic changes.

Risk: Installer and dependency versions may drift over time.

Mitigation: Prefer pinned installer and Python dependency versions where available.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/andy27725/skills/free-ride-1-0-5)
- [OpenClaw project](https://github.com/openclaw/openclaw)
- [OpenRouter keys](https://openrouter.ai/keys)
- [OpenRouter models API](https://openrouter.ai/api/v1/models)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose OpenClaw configuration changes and optional watcher commands; no structured artifact is guaranteed.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata also reports 1.0.5 and skill.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
