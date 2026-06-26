## Description: <br>
Automates reading, writing, merging, transforming, and validating Excel (.xlsx/.xls) files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cheneycheung](https://clawhub.ai/user/cheneycheung) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operations users use this skill to automate local Excel and CSV workflows such as merging sheets, filtering rows, validating tables, aggregating values, converting formats, and generating reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spreadsheet commands can modify important workbooks, including in-place sheet renaming or formatting when no output path is provided. <br>
Mitigation: Run the skill on copies of important workbooks or require explicit output paths before applying changes. <br>
Risk: Filtering, merging, deduplication, aggregation, or format conversion can change row counts, values, formulas, or formatting in ways that affect business decisions. <br>
Mitigation: Review generated files, compare row counts or key columns against the source data, and keep source files available for rollback. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cheneycheung/automate-excel-0-1-3) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/cheneycheung) <br>
- [reference.md](artifact/reference.md) <br>
- [examples.md](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance, files] <br>
**Output Format:** [Markdown with inline Python and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local .xlsx, .xls, and .csv files when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata version 0.1.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
