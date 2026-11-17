## Description:

Interact with an email inbox using mail-cli commands to read, search, send, reply, mark, move, delete, manage folders, drafts, and accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirai3103](https://clawhub.ai/user/mirai3103)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage Gmail or Outlook mailboxes through mail-cli, including inbox review, search, sending or replying, folder organization, draft handling, attachment downloads, and account management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives agents broad mailbox authority for sending, deleting, batch moves, draft deletion, and account removal.

Mitigation: Require explicit user confirmation before sends, deletes, batch moves, draft deletion, or account removal.

Risk: Installing the latest global CLI package may introduce unreviewed behavior.

Mitigation: Use a pinned or otherwise verified mail-cli version before granting mailbox access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mirai3103/skills/emailcli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and parsed JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are expected to parse JSON responses and report errors, partial failures, and remediation steps clearly.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
