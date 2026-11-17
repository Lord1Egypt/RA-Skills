## Description:

Wire a Fieldy webhook transform into Moltbot hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrzilvis](https://clawhub.ai/user/mrzilvis)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to connect Fieldy voice webhook requests to Moltbot Gateway, triggering an agent only when a wake word is detected and logging other transcripts locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw voice transcripts may be stored locally in JSONL files.

Mitigation: Install only if local transcript storage is acceptable, or modify the transform to disable logging, use a protected fixed log directory, set restrictive permissions, redact sensitive content, and add retention controls.

Risk: The webhook can trigger an agent and has under-scoped controls.

Mitigation: Use a dedicated low-privilege token, restrict and rate-limit the webhook, and keep the receiving agent least-privileged.

Risk: Query-string webhook tokens can be exposed through URLs, logs, or browser history.

Mitigation: Prefer Authorization headers over query-string tokens when the webhook provider supports them.

## Reference(s):

- [Moltbot Webhooks documentation](https://docs.molt.bot/automation/webhook.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a JavaScript webhook transform that can write local JSONL transcript logs.]

## Skill Version(s):

0.1.2 (source: server release metadata; package.json reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
