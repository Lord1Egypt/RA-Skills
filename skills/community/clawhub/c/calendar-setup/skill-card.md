## Description: <br>
Step-by-step wizard for connecting an owner's Google Calendar to their OpenClaw PA agent, including granting write permissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[netanel-abergel](https://clawhub.ai/user/netanel-abergel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Owners, operators, and agent maintainers use this skill to connect an owner's Google Calendar to an OpenClaw PA agent, grant write access, verify the connection, and troubleshoot common authentication or permission failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to obtain owner Google Calendar write access, and the release security summary flags broader Google account access. <br>
Mitigation: Use only when owner calendar write access is intentional, prefer calendar-only OAuth scopes where possible, and revoke Google access when it is no longer needed. <br>
Risk: The release security summary flags unsafe handling of long-lived OAuth secrets. <br>
Mitigation: Do not paste, print, or expose refresh tokens or client secrets; avoid the deployment-specific credential-file workaround unless it is required and approved for the environment. <br>


## Reference(s): <br>
- [Calendar Setup on ClawHub](https://clawhub.ai/netanel-abergel/calendar-setup) <br>
- [Google Calendar](https://calendar.google.com) <br>
- [Google OAuth token endpoint](https://oauth2.googleapis.com/token) <br>
- [Google Calendar API calendar list endpoint](https://www.googleapis.com/calendar/v3/users/me/calendarList) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with numbered steps, checklists, and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes troubleshooting guidance for Google Calendar sharing, OAuth re-authentication, and calendar write-access verification.] <br>

## Skill Version(s): <br>
1.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
