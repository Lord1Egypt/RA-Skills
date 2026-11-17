## Description:

Give an AI agent real communication channels - Slack, Discord, Telegram, email, X, SMS - behind one on_message handler via caspian-sdk, with free channels requiring no signup because the skill mints a sandbox API key itself.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trycaspian](https://clawhub.ai/user/trycaspian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add multi-channel messaging to an AI agent through caspian-sdk, using one message handler for email, Slack, Discord, Telegram, X, SMS, and related channel setup flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask users to provide long-lived provider tokens or account credentials during channel setup.

Mitigation: Prefer OAuth-based setup where available, avoid pasting long-lived tokens into chat, and rotate any credentials used during installation.

Risk: The skill includes billing automation flows such as autopay and paid channel credit management.

Mitigation: Require explicit user approval before enabling autopay, configure monthly and per-channel caps, and monitor low-balance or limit events.

Risk: The skill suggests using remotely fetched channel behavior text in an agent prompt.

Mitigation: Review fetched behavior guidance before use and do not place untrusted remote text directly into a privileged system prompt.

Risk: The server security verdict is suspicious.

Mitigation: Review the skill before installing, pin the caspian-sdk dependency in a lockfile, and follow the server-provided security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trycaspian/skills/caspian)
- [Caspian homepage](https://trycaspianai.com)
- [Caspian REST reference](https://api.trycaspianai.com/docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python snippets, shell commands, API requests, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CASPIAN_API_KEY for authenticated gateway operations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
