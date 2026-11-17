## Description:

Books, tracks, and reminds you about every appointment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rednix](https://clawhub.ai/user/rednix)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to book, log, reschedule, cancel, and receive reminders for personal appointments, including medical, dental, optician, beauty, and custom appointment types.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store sensitive appointment and medical-adjacent history in local Markdown files.

Mitigation: Install only when local appointment and provider history storage is acceptable, and avoid recording unnecessary medical details in notes or follow-ups.

Risk: The skill may transmit personal details such as date of birth, medical reason, address, or follow-up notes through booking sites, calendars, or reminder channels.

Mitigation: Require explicit user confirmation before any booking, cancellation, calendar update, or transmission of sensitive personal details.

Risk: Online booking and rescheduling actions can create, change, or cancel real appointments.

Mitigation: Present the provider, slot, action, and submitted details for confirmation before completing any external appointment workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rednix/skills/appointment-manager)
- [Skill homepage metadata](https://clawhub.com/skills/appointment-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown records, plain-text reminders, call scripts, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local appointment, provider, and configuration Markdown files; may prepare reminder schedules and calendar entries when connected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
