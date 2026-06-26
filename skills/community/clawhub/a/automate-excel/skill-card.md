## Description: <br>
Automates reading, writing, merging, transforming, and validating Excel (.xlsx/.xls) files for spreadsheet, CSV-to-Excel, batch processing, and report-generation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zways](https://clawhub.ai/user/zways) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and operations teams use this skill to automate routine Excel and CSV tasks such as merging sheets, converting files, filtering rows, deduplicating data, aggregating tables, validating workbooks, applying formatting, and filling report templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spreadsheet files may be overwritten when scripts are run without explicit output paths. <br>
Mitigation: Use explicit --output paths where supported and keep backups of important workbooks before running write or formatting operations. <br>
Risk: The skill reads and writes local Excel and CSV files as part of normal operation. <br>
Mitigation: Run the skill only on intended local files and review paths, sheet names, and filters before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zways/automate-excel) <br>
- [Publisher profile: zways](https://clawhub.ai/user/zways) <br>
- [Reference guide](reference.md) <br>
- [Examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with command examples and generated Excel or CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local spreadsheet operations and may write output workbooks or CSV files.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
