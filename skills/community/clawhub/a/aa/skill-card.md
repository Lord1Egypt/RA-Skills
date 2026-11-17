## Description:

Automatically draft and send Gmail replies matching a client's tone, sign-off, and templates, requiring Gmail access and a client profile for context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azvast](https://clawhub.ai/user/azvast)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to draft concise Gmail replies on behalf of a client, matching the client's tone, sign-off, templates, and escalation rules. It can return drafts for approval or send replies when the user has explicitly configured sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto-send mode can grant the agent sensitive Gmail sending authority.

Mitigation: Keep draft-only review as the default and require explicit user approval before enabling any sending behavior.

Risk: Gmail access may expose sensitive email content or credentials.

Mitigation: Use least-privilege Gmail scopes and keep credentials in environment variables or secure configuration instead of skill files.

Risk: Unusual, sensitive, or instruction-like emails may lead to inappropriate replies.

Mitigation: Restrict auto-send rules to low-risk senders, labels, and templates, and require human approval for sensitive or unusual messages.

## Reference(s):

- [Skill instructions](artifact/SKILL.md)
- [Package manifest](artifact/manifest.json)
- [Reply templates](artifact/templates/reply_templates.json)
- [ClawHub skill page](https://clawhub.ai/azvast/skills/aa)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or plain text email drafts with optional template guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a configured Gmail send function only when the user has explicitly enabled sending.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
