## Description: <br>
Converts bank statement Excel and CSV exports from different banks into a standardized nine-column regulatory reporting format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiqikuaidianpao](https://clawhub.ai/user/qiqikuaidianpao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, accounting, and operations users use this skill to batch standardize bank-statement spreadsheets across banks and accounts, then produce reporting-ready Excel outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bank statements contain financial transaction data, and the generated ZIP contains standardized copies of that data. <br>
Mitigation: Run the converter only in a trusted local environment and handle the output ZIP as sensitive financial data. <br>
Risk: Pointing the converter at a broad folder can include unintended statement files in the output. <br>
Mitigation: Use a narrow input folder containing only the intended bank statement files before running the command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiqikuaidianpao/crc-bank-statement-converter) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, files] <br>
**Output Format:** [Markdown guidance with bash commands; generated ZIP containing standardized XLSX spreadsheets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python3, pip, openpyxl, and xlrd; processes local XLS, XLSX, and CSV statement files from a selected folder.] <br>

## Skill Version(s): <br>
1.5.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
