## Description:

Read your Apple Books library, highlights, notes, and reading progress directly from the local SQLite databases on macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexissan](https://clawhub.ai/user/alexissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users on macOS use this skill to let an agent inspect local Apple Books library data, highlights, notes, reading progress, collections, and reading statistics through SQLite queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Full Disk Access for the process querying local Apple Books data, which can expose private library, highlight, note, and reading progress information.

Mitigation: Install and run it only in a trusted agent environment, and grant Full Disk Access only to the specific process that needs to query Apple Books data.

Risk: The sample SQLite commands are described as read-only but are not technically constrained to read-only execution.

Mitigation: Run sqlite3 in read-only mode where possible and execute only SELECT-style queries against Apple Books databases.

Risk: Search terms and asset IDs shown in sample queries can be directly substituted into SQL examples.

Mitigation: Escape or parameterize user-provided search terms and asset IDs before execution instead of inserting raw text into SQL.

Risk: Writing to Apple Books databases can corrupt local data or create iCloud sync issues.

Mitigation: Do not run INSERT, UPDATE, or DELETE statements against these databases; keep interactions limited to inspection queries.

## Reference(s):

- [ClawHub Apple Books skill page](https://clawhub.ai/alexissan/skills/apple-books)
- [Skill homepage](https://clawhub.ai/alexissan/apple-books)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance with shell and SQL command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [macOS only; requires sqlite3 and Full Disk Access for the process querying Apple Books data.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
