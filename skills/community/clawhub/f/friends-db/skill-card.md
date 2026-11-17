## Description:

Query and maintain Alex's local friends database stored in a private SQLite file under the OpenClaw workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexuser](https://clawhub.ai/user/alexuser)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal-agent operators use this skill to query and maintain a private local contacts and friendship CRM, including contact methods, relationship notes, interaction history, cadence tracking, and activity suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill maintains a persistent private friends CRM containing sensitive contact details, notes, interaction history, and cadence data.

Mitigation: Install only when that persistent local CRM behavior is intended, keep the database in the helper-created private state directory, and return only task-relevant fields.

Risk: Calendar sync processes attendee emails, event titles, descriptions, locations, account configuration, and history through the gog executable on PATH.

Mitigation: Use sync-calendar only after confirming the gog executable and account configuration are trusted, and review the requested calendar scan window before running it.

Risk: Migration with --replace-with-stub rewrites the source friends.md file after importing contacts.

Mitigation: Use --replace-with-stub only after confirming the generated backup and accepting SQLite as the source of truth.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexuser/skills/friends-db)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should be limited to fields needed for the user task and should not dump the full contact database unless explicitly requested.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
