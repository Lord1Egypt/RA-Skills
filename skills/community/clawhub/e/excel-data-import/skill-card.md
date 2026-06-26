## Description: <br>
Import, merge, and transform data from Excel (.xlsx/.csv) files using YAML-driven configuration with field mapping, validation, batch processing, and incremental updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aqbjqtd](https://clawhub.ai/user/aqbjqtd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and data operators use this skill to create YAML import configurations and run local spreadsheet imports that map, validate, merge, and update Excel/CSV data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spreadsheet inputs, generated backups, logs, and reports may contain sensitive or personal data. <br>
Mitigation: Process only needed spreadsheet paths, avoid passwords or unnecessary personal data, and restrict access to generated backups, logs, and reports. <br>
Risk: Import commands can write output spreadsheets and related local files. <br>
Mitigation: Run with --dry-run first, use a dedicated project folder, review the planned output, and keep backups enabled unless there is a clear reason to disable them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aqbjqtd/excel-data-import) <br>
- [Data Mapping Guide](references/data-mapping-guide.md) <br>
- [Advanced Features](references/advanced-features.md) <br>
- [Auto Header Detection](references/auto_header_detection.md) <br>
- [Quickstart](references/quickstart.md) <br>
- [Workflow](references/workflow.md) <br>
- [Best Practices](references/best-practices.md) <br>
- [Error Handling](references/error-handling.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with YAML configuration snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local spreadsheet outputs, backups, logs, and JSON import reports when the generated commands are executed.] <br>

## Skill Version(s): <br>
2.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
