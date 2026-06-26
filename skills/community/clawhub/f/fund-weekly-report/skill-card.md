## Description: <br>
Generates Chinese fund weekly report Word documents from user-provided Excel data for active equity, fixed income, index funds, FOF, QDII, REITs, fund issuance, and related weekly performance analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yujing2013](https://clawhub.ai/user/Yujing2013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts and agents use this skill to turn fund weekly return spreadsheets, optional ETF flow spreadsheets, and reporting templates into structured Chinese weekly fund reports. It is intended for local document generation from files the user provides. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes a generated Word document to a user-selected path, which could overwrite an existing file if the same output name is reused. <br>
Mitigation: Choose an output filename inside the working directory and check for existing files before running report generation. <br>
Risk: Report content depends on the accuracy and intended scope of the Excel spreadsheets and optional template or news files supplied by the user. <br>
Mitigation: Provide only the spreadsheet, template, and news files intended for analysis, and review the generated report before relying on it. <br>
Risk: Spreadsheet parsing and report wording may produce misleading analysis if the input workbook layout differs from the documented sheet and column mappings. <br>
Mitigation: Validate input workbooks against the documented data mapping and spot-check generated statistics, date ranges, and fund names. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Yujing2013/fund-weekly-report) <br>
- [Chapter Breakdown](references/chapter_breakdown.md) <br>
- [Data Mapping](references/data_mapping.md) <br>
- [Data Processing Logic](references/data_processing_logic.md) <br>
- [ETF Flow Usage](references/etf_flow_usage.md) <br>
- [Template Usage](references/template_usage.md) <br>
- [Writing Templates V3 Learned](references/writing_templates_v3_learned.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance and Python scripts that generate Word .docx reports from Excel inputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-provided .xlsx or .xls inputs and writes a Word report to the selected output path.] <br>

## Skill Version(s): <br>
1.8.3 (source: server release metadata; artifact frontmatter says 1.8.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
