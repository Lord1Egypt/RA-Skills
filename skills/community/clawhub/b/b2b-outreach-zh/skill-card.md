## Description:

This skill helps agents collect Google Maps business leads, validate phone numbers, email addresses, and domains, send bulk cold email or global SMS outreach, and monitor delivery status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External exporters, trading companies, purchasing agents, and global sales teams use this skill to run cross-border B2B outreach workflows: gather merchant leads, validate contact data, send email or SMS campaigns, and review delivery or reply status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an API key that can access billable outreach, account, validation, and task data.

Mitigation: Use an environment variable or protected secret store, avoid printing or pasting ~/.upkuajing/.env, and rotate any exposed key.

Risk: Sending, searching, and validation actions can incur charges and may submit outreach to external recipients.

Mitigation: Confirm each send, search, or validation action before execution and check current pricing instead of estimating costs.

Risk: Bulk outreach and contact-list processing can create privacy, consent, opt-out, or regional compliance obligations.

Mitigation: Use only authorized contact lists with appropriate consent, opt-out handling, and compliance review for the intended geography.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/b2b-outreach-zh)
- [UpKuaJing homepage](https://www.upkuajing.com)
- [UpKuaJing developer portal](https://developer.upkuajing.com/)
- [UpKuaJing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [Email Send API](references/email-send-api.md)
- [Email Task List API](references/email-task-list-api.md)
- [Email Task Record List API](references/email-task-record-list-api.md)
- [SMS Send API](references/sms-send-api.md)
- [SMS Task List API](references/sms-task-list-api.md)
- [SMS Task Record List API](references/sms-task-record-list-api.md)
- [Merchants Search API](references/merchants-search-api.md)
- [Country List API](references/country-list-api.md)
- [Province List API](references/province-list-api.md)
- [City List API](references/city-list-api.md)
- [Phone Validity API](references/validity-phone-api.md)
- [Email Validity API](references/validity-email-api.md)
- [Domain Validity API](references/validity-domain-api.md)
- [Skill Error Report API](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-formatted script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API request guidance, campaign status summaries, validation results, and local task data files.]

## Skill Version(s):

1.0.1 (source: skill metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
