## Description:

Send and search email through configurable IMAP and SMTP settings with support for recipients, message content, mailbox queries, and optional read marking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chowardcode](https://clawhub.ai/user/chowardcode)

### License/Terms of Use:


## Use Case:

Developers and agent users can use this skill to send outbound email and search inbox messages from a configured email account. It is intended for workflows where an agent needs email access through reviewed recipients, message bodies, and mailbox queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send email using configured account credentials, which could deliver unintended messages if agent actions are not reviewed.

Mitigation: Require manual review of recipients, subject, body, CC, BCC, and message body before sending, and use only an email account appropriate for agent access.

Risk: Mailbox searches can expose message contents and may mark messages as read when markRead is enabled.

Mitigation: Avoid sensitive mailbox searches unless needed, leave markRead disabled unless explicitly intended, and review how returned message content is handled.

Risk: Security guidance recommends dependency updates before production use.

Mitigation: Update vulnerable dependencies and rerun security review before production deployment.

## Reference(s):

- [ClawHub Email Tool page](https://clawhub.ai/chowardcode/skills/email-tool)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [Plain text status messages and email search result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can send email and retrieve inbox content using externally supplied account credentials.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
