## Description: <br>
Calendar and task management via CalDAV protocol. Query, create, edit, and delete calendar events and todos. Free/busy query, multi-account support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gzlicanyi](https://clawhub.ai/user/gzlicanyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, developers, and automation agents use this skill to manage CalDAV calendars and tasks across supported providers, including querying availability and creating, updating, or deleting events and todos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has read, create, update, and delete access to events and todos in configured CalDAV accounts. <br>
Mitigation: Review requested account and calendar targets before running write or delete commands. <br>
Risk: The skill stores credentials locally in configuration files and sync data in a local cache. <br>
Mitigation: Prefer app-specific passwords or authorization codes, restrict local file permissions, and remove local configuration or cache files when they are no longer needed. <br>
Risk: Custom CalDAV server URLs can expose credentials or calendar data if insecure endpoints are used. <br>
Mitigation: Use HTTPS-only CalDAV URLs and verify the server URL before configuring the skill. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/gzlicanyi/caldav-sync) <br>
- [Google App Passwords](https://myaccount.google.com/apppasswords) <br>
- [Apple App-Specific Passwords](https://appleid.apple.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, update, delete, and cache calendar events and todos in configured CalDAV accounts.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
