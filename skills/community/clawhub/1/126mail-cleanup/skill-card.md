## Description:

Use this skill when the user wants to clean up, back up, or optimize their 126.com (NetEase) email account, including local backup, spam and subscription cleanup, and large attachment stripping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinghaojia](https://clawhub.ai/user/yinghaojia)

### License/Terms of Use:

MIT-0

## Use Case:

External users with NetEase 126.com mailboxes use this skill to back up email locally, classify bulk senders, review cleanup candidates, delete unwanted mail, and reduce server storage used by large attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires full IMAP access to the user's 126.com mailbox.

Mitigation: Use a 126 IMAP authorization code rather than the login password, store it securely, and revoke it when mailbox cleanup is complete.

Risk: Cleanup or attachment stripping can permanently remove email, including unrelated messages already marked deleted if EXPUNGE is applied broadly.

Mitigation: Create and verify a full local backup first, require explicit approval for destructive steps, and restrict expunge operations to approved UID sets or use Trash/staging for manual deletion.

Risk: Local backups and downloaded attachments may contain sensitive mailbox data.

Mitigation: Save backups only to a trusted local directory with appropriate access controls and delete temporary progress or export files when no longer needed.

## Reference(s):

- [126 Mail Cleanup on ClawHub](https://clawhub.ai/yinghaojia/skills/126mail-cleanup)
- [yinghaojia ClawHub publisher profile](https://clawhub.ai/user/yinghaojia)
- [NetEase 126 Mail](https://mail.126.com)
- [Support issues](https://github.com/jimmyclaw/126mail-cleanup/issues)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with command examples, configuration values, and procedural checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to create local backup, metadata, classification, and progress files during mailbox operations.]

## Skill Version(s):

1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
