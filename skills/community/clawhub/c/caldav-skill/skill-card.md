## Description:

Manage CalDAV calendars and events, with special support for Radicale server. Use when the user wants to create, update, delete, or query calendar events, manage calendars, or configure/administer a Radicale CalDAV server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chakyiu](https://clawhub.ai/user/chakyiu)

### License/Terms of Use:


## Use Case:

Developers, operators, and administrators use this skill to automate CalDAV calendar, event, and todo workflows and to manage Radicale server configuration, users, status checks, and storage validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles CalDAV credentials and calendar data.

Mitigation: Use HTTPS except for loopback testing, prefer environment-backed secrets or a protected config file, and avoid pasting real passwords into curl examples.

Risk: Calendar, event, and todo commands can delete or update user data.

Mitigation: Review each destructive operation before execution, avoid force flags unless the target is confirmed, and export or back up important calendars before bulk changes.

Risk: Radicale workflows include server-administration actions such as service checks, user-file changes, and storage validation.

Mitigation: Run administrative commands only on the intended host with appropriate privileges, inspect the active Radicale configuration first, and treat htpasswd or system service changes as explicit administrator actions.

## Reference(s):

- [ClawHub Caldav Skill Page](https://clawhub.ai/chakyiu/skills/caldav-skill)
- [python-caldav Project](https://github.com/python-caldav/caldav)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python examples, configuration snippets, and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a configured CalDAV or Radicale environment; scripts may read or modify calendars, events, todos, users, and server state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
