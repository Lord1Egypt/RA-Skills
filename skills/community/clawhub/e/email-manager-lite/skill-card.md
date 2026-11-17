## Description:

Lightweight email manager with IMAP/SMTP support, advanced search, folder management, and attachment detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jorgermp](https://clawhub.ai/user/jorgermp)

### License/Terms of Use:

ISC

## Use Case:

Developers and email power users use this skill to send mail, read and search mailbox contents, inspect attachment metadata, list folders, and move messages through an IMAP/SMTP provider.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles email credentials and private mailbox data and can read mail, send mail, and move messages.

Mitigation: Use a narrowly scoped app password or a test mailbox, and review commands before granting access to a real account.

Risk: The authoritative security scan reports that IMAP TLS certificate verification is disabled.

Mitigation: Enable certificate verification before production use and confirm the configured IMAP host presents a valid certificate.

Risk: Terminal output may include untrusted email content from senders outside the user's control.

Mitigation: Avoid trusting or reusing email-derived terminal output until sanitization is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jorgermp/skills/email-manager-lite)
- [Zoho app passwords](https://accounts.zoho.eu/home#security/apppasswords)
- [Google app passwords](https://myaccount.google.com/apppasswords)
- [README](artifact/README.md)
- [SKILL](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text with command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Email operations may send messages, read mailbox content, list folders, and move messages when run with valid credentials.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact files report 0.2.0 in frontmatter, package.json, and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
