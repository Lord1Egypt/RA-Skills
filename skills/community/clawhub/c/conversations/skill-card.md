## Description: <br>
Imports OpenClaw session JSONL files into a local SQLite database and provides FTS5-backed conversation search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shu0yu](https://clawhub.ai/user/shu0yu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to import local chat session history into a searchable SQLite database and query past conversations from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local conversations.db database can contain sensitive chat history, including personal data, credentials, or confidential work. <br>
Mitigation: Store the database in a protected location, restrict access, and delete or rotate it when the imported history is no longer needed. <br>
Risk: The cron example can continue importing new conversations over time, expanding the amount of sensitive data retained locally. <br>
Mitigation: Enable scheduled imports only after confirming the retention behavior is acceptable for the workspace. <br>


## Reference(s): <br>
- [Database Schema](references/schema.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files, Text] <br>
**Output Format:** [Markdown instructions with inline shell commands; scripts write SQLite data and print query results as text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates a local conversations.db database; query output is limited by the optional result limit argument.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
