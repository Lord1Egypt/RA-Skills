## Description:

Build or update the BlueBubbles external channel plugin for OpenClaw, including the extension package, REST send/probe helpers, and webhook inbound handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build or update the BlueBubbles external channel plugin for OpenClaw, including channel wiring, REST helpers, webhook ingestion, reactions, attachments, and configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private messages or attachments could be forwarded across chats without explicit user intent.

Mitigation: Require an explicit relay request before moving message content between chats.

Risk: Attachment handling could write outside the designated storage directory.

Mitigation: Validate resolved attachment download paths and reject absolute paths or traversal segments before writing.

Risk: Webhook-supplied or user-supplied values could be used to construct unsafe API URLs.

Mitigation: Use the shared BlueBubbles URL builder and avoid direct URL concatenation with untrusted values.

Risk: Configured BlueBubbles credentials could be exposed in logs, errors, comments, or outbound payloads.

Mitigation: Access credentials through configuration accessors and redact or omit sensitive values from all outputs.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/snazar-faberlens/skills/bluebubbles-hardened)
- [Faberlens BlueBubbles safety evaluation](https://faberlens.ai/explore/bluebubbles)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell command, and configuration snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
