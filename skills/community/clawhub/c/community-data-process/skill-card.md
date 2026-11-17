## Description:

Processes BAIC community export workbooks by cleaning selected group-label data, checking key metrics, and merging the result into a BI upload workbook using the source file creation date as the statistics date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuhui435](https://clawhub.ai/user/yuhui435)

### License/Terms of Use:

MIT-0

## Use Case:

Operations users and data analysts use this skill to automate daily cleaning, validation, and incremental BI workbook preparation for BAIC community group exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow automatically reads and writes Excel files in Downloads and creates BI upload workbooks from local source data.

Mitigation: Review generated workbooks before upload and add output confirmation or overwrite safeguards before operational use.

Risk: Spreadsheet content from source workbooks may carry unsafe formulas or misleading values into generated outputs.

Mitigation: Use spreadsheet protections and add formula sanitization before processing untrusted source data.

Risk: Validation safeguards are weak for an automated business workflow.

Mitigation: Block uploads on audit failures and require review of generated files before downstream BI use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuhui435/skills/community-data-process)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Text]

**Output Format:** [Excel workbooks and plain-text audit or status reports with console output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes cleaned and merged .xlsx files plus a text result report in the user's Downloads folder.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
