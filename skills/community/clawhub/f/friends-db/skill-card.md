## Description: <br>
Query and maintain Alex's local friends database stored in a private SQLite file under the OpenClaw workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexuser](https://clawhub.ai/user/alexuser) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to look up and maintain private friend and contact records, including contact methods, relationship notes, interaction cadence, and local activity suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive personal contact, relationship, and calendar-derived data. <br>
Mitigation: Install only when a persistent local friends/contact CRM is desired, keep the database and backups private, and return only the fields needed for the current task. <br>
Risk: Migration with --replace-with-stub intentionally replaces the prior friends.md source with a stub after import. <br>
Mitigation: Run that migration option only after confirming the replacement is intended and preserving the generated backup. <br>
Risk: Calendar sync can import personal interaction history from the configured calendar account and date range. <br>
Mitigation: Check the calendar account, calendar ID, and sync date range before running sync-calendar. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with shell command snippets and local command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local SQLite database and returns only task-relevant contact fields unless the user asks for broader output.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
