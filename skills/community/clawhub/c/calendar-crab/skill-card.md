## Description:

Google Calendar CLI - list, create, move, and delete events. Zero dependencies, just Node.js + Google OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawbob](https://clawhub.ai/user/clawbob)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Calendar Crab to let an agent or terminal session list, create, reschedule, and delete Google Calendar events through Google OAuth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, move, or delete Google Calendar events immediately using stored OAuth credentials.

Mitigation: Review proposed calendar operations before execution and list events first to confirm the intended target.

Risk: Time-based move and delete operations can affect the wrong event when more than one event matches.

Mitigation: Use event IDs for move and delete operations whenever possible and avoid time-based deletes for ambiguous calendar slots.

Risk: OAuth credential and token files stored locally can expose calendar access if shared or copied.

Mitigation: Store OAuth files in a private directory with restrictive permissions and revoke the Google refresh token if the files are exposed.

## Reference(s):

- [Calendar Crab ClawHub Page](https://clawhub.ai/clawbob/skills/calendar-crab)
- [Google Cloud Console](https://console.cloud.google.com/)
- [OpenClaw Project](https://github.com/pearyj/openclaw)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text CLI output with shell commands and JSON error details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can perform authenticated Google Calendar API operations that create, move, or delete events.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
