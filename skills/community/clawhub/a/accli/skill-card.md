## Description:

Apple Calendar CLI helps agents use the accli command-line tool on macOS to list calendars, view events, create, update, delete events, and check free/busy availability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joargp](https://clawhub.ai/user/joargp)

### License/Terms of Use:


## Use Case:

Employees, external users, and developers use this skill to inspect Apple Calendar schedules, find availability, and manage calendar events from an agent on macOS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a globally installed third-party npm CLI with access to Apple Calendar.

Mitigation: Verify the npm package and source before installation, pin a reviewed version, and prefer running under a non-admin macOS account.

Risk: Calendar create, update, and delete commands can change or remove user calendar data.

Mitigation: Limit calendar and date ranges where practical, confirm create and update details with the user, and require explicit confirmation before delete operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joargp/skills/accli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands typically use the --json flag for programmatic parsing.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
