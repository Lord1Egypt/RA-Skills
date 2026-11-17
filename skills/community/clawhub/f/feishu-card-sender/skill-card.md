## Description:

Sends Feishu interactive card messages through Feishu OpenAPI using JSON templates and variable substitution for structured notifications to open_id or chat_id recipients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dobbey](https://clawhub.ai/user/dobbey)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to send templated Feishu card notifications and route Feishu card actions, including MoviePilot subscription callbacks, from structured input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run callback workflows that create MoviePilot subscriptions, so unintended or unauthenticated callbacks could trigger actions beyond sending a card.

Mitigation: Install only for Feishu-to-MoviePilot automation, require Feishu callback signature verification, bind callbacks to the original recipient and media, and review subscription behavior before use.

Risk: Network inputs such as callback requests, MoviePilot endpoints, and poster URLs can expose the workflow to spoofing or untrusted content.

Mitigation: Require HTTPS, configure an explicit MoviePilot base URL, remove any hard-coded default endpoint, and restrict poster downloads to trusted HTTPS image hosts.

Risk: Credential caches and persistent callback state may expose tokens or sensitive workflow data if stored or logged carelessly.

Mitigation: Protect or avoid plaintext token caches and persistent callback state, and keep secret values out of logs.

## Reference(s):

- [Template Parameters](references/template-params.md)
- [TV Template Parameters](references/template-params-tv.md)
- [Feishu Callback Response Contract](references/feishu-callback-response-contract.md)
- [Subscribe Callback](references/subscribe-callback.md)
- [Callback Response Examples](references/callback-response-examples.json)
- [ClawHub Skill Page](https://clawhub.ai/dobbey/skills/feishu-card-sender)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute Feishu OpenAPI calls and callback handling scripts when configured with valid credentials.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
