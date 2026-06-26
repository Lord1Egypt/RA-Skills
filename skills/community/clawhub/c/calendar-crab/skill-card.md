## Description: <br>
Google Calendar CLI — list, create, move, and delete events. Zero dependencies, just Node.js + Google OAuth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawbob](https://clawhub.ai/user/clawbob) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use Calendar Crab to inspect and modify Google Calendar events from a terminal or agent workflow. It supports listing upcoming events, creating meetings, rescheduling events, and deleting events after verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent persistent Google Calendar write and delete access. <br>
Mitigation: Review actions before execution, list events first, and use exact event IDs for move or delete operations when possible. <br>
Risk: OAuth credential and refresh-token files are stored locally. <br>
Mitigation: Store OAuth files with restrictive permissions, do not commit or share them, and revoke the refresh token when the skill is no longer used. <br>
Risk: Move and delete operations may notify attendees. <br>
Mitigation: Assume attendee notifications may be sent and confirm the target event before changing or deleting it. <br>


## Reference(s): <br>
- [Calendar Crab on ClawHub](https://clawhub.ai/clawbob/calendar-crab) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output and Markdown usage guidance with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Google Calendar APIs and update local OAuth token files when access tokens are refreshed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
