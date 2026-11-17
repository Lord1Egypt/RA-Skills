## Description:

Use local CLI to manage Gmail, Outlook, iCloud, Yahoo, Fastmail, and other mail accounts synced in Apple Mail on macOS, without APIs or OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an agent search, triage, draft, send, move, archive, and delete messages in Apple Mail on macOS while keeping provider sync inside Mail.app.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send email or change mailbox state through Apple Mail.

Mitigation: Keep dry-run previews and explicit confirmation gates enabled before send, delete, move, archive, forwarding, reply-all, or bulk workflows.

Risk: Wrong-recipient or duplicate-send mistakes can occur if message identity or recipient lists are ambiguous.

Mitigation: Resolve messages with at least two identity fields, review recipients before sending, require second confirmation when recipients change, and check operation history for duplicate send context.

Risk: Bulk archive or delete actions can cause unintended mailbox changes.

Mitigation: Show filters, impacted counts, and sample rows before execution, require a second confirmation, prefer archive over permanent delete unless explicitly requested, and verify mailbox state afterward.

Risk: Local operation logs may contain mail metadata and high-risk action history.

Mitigation: Store only the operational context needed for safety and review local logs when deciding whether the skill fits the deployment environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/apple-mail-macos)
- [Skill Homepage](https://clawic.com/skills/apple-mail-macos)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run previews, confirmation prompts, operation IDs, and read-back verification for write workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
