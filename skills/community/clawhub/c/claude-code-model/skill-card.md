## Description:

Configure Claude Code to use custom models such as DeepSeek, GLM, Qwen, or other OpenAI-compatible endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moonbird0423](https://clawhub.ai/user/moonbird0423)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claude Code users use this skill to route Claude Code to a chosen third-party or OpenAI-compatible model endpoint by setting the provider URL, model name, API key, and related Claude configuration files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Claude Code traffic can be persistently routed to a configured third-party model endpoint.

Mitigation: Install only when that routing is intended, review the provider URL carefully, and remove ANTHROPIC_* variables plus related Claude config entries to revert.

Risk: API keys can be exposed through shell history, terminal logs, or persistent configuration files.

Mitigation: Use short-lived or restricted API keys where possible and rotate any key exposed in a terminal, shell profile, or log.

Risk: Conflicting or stale Claude Code authentication and model settings can cause unexpected provider or model use.

Mitigation: Clear conflicting ANTHROPIC_AUTH_TOKEN values, check config.json and settings.json for stale values, and open a new terminal after environment changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moonbird0423/skills/claude-code-model)
- [DeepSeek Anthropic-compatible endpoint](https://api.deepseek.com/anthropic)
- [DashScope Anthropic-compatible endpoint](https://coding.dashscope.aliyuncs.com/apps/anthropic)

## Skill Output:

**Output Type(s):** [Configuration instructions, Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline shell, PowerShell, JSON, and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires base_url, model, and api_key inputs; may persistently update Claude Code environment variables and configuration files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
