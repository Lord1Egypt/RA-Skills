## Description:

Use when every conversation needs to be archived to the "历史归档" directory for knowledge management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanll](https://clawhub.ai/user/yanll)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to summarize each completed conversation and append an objective Markdown archive entry to a configured notes repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may archive conversations verbatim without clear per-chat consent or redaction.

Mitigation: Use it only when the user intentionally wants chat archiving, and add explicit consent, redaction, and retention controls before using it with sensitive conversations.

Risk: Archived notes may contain secrets, credentials, personal data, client work, or legal, health, or financial information.

Mitigation: Avoid using the skill for sensitive conversations unless the notes repository has appropriate access controls and retention practices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanll/skills/conversation-archive-skill)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown archive entries with concise summary text and preserved original user and assistant content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Appends entries to a date-named archive file under the configured notes repository.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
