## Description: <br>
Profile messy CSV files, standardize columns, detect data quality issues, and produce a reproducible cleanup plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data analysts, and operations teams use this skill to inspect CSV datasets, normalize schemas, identify data quality issues, and prepare cleanup plans before applying changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script reads local CSV data, which may contain sensitive information. <br>
Mitigation: Run it only on datasets the user intends to inspect locally and avoid sharing generated reports unless their contents have been reviewed. <br>
Risk: The report output path could overwrite an existing file if the user chooses an existing location. <br>
Mitigation: Use a safe new output path when preserving files matters and review proposed cleanup steps before applying changes to original data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/csv-cleanroom) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Data quality checklist](artifact/resources/data_quality_checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional JSON profile files produced by the local helper script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script reads a user-specified CSV path and writes a user-specified local report path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
