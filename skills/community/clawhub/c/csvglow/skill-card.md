## Description: <br>
Generate beautiful interactive HTML dashboards from CSV/Excel files with smart insights, auto-detected charts, correlations, and statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ratnaditya-J](https://clawhub.ai/user/Ratnaditya-J) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and data practitioners use csvglow to turn local CSV, TSV, XLS, and XLSX files into self-contained interactive HTML dashboards for visual data exploration and reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports a helper path that can run nested Codex review with sandbox and approval bypass enabled. <br>
Mitigation: Use the scanner guidance: install only from a trusted publisher, and use --no-yolo or AUTOREVIEW_YOLO=0 unless full-access nested review is explicitly intended. <br>
Risk: The skill runs a local csvglow binary over user-provided spreadsheet data. <br>
Mitigation: Verify the installed binary and review generated dashboards before sharing outputs that may include sensitive source data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Ratnaditya-J/csvglow) <br>
- [csvglow Repository](https://github.com/Ratnaditya-J/csvglow) <br>
- [csvglow Issues](https://github.com/Ratnaditya-J/csvglow/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands; generated artifact is self-contained HTML] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the csvglow binary; supports CSV, TSV, XLS, and XLSX inputs, with optional MCP server mode.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter, clawhub.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
