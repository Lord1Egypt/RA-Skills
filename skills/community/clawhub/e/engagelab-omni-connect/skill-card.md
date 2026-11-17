## Description:

EngageLab Omnichannel communications tool (SMS, WhatsApp, Email) with template management and messaging capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gptbots](https://clawhub.ai/user/gptbots)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support or marketing operators use this skill to prepare approved EngageLab SMS and WhatsApp templates and send SMS, WhatsApp, and email messages through EngageLab APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use real EngageLab provider credentials to send SMS, WhatsApp, and email messages or modify messaging templates.

Mitigation: Install only in authorized messaging environments, scope credentials to the minimum required permissions, and review recipients, template IDs, and message content before execution.

Risk: The package contains an unrelated ClawHub skill-management component with install, update, force-update, and publish authority.

Mitigation: Install only if that package-management authority is intended; otherwise remove or exclude the bundled ClawHub component before deployment and restrict any ClawHub publishing credentials.

## Reference(s):

- [EngageLab Omni Connect ClawHub page](https://clawhub.ai/gptbots/skills/engagelab-omni-connect)
- [EngageLab SMS API base URL](https://smsapi.engagelab.com)
- [EngageLab WhatsApp API base URL](https://wa.api.engagelab.cc/v1)
- [EngageLab Email send endpoint](https://email.api.engagelab.cc/v1/mail/send)
- [EngageLab Email Turkey endpoint](https://emailapi-tr.engagelab.com)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, JSON, Configuration]

**Output Format:** [Markdown guidance with REST endpoint details and JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EngageLab SMS, WhatsApp, and email credentials through environment variables.]

## Skill Version(s):

1.0.3 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
