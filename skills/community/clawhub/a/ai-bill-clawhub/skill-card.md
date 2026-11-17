## Description:

Real-time AI API usage tracking and cost monitoring for OpenClaw across OpenAI, Claude, Gemini, Kimi, DeepSeek, Grok, and other providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fumarole16-afk](https://clawhub.ai/user/fumarole16-afk)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and agents use this skill to monitor AI API usage, estimate provider costs, update balances and payment modes, and check the billing collector and dashboard health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard can expose or modify sensitive usage and balance data with weak controls.

Mitigation: Bind the service to localhost or place it behind real authentication, avoid public exposure of port 8003, and remove or restrict /api/setup and vault access.

Risk: Installer and background service behavior can introduce unreviewed downloads or persistent services.

Mitigation: Avoid pipe-to-shell installation, pin and verify install artifacts, and make service installation explicit opt-in with clear uninstall steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fumarole16-afk/skills/ai-bill-clawhub)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional shell commands and JSON configuration edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and summarize local usage JSON and suggest configuration or service checks]

## Skill Version(s):

2.2.5 (source: server release metadata and root package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
