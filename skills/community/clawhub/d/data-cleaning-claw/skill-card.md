## Description: <br>
Cleans CSV, Excel, and JSON datasets by removing duplicate rows, filling missing values, standardizing dates, amounts, and phone numbers, stripping HTML noise, validating common fields, and producing cleaned data plus a JSON report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to clean user-provided tabular datasets before analysis, reporting, migration, or quality review. It is suited for workflows that need repeatable deduplication, missing-value handling, format normalization, HTML noise removal, and validation summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill processes files or pasted data supplied by the user and writes cleaned outputs plus a JSON report in the workspace. <br>
Mitigation: Use it only with datasets you are comfortable processing locally, review sensitive or regulated data before cleaning, and choose output paths deliberately. <br>
Risk: Cleaning operations can modify values, fill missing data, remove duplicate rows, and add quality markers, which may affect downstream analysis. <br>
Mitigation: Keep a backup of original datasets and review the cleaning report plus flagged rows before relying on the cleaned output. <br>


## Reference(s): <br>
- [Cleaning Rules](references/cleaning-rules.md) <br>
- [Noise Patterns](references/noise-patterns.md) <br>
- [Data Types](references/data-types.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; cleaned CSV, Excel, or JSON files; JSON cleaning report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a cleaned output file and a sibling .report.json file summarizing row counts and operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
