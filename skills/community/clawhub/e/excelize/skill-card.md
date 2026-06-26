## Description: <br>
Helps agents read and write Excel-compatible spreadsheet files, including XLAM, XLSM, XLSX, XLTM, and XLTX workbooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuri](https://clawhub.ai/user/xuri) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to install and apply the excelize Python package for creating, reading, modifying, charting, and embedding images in Excel-compatible spreadsheets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the referenced PyPI package may introduce dependency or supply-chain risk in sensitive environments. <br>
Mitigation: Trust and pin the excelize package version before installation. <br>
Risk: Generated spreadsheet operations may overwrite files if an agent uses an unintended output path. <br>
Mitigation: Provide explicit input and output paths and keep backups for important spreadsheets. <br>


## Reference(s): <br>
- [Excelize Python Documentation](https://xuri.me/excelize-py/) <br>
- [excelize-py Source Code](https://github.com/xuri/excelize-py) <br>
- [excelize-py Docs Repository](https://github.com/xuri/excelize-py-docs) <br>
- [excelize PyPI Package](https://pypi.org/project/excelize) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify local spreadsheet files when the generated code is executed.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
