## Description:

Complete AI voice receptionist system for dental practices with 12 workflows covering inbound call routing, appointment booking, reminders, no-show follow-up, cancellation and waitlist handling, after-hours capture, patient recall, FAQ handling, staff escalation, CRM sync, daily reports, and SMS reply handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mhmalvi](https://clawhub.ai/user/mhmalvi)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

Dental practice operators, dental IT providers, and automation developers use this skill to configure n8n workflows for AI-assisted phone reception, appointment scheduling, reminders, patient recall, staff escalation, and patient-system synchronization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public webhooks can expose patient-data and scheduling workflows if they are deployed without authentication or signature validation.

Mitigation: Add authentication or signature validation to every public webhook and limit accepted webhook sources before activation.

Risk: The workflows share patient information across calendars, SMS, email, CRM, and optional practice-management APIs.

Mitigation: Review third-party data flows for healthcare compliance and minimize patient information sent to external systems.

Risk: Automated cancellation, no-show classification, waitlist outreach, and CRM or PMS writes can create high-impact patient or business changes.

Mitigation: Require staff approval before destructive or high-impact actions and confirm consent and opt-out handling for patient communications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mhmalvi/skills/dental-ai-receptionist)

## Skill Output:

**Output Type(s):** [Configuration, Guidance, Shell commands]

**Output Format:** [Markdown instructions with environment variables, credential requirements, and workflow import guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance for n8n workflows that integrate Vapi or Retell, Twilio, Google Sheets, Google Calendar, OpenAI, email, and optional CRM or practice-management APIs.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter and _meta.json list 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
