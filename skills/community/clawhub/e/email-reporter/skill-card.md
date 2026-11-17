## Description:

Email Reporter helps OpenClaw agents send Markdown reports by email and converts image-heavy or large reports to PDF attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dirkcaiusa](https://clawhub.ai/user/dirkcaiusa)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to email generated reports from OpenClaw agents, with support for Markdown delivery, PDF conversion, and SMTP configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The msmtp backend can expose reports or allow command execution through unsafe command and temporary-file handling.

Mitigation: Use the SMTP backend only and keep msmtp disabled until command construction and temporary-file handling are fixed.

Risk: SMTP credentials and emailed reports may be exposed if plaintext configuration files or unreviewed report content are used.

Mitigation: Prefer environment variables or locked-down config-file permissions, use limited app passwords, and review report content before sending.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dirkcaiusa/skills/email-reporter)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown or PDF email attachments, plain-text status messages, and Markdown documentation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May convert Markdown reports to PDF when images are present or files are larger than 500KB.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and README state 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
