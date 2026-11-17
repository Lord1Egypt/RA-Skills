## Description:

Excel 表格去重清洗。自动去除多余空格、全角字符转半角、标准化手机号和身份证号、按关键列（姓名/手机号/编号）去重，并生成清洗报告 sheet。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dont4getme-2](https://clawhub.ai/user/dont4getme-2)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this Chinese-language skill to clean uploaded Excel workbooks, standardize common contact-list fields, remove duplicate rows, and summarize the cleanup results without modifying the original file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises CSV handling, but the inspected script loads Excel workbooks with openpyxl and expects .xlsx input.

Mitigation: Use .xlsx files for this release, or convert CSV data to an Excel workbook before running the script.

Risk: Automatically selected deduplication keys may remove rows the user intended to keep.

Mitigation: Confirm the key columns before execution and pass an explicit --key value when the correct deduplication fields are known.

Risk: Cleaning contact-list fields can affect sensitive personal data such as phone numbers and ID numbers.

Mitigation: Run the skill only on appropriate local copies, keep the original file unchanged, and review the generated cleaning report before using the cleaned workbook.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dont4getme-2/skills/excel)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Markdown, Guidance]

**Output Format:** [Markdown guidance with inline shell command and generated .xlsx workbook output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a new cleaned workbook containing a cleaned-results sheet and a cleaning-report sheet.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
