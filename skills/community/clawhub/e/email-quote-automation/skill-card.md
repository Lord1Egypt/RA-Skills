## Description:

Automates IMAP inquiry intake for custom medal and manufacturing businesses by saving customer emails, translating non-target-language content, calculating quotes from configurable pricing rules, and generating reply templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fankcoder](https://clawhub.ai/user/fankcoder)

### License/Terms of Use:

MIT-0

## Use Case:

External sales and operations users at custom manufacturing businesses use this skill to monitor inquiry mailboxes, organize customer requests, and prepare quote drafts for review before replying.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox credentials and app passwords are configured in local project files.

Mitigation: Use a dedicated mailbox with a revocable app password, keep SSL enabled, and avoid committing configured secrets.

Risk: Customer email contents and generated quotes are stored locally.

Mitigation: Store processed email folders in a private location with access controls and retention rules.

Risk: External translation may send customer email content to a third-party translation service.

Mitigation: Disable external translation or use it only after approval for the customer data being processed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fankcoder/skills/email-quote-automation)
- [README.md](artifact/README.md)
- [Data Files Instructions](artifact/data/README.md)
- [Example Pricing Rules - Medal Customization](artifact/data/example/pricing_rules_example.md)
- [Email quotation template](artifact/references/email_template.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated plain-text quotation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores raw email, extracted text, translated content, and quote drafts in user-configured local folders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
