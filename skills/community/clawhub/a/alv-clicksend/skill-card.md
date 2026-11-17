## Description:

SkillBoss API Hub integration for SMS/MMS messaging and voice calls that helps agents send messages, place voice calls, manage contacts and lists, and track delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to work with ClickSend-style messaging workflows through SkillBoss API Hub, including SMS, MMS, voice messages, contact lists, templates, pricing, history, and delivery receipts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send billable SMS, MMS, or voice messages and can cancel scheduled messaging actions.

Mitigation: Require manual review of recipients, message content, schedule, and estimated cost before any send, call, or cancellation request.

Risk: The skill can create, update, transfer, or delete contact and list data.

Mitigation: Require explicit confirmation for destructive or bulk contact operations and prefer test or least-privilege credentials during setup.

Risk: Recipient numbers, message contents, contact records, and account data are processed by SkillBoss/Prelude.

Mitigation: Use the skill only for data approved for that processing path and monitor billing, delivery, and account activity.

Risk: Troubleshooting steps can expose the SkillBoss API key if users print or paste environment variables.

Mitigation: Do not print, paste, or log API keys; store credentials in a secret manager or protected environment variable.

## Reference(s):

- [SkillBoss API Hub](https://heybossai.com)
- [SkillBoss API Run Endpoint](https://api.skillboss.com/v1/run)
- [ClickSend Developer Portal](https://developers.clicksend.com/)
- [ClickSend REST API v3 Documentation](https://developers.clicksend.com/docs)
- [ClickSend Help Center](https://help.clicksend.com/)
- [ClickSend PHP SDK](https://github.com/ClickSend/clicksend-php)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with API examples, JSON payloads, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and a valid SKILLBOSS_API_KEY. Generated requests can transmit recipient numbers, message contents, contact records, and account data.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
