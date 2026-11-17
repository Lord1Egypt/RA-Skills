## Description:

B2B Outreach helps agents run bulk cold email and global SMS campaigns, harvest Google Maps merchant data, validate phone, email, and domain contact data, and monitor outreach delivery status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External sales, export, sourcing, and B2B outreach teams use this skill to collect merchant leads, validate contact records, send email or SMS outreach, and monitor campaign delivery. Operators should use it only where their collection, validation, and outreach practices comply with applicable consent, privacy, and anti-spam rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk contact harvesting, validation, email, and SMS outreach can create consent, privacy, and anti-spam compliance risk.

Mitigation: Use the skill only for permitted B2B outreach, verify consent or other lawful basis, honor suppression and opt-out requirements, and review applicable regional rules before running campaigns.

Risk: The skill requires an UpKuaJing API key and evidence reports unsafe key handling.

Mitigation: Store the API key in a protected environment variable or secret store, restrict permissions on ~/.upkuajing/.env, avoid exposing keys in prompts or logs, and rotate any key that may have been disclosed.

Risk: Search, validation, send, and top-up actions may incur fees.

Mitigation: Check current pricing and obtain explicit user confirmation before fee-incurring operations, especially batch searches or multi-recipient sends.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/upkuajing/skills/b2b-outreach)
- [UpKuaJing Homepage](https://www.upkuajing.com)
- [UpKuaJing Open Platform](https://developer.upkuajing.com/)
- [Detailed Price Description](https://www.upkuajing.com/web/openapi/price.html)
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

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API responses]

**Output Format:** [Markdown guidance with shell commands and JSON-like API response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include campaign status, validation results, merchant records, account or pricing guidance, and explicit confirmation prompts before fee-incurring actions.]

## Skill Version(s):

1.0.1 (source: evidence.json release.version and SKILL.md metadata.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
