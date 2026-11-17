## Description:

This skill is used to send emails via the EngageLab REST API. It supports regular sending, template sending, variable replacement, attachment handling, and sending settings such as sandbox mode and tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[devengagelab](https://clawhub.ai/user/devengagelab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to send EngageLab email messages, including regular email, template-style content, personalized variables, attachments, sandbox testing, and email tracking settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has a legitimate email-sending purpose, but release security evidence reports mishandled API credentials and overly broad external sending behavior.

Mitigation: Review the skill before installation, keep Authorization values out of message payloads and logs, restrict destinations to documented EngageLab endpoints, and add explicit confirmation before live sends.

Risk: Email tracking and attachments can affect recipient privacy and data handling obligations.

Mitigation: Document privacy expectations before use, enable tracking only when appropriate, and review attachment contents before sending.

Risk: The security guidance says not to use production API keys until the send script is fixed to run.

Mitigation: Test with sandbox mode and non-production credentials first, then verify the script behavior before using production EngageLab credentials.

## Reference(s):

- [EngageLab Email REST API Detailed Specification](references/api_spec.md)
- [EngageLab Email API Reference](references/api_reference.md)
- [EngageLab Singapore email send endpoint](https://email.api.engagelab.cc/v1/mail/send)
- [EngageLab Turkey email send endpoint](https://emailapi-tr.engagelab.com/v1/mail/send)
- [ClawHub skill page](https://clawhub.ai/devengagelab/skills/engagelab-email)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON payloads, Python code references, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce live EngageLab API requests when configured with credentials and non-sandbox settings.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
