## Description:

Automated appointment management for beauty salons, clinics, studios, and photo booths. Handles booking requests, calendar sync, conflict detection, reminders, no-show tracking, and waitlist management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mupengi-bot](https://clawhub.ai/user/mupengi-bot)

### License/Terms of Use:


## Use Case:

Service-business operators and their agents use this skill to parse customer booking requests, create and cancel appointments, check availability, send reminders, track no-shows, manage waitlists, and optionally sync bookings with calendar services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles customer appointment data and calendar access, including phone numbers and notes.

Mitigation: Review the data-handling model before installation, avoid syncing phone numbers or notes unless customers have consented, and store appointment data with restricted file permissions.

Risk: Google Calendar integration can use broad calendar permissions and stores OAuth material locally.

Mitigation: Use a dedicated calendar, restrict token permissions, and keep credentials and tokens in protected secret paths.

Risk: Cron-based reminders and calendar sync continue running after setup.

Mitigation: Enable cron jobs only as an explicit opt-in and document how to audit, pause, or remove them.

Risk: Natural-language date parsing may miss or misread booking times.

Mitigation: Validate date inputs before booking or syncing and prefer explicit date and time formats for customer requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mupengi-bot/skills/appointment-scheduler)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [TESTING.md](artifact/TESTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and structured JSON message outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates local appointment, waitlist, no-show, reminder, event, and optional calendar-sync records.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
