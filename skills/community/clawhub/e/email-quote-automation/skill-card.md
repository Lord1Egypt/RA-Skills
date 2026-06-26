## Description: <br>
Automates email inquiry handling for custom manufacturing businesses by fetching unread customer emails, translating non-target-language content, calculating quotes from configured pricing rules, and saving quote reply drafts for review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fankcoder](https://clawhub.ai/user/fankcoder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and operations teams at custom manufacturing or e-commerce businesses use this skill to triage mailbox inquiries, preserve customer email records, calculate draft prices from business rules, and prepare quote replies for human review before sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads customer email and requires sensitive mailbox credentials. <br>
Mitigation: Use a dedicated least-privilege mailbox with an app password, store credentials securely, and test against a non-production inbox before deployment. <br>
Risk: Processed email content is stored locally, including original messages, extracted text, translations, and quote drafts. <br>
Mitigation: Restrict permissions on the storage directory and define retention and deletion procedures appropriate for customer data. <br>
Risk: Non-target-language email content may be sent to an external translation service. <br>
Mitigation: Disable external translation or replace it with an approved service before processing confidential or regulated mail. <br>
Risk: Unread messages are marked as read after processing, which can hide failed or incomplete handling. <br>
Mitigation: Review behavior in a test inbox and monitor generated manual-review files before allowing production mail to be marked as read. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fankcoder/email-quote-automation) <br>
- [Email template](artifact/references/email_template.html) <br>
- [Pricing data instructions](artifact/data/README.md) <br>
- [Example pricing rules](artifact/data/example/pricing_rules_example.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python scripts, configuration files, local email archives, translated text files, and quote reply drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on mailbox contents, translation settings, and user-supplied pricing rules; generated quote drafts should be reviewed before being sent to customers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
