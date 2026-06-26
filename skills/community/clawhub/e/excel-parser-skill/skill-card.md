## Description: <br>
Extracts text and structured table data from Excel files, including .xls, .xlsx, .xlsm, .xltx, and .xltm formats, using python-calamine with xlrd/openpyxl fallback parsing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yejinlei](https://clawhub.ai/user/yejinlei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to parse Excel workbooks, inspect worksheet contents, convert tables to text, and return structured row data for data extraction, report analysis, and content review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The parser can automatically install missing Python packages at runtime, which may alter the active Python environment. <br>
Mitigation: Run the skill in an isolated virtual environment and preinstall pinned dependencies before use. <br>
Risk: Excel files may be untrusted inputs and can contain unexpected or sensitive workbook content. <br>
Mitigation: Process files in a restricted workspace, review source files before parsing, and avoid exposing extracted cell contents outside the intended workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yejinlei/excel-parser-skill) <br>
- [python-calamine](https://github.com/dimastbk/python-calamine) <br>
- [xlrd](https://github.com/python-excel/xlrd) <br>
- [openpyxl documentation](https://openpyxl.readthedocs.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [Plain text summaries and JSON-compatible dictionaries containing worksheet names, rows, row counts, column counts, total cell counts, and parser engine metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Text output displays up to the first 100 rows per sheet; structured output returns parsed worksheet rows and workbook metadata.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
