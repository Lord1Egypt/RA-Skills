## Description: <br>
Convert CSV files to professionally formatted Excel workbooks with Chinese character support, automatic formatting, and multi-sheet capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuanguan2020](https://clawhub.ai/user/xuanguan2020) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to convert one or more CSV files into formatted Excel workbooks, including multi-sheet reports and files containing Chinese or other non-ASCII text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The converter reads local CSV files and writes an Excel workbook to the requested path. <br>
Mitigation: Provide only the intended input files and output path, and review the generated workbook before sharing it. <br>
Risk: The script depends on openpyxl from the Python package ecosystem. <br>
Mitigation: Install openpyxl from a trusted package index or approved internal mirror before running the conversion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuanguan2020/csvtoexcel) <br>
- [Publisher profile](https://clawhub.ai/user/xuanguan2020) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated Excel workbook files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local CSV inputs and writes .xlsx workbook files; requires openpyxl to be installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
