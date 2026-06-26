## Description: <br>
Microsoft 365 / Outlook CLI for calendar and email. Use when managing Outlook calendar (view, create, update, delete events, find meeting times, respond to invitations), sending/reading emails, or searching for people/rooms in the organization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foeken](https://clawhub.ai/user/foeken) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, assistants, and developers use this skill to operate Outlook calendar, email, people search, and room search through the clippy CLI. It is useful for scheduling meetings, responding to invitations, reading or sending mail, and finding meeting times. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate through a signed-in Microsoft 365 account and change mail or calendar data. <br>
Mitigation: Require explicit user confirmation before sending, forwarding, reply-all, deleting, moving, or downloading sensitive items. <br>
Risk: The external clippy CLI and its dependencies run outside the skill context. <br>
Mitigation: Install only when the publisher and external CLI are trusted, and review the external project before running bun install. <br>
Risk: Keepalive can preserve an authenticated browser session in the background. <br>
Mitigation: Enable keepalive only when needed, monitor the health file for stale sessions, and ensure the background service can be stopped. <br>


## Reference(s): <br>
- [Clippy ClawHub listing](https://clawhub.ai/foeken/clippy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with CLI command examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external clippy binary and a signed-in Microsoft 365 browser session; some commands can change calendar, email, and session state.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
