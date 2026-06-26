## Description: <br>
Automates ecommerce inquiry email processing by fetching unread mail, translating messages, storing email content locally, and generating quotation drafts from configurable pricing rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fankcoder](https://clawhub.ai/user/fankcoder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users and developers use this skill to process ecommerce inquiry emails, archive message content, translate customer requests, and draft price quotations for products with repeatable pricing rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process every unread message in a configured mailbox and mark messages as read automatically. <br>
Mitigation: Install it only for a dedicated inquiry mailbox or folder, and test single-check mode before running the daemon. <br>
Risk: Processed customer emails and generated quote drafts may be stored locally. <br>
Mitigation: Secure the email_storage directory and define retention and deletion rules for stored email content. <br>
Risk: Message text may be sent to external translation services when translation is enabled. <br>
Mitigation: Disable external translation unless approved for the data being processed. <br>
Risk: Mailbox credentials are required for IMAP access. <br>
Mitigation: Use an app password or secret manager rather than a primary account password. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fankcoder/auto-quote-mailer) <br>
- [Skill README](artifact/README.md) <br>
- [Pricing data instructions](artifact/data/README.md) <br>
- [Example pricing rules](artifact/data/example/pricing_rules_example.md) <br>
- [Email template](artifact/references/email_template.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python shell commands and generated quotation text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local raw email, extracted text, translation, and quote files under the configured storage directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
