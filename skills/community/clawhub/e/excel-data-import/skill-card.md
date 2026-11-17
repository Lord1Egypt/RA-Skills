## Description:

Import, merge, and transform Excel or CSV data using YAML-driven field mapping, validation, batch processing, and incremental updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aqbjqtd](https://clawhub.ai/user/aqbjqtd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users use this skill to configure and run repeatable imports from Excel or CSV sources into target workbooks, including directory batches, multiple sources, mapped fields, validations, and update-or-append workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet imports can expose or duplicate sensitive data through output workbooks, backups, logs, and reports.

Mitigation: Run the skill in a controlled workspace using copies of source files, restrict access to generated files, and remove or protect backups, logs, and reports after review.

Risk: Documented safety controls may be weaker than expected, including dry-run behavior and encrypt or custom validation behavior.

Mitigation: Verify behavior on non-sensitive sample files before production use and do not rely on those controls until the implementation has been reviewed and fixed.

Risk: Untrusted spreadsheets may contain formula-like values or malformed data that could be carried into generated workbooks.

Mitigation: Reject or neutralize formula-like values before import and review validation failures before opening or distributing generated workbooks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aqbjqtd/skills/excel-data-import)
- [Data Mapping Guide](references/data-mapping-guide.md)
- [Advanced Features](references/advanced-features.md)
- [Auto Header Detection](references/auto_header_detection.md)
- [Quickstart](references/quickstart.md)
- [Workflow](references/workflow.md)
- [Best Practices](references/best-practices.md)
- [Error Handling](references/error-handling.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Configuration, Shell commands, Code, Markdown, Guidance]

**Output Format:** [Markdown guidance with YAML configuration examples and shell commands; the bundled scripts produce spreadsheet files, backups, logs, and JSON reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write or update local workbook files and create backup, log, and import report files when executed.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
