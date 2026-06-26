## Description: <br>
根据财务报表 Excel 文件生成规范化资产负债表，保留模板格式和公式，并按指定规则汇总银行余额、往来款项和经营利润。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[courage-zen](https://clawhub.ai/user/courage-zen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance and operations users can use this skill to turn a workbook containing an asset-liability template, detail sheet, and income statement into a completed balance-sheet workbook for monthly or annual reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads financial Excel files from the workspace. <br>
Mitigation: Use only intended source workbooks, keep sensitive files out of the workspace when possible, and review generated output before sharing it. <br>
Risk: Running without an explicit output path writes the default workbook name and may replace an existing file. <br>
Mitigation: Provide a specific output path or check whether 资产负债表.xlsx already exists before running. <br>
Risk: Generated totals depend on the expected workbook sheets, columns, and category labels. <br>
Mitigation: Confirm the input workbook follows the documented template and validate key totals against source records before relying on the result. <br>


## Reference(s): <br>
- [Balance-sheet generation rules](references/rules.md) <br>
- [ClawHub skill page](https://clawhub.ai/courage-zen/balance-sheet-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Excel workbook (.xlsx) with concise command-line status text when run from a shell] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a source workbook and writes a balance-sheet workbook, defaulting to 资产负债表.xlsx when no output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
