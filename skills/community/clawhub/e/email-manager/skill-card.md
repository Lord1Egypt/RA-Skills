## Description:

Complete email management for Postfix/Dovecot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soderholmm](https://clawhub.ai/user/soderholmm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage Postfix/Dovecot mailboxes through non-interactive IMAP and SMTP commands, including listing, reading, drafting, sending, moving, deleting, and searching email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad non-interactive mailbox control can send, delete, move, or empty messages without further prompts.

Mitigation: Require explicit confirmation before sending mail, deleting or moving messages, or emptying Trash or Spam folders.

Risk: Mailbox credentials may be stored in local config.json or passed through command-line overrides.

Mitigation: Use a dedicated app password or low-privilege mailbox, keep config.json owner-only and outside shared workspaces or source control, and avoid passing passwords on the command line.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/soderholmm/skills/email-manager)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text or JSON command output, with Markdown usage guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local config.json or environment variables for IMAP/SMTP credentials; no external Python dependencies.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
