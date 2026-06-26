## Description: <br>
Read, create, update, snooze, and delete alarms on a user's iPhone running ClawAlarm through the ClawAlarm cloud-sync API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anglinb](https://clawhub.ai/user/anglinb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to pair a ClawAlarm-enabled iPhone, inspect existing alarms, and make requested alarm changes from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A long-lived ClawAlarm bearer token can read and change alarms on the paired phone if exposed. <br>
Mitigation: Treat the token as a secret, keep it out of shared project files and committed docs, prefer protected untracked storage or environment variables, and reset pairing if exposure is suspected. <br>
Risk: The skill can create, update, snooze, disable, or delete alarms, which can affect the user's schedule. <br>
Mitigation: Confirm the intended alarm action with the user before running mutating commands and review the generated endpoint, method, and JSON payload before execution. <br>


## Reference(s): <br>
- [Claw Alarm on ClawHub](https://clawhub.ai/anglinb/claw-alarm) <br>
- [ClawAlarm OpenAPI spec](https://api.claw-alarm.com/openapi.json) <br>
- [ClawAlarm API reference](https://api.claw-alarm.com/reference) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a bearer token for one paired device and returns API responses from the ClawAlarm service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
