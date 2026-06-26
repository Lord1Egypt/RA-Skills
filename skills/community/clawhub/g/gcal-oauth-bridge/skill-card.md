## Description: <br>
Interact with Calendar Bridge, a self-hosted Node.js service that provides a persistent REST API for Google Calendar events, lists calendars, and helps set up or troubleshoot OAuth with token auto-refresh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DanielKillenberger](https://clawhub.ai/user/DanielKillenberger) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to check upcoming Google Calendar events, list calendars, and set up or troubleshoot a local Calendar Bridge OAuth service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Google Calendar data and persistent local OAuth tokens. <br>
Mitigation: Keep the service bound to localhost, protect .env and tokens.json, and revoke Google access or stop the systemd service when ongoing calendar access is no longer wanted. <br>
Risk: Unauthenticated local access could expose calendar events if the bridge is reachable by unintended clients. <br>
Mitigation: Enable CALENDAR_BRIDGE_API_KEY where practical and require Authorization: Bearer <key> for event requests. <br>
Risk: The external Calendar Bridge repository and dependencies are outside NVIDIA ownership. <br>
Mitigation: Review the linked repository and its dependencies before installing or running the service. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/DanielKillenberger/gcal-oauth-bridge) <br>
- [Calendar Bridge repository](https://github.com/DanielKillenberger/gcal-oauth-bridge) <br>
- [Google Cloud API credentials](https://console.cloud.google.com/apis/credentials) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline bash commands, HTTP endpoints, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Google OAuth client credentials for initial setup; may require an Authorization bearer token when CALENDAR_BRIDGE_API_KEY is configured.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
