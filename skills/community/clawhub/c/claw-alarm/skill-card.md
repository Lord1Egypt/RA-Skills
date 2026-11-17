## Description:

Claw Alarm lets an agent read, create, update, snooze, and delete alarms on a paired iPhone running ClawAlarm through the ClawAlarm cloud-sync API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anglinb](https://clawhub.ai/user/anglinb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to manage alarms on a paired iPhone, including listing, creating, updating, snoozing, disabling, and deleting alarms. It is intended for personal alarm-control workflows after a user completes the ClawAlarm pairing handshake.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived pairing tokens can read and rewrite the alarm list for the paired device if exposed.

Mitigation: Treat the token like a password, keep it out of committed files, shared notes, logs, and shell history, and reset pairing if exposure is suspected.

Risk: The API wrapper can delete, disable, or overwrite alarms once authenticated.

Mitigation: Require explicit user confirmation before destructive or schedule-changing operations such as deletion, disabling, snoozing, or overwriting alarms.

Risk: The API destination can be changed with CLAW_ALARM_API_BASE_URL.

Mitigation: Run the wrapper with an overridden API base URL only when the destination is intentional and trusted.

## Reference(s):

- [Claw Alarm skill page](https://clawhub.ai/anglinb/skills/claw-alarm)
- [ClawAlarm OpenAPI spec](https://api.claw-alarm.com/openapi.json)
- [ClawAlarm API reference](https://api.claw-alarm.com/reference)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform authenticated API calls when the user has supplied a valid ClawAlarm pairing token.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
