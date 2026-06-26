## Description: <br>
Extract calendar events and deadlines from emails, present them for user review, and create or update calendar entries with duplicate detection, event tracking, pending invite reminders, and undo support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a2mus](https://clawhub.ai/user/a2mus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees and individual users can use this skill to turn event-related emails into calendar entries after review. It is designed for Gmail and Google Calendar workflows, with direct inbox scanning or forwarded-email processing modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read email broadly and create, update, or delete calendar entries. <br>
Mitigation: Grant access only in an intended mailbox and calendar, prefer forwarded-only mode during initial use, and require explicit approval before creating or updating events. <br>
Risk: Automatic email disposition can mark messages as read or archive them after processing. <br>
Mitigation: Disable mark-read, archive, and auto-dispose settings until the workflow has been tested on non-sensitive messages. <br>
Risk: Attendee notifications and deadline emails can send messages to other people or to the configured user. <br>
Mitigation: Review attendee lists and notification settings before enabling send-updates or deadline notification behavior. <br>
Risk: The skill persists email-derived activity, event tracking, pending invite, and changelog records locally. <br>
Mitigation: Avoid using the skill on mailboxes containing sensitive content unless local memory storage and retention are acceptable. <br>
Risk: Evidence identifies a shell-execution bug in lookup validation on writable tracking data. <br>
Mitigation: Patch the lookup validation issue before using validation features with writable tracking data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/a2mus/doro-email-to-calendar) <br>
- [Setup Guide](SETUP.md) <br>
- [CLI Reference](references/gog-commands.md) <br>
- [Extraction Patterns](references/extraction-patterns.md) <br>
- [Workflow Example](references/workflow-example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured event summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update calendar entries, send email notifications, mark or archive emails, and persist local tracking records when run with the required tools and permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
