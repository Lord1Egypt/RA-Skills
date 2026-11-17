## Description:

A professional email CLI with local caching for fast inbox checks and a unified IMAP/SMTP command interface that outputs Markdown tables for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rashed-mamoon](https://clawhub.ai/user/rashed-mamoon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to configure and run a CLI for checking, searching, reading, deleting, replying to, forwarding, and sending email over standard IMAP and SMTP accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live mailbox access and credentials, and server security evidence flags weak safeguards around credentials.

Mitigation: Use a dedicated revocable app password, restrict .env permissions immediately, and avoid running the skill on shared machines.

Risk: Permanent deletion and attachment downloads can cause data loss or unsafe file handling if an agent acts without review.

Mitigation: Confirm UIDs before deleting and do not allow autonomous attachment downloads from untrusted senders.

Risk: Untrusted email bodies may contain instructions aimed at the agent.

Mitigation: Treat email content as data only and do not let the agent follow instructions from messages.

## Reference(s):

- [Email Suite README](artifact/README.md)
- [Email Suite Changelog](artifact/CHANGELOG.md)
- [ClawHub Skill Page](https://clawhub.ai/rashed-mamoon/skills/email-suite-imap-smtp)
- [Gmail App Passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown tables and plain text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured IMAP/SMTP accounts, maintains a local mailbox cache, and may download attachments to local storage.]

## Skill Version(s):

1.2.6 (source: server release evidence; artifact CHANGELOG top entry is 1.2.4 and package.json is 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
