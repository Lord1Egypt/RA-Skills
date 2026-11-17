## Description:

Interact with Calendar Bridge, a self-hosted Node.js service that provides a persistent REST API for Google Calendar events and handles OAuth token refresh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielkillenberger](https://clawhub.ai/user/danielkillenberger)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to set up, call, and troubleshoot a local Calendar Bridge service for checking upcoming Google Calendar events, listing calendars, and managing OAuth-backed calendar access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run unpinned external code persistently with Google Calendar credentials.

Mitigation: Review the repository before installation, pin a trusted revision, and understand the npm dependency risk before running the service.

Risk: Local calendar access can expose calendar data if the service is reachable or weakly protected.

Mitigation: Keep the service bound to localhost and configure a strong CALENDAR_BRIDGE_API_KEY for local API calls.

Risk: OAuth tokens and a persistent user service may remain active after the skill is no longer needed.

Mitigation: Know how to disable the systemd user service and revoke Google OAuth access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danielkillenberger/skills/gcal-oauth-bridge)
- [Calendar Bridge GitHub repository](https://github.com/DanielKillenberger/gcal-oauth-bridge)
- [Google Cloud OAuth credentials](https://console.cloud.google.com/apis/credentials)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, endpoint examples, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local Calendar Bridge endpoints and required or optional environment variables.]

## Skill Version(s):

1.0.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
