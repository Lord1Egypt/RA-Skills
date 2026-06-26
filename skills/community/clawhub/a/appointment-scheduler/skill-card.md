## Description: <br>
Automated appointment management for beauty salons, clinics, studios, and photo booths. Handles booking requests, calendar sync, conflict detection, reminders, no-show tracking, and waitlist management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mupengi-bot](https://clawhub.ai/user/mupengi-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External service businesses such as salons, clinics, studios, and photo booths use this skill to manage appointment intake, booking, calendar sync, conflict checks, reminders, no-show tracking, and waitlists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A confirmed command-injection weakness can expose the host when booking identifiers or related command inputs are untrusted. <br>
Mitigation: Fix the unsafe shell call before production use; invoke scripts with argument arrays or direct module calls and validate booking identifiers. <br>
Risk: The skill stores customer names, contact details, appointment history, no-show status, and reminder logs. <br>
Mitigation: Collect only necessary data, avoid sensitive notes, define retention and deletion practices, and restrict access to appointment data files. <br>
Risk: Google Calendar integration depends on OAuth credential and token files. <br>
Mitigation: Store credentials outside shared workspaces, restrict file permissions, rotate tokens when access changes, and verify the calendar scope before connecting real accounts. <br>
Risk: Automated reminder and waitlist messages may contact customers without appropriate consent or with incorrect timing. <br>
Mitigation: Confirm opt-in messaging consent, test timezone and calendar settings, and review generated messages before enabling automated sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mupengi-bot/appointment-scheduler) <br>
- [Publisher profile](https://clawhub.ai/user/mupengi-bot) <br>
- [README.md](README.md) <br>
- [TESTING.md](TESTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces booking records, reminder payloads, waitlist notifications, no-show reports, event logs, and calendar sync actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
