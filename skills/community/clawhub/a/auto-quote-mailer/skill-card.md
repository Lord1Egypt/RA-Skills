## Description:

Automates e-commerce inquiry email processing by fetching unread IMAP messages, translating content, storing local archives, and drafting quotation replies from configurable pricing rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fankcoder](https://clawhub.ai/user/fankcoder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business operators use this skill to automate customer inquiry intake and produce quotation drafts for e-commerce, medal, trophy, and custom manufacturing workflows. Generated quotes should be reviewed before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles full customer emails and stores raw, extracted, translated, and quote content locally.

Mitigation: Use a dedicated inquiry mailbox, restrict access to email_storage, and clean up stored mail on a retention schedule.

Risk: Automatic translation can send customer email content to a third-party translation service.

Mitigation: Disable translation or require explicit approval before translating sensitive customer mail.

Risk: The workflow marks processed messages as read.

Mitigation: Test mark-as-read behavior on a non-production mailbox before using it on live inquiries.

Risk: Email credentials and IMAP settings are required for operation.

Mitigation: Use least-privilege app passwords, require SSL/TLS IMAP, and keep credentials out of source files and shared artifacts.

Risk: Dependency behavior can change if unreviewed package versions are used.

Mitigation: Pin reviewed dependency versions before deployment and retest translation and email processing after updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fankcoder/skills/auto-quote-mailer)
- [Artifact README](artifact/README.md)
- [Data setup instructions](artifact/data/README.md)
- [Example pricing rules](artifact/data/example/pricing_rules_example.md)
- [Email template](artifact/references/email_template.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python scripts, configuration files, HTML templates, and generated plain-text email quote drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local .eml archives, extracted text, translated text, and quote draft files; console output reports processing status.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
