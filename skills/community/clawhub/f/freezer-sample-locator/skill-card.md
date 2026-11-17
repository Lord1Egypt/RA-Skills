## Description:

Track and retrieve sample locations in -80 C freezers with hierarchical storage organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Lab operations staff, researchers, and developers use this skill to record, search, update, delete, and export freezer sample inventory locations across freezer, level, rack, box, and grid-position coordinates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File export and storage controls may be broader or weaker than the documentation claims.

Mitigation: Run the skill in a dedicated workspace and keep exports in a reviewed directory.

Risk: CSV exports based on untrusted sample metadata may be unsafe to open directly in spreadsheet software.

Mitigation: Use spreadsheet protections or sanitize exported fields before opening CSV files.

Risk: Concurrent use may corrupt or overwrite the JSON sample database.

Mitigation: Use single-writer operation, external locking, and backups until atomic writes and concurrency controls are implemented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/freezer-sample-locator)
- [Publisher profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell and Python code examples; runtime output includes CLI text, JSON records, and CSV exports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains a local JSON sample database and can filter searches or exports by freezer, project, name, or sample ID.]

## Skill Version(s):

0.1.0 (source: release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
