## Description: <br>
Professional Excel spreadsheet generator for creating formatted spreadsheets, reports, charts, formulas, and multi-sheet workbooks in XLSX, XLS, or CSV formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to turn spreadsheet requirements into local Python-based generation steps for business reports, data analysis workbooks, financial models, inventories, project trackers, and personal tables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Python commands write local spreadsheet files and may handle financial or business data. <br>
Mitigation: Review generated commands and output paths before execution, especially when working with sensitive business data. <br>
Risk: Spreadsheet generation depends on Python packages that may vary across environments. <br>
Mitigation: Pin dependency versions and install them in controlled environments for production or regulated workflows. <br>


## Reference(s): <br>
- [Excel templates reference](artifact/references/templates.md) <br>
- [ClawHub release page](https://clawhub.ai/tobewin/excel-studio) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Files] <br>
**Output Format:** [Markdown with Python and shell code blocks plus generated spreadsheet files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local XLSX, XLS, or CSV outputs; no network calls are indicated by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
