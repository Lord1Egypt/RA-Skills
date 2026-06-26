## Description: <br>
Excel 数据自动清洗引擎 Pro helps agents clean CSV, XLSX, and JSON datasets by deduplicating records, normalizing formats, handling missing values, classifying rows, validating cross-field logic, and producing quality reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lijinhao123-dot](https://clawhub.ai/user/lijinhao123-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business users, analysts, operations teams, ecommerce sellers, and agents working on their behalf use this skill to inspect messy spreadsheet data, apply common cleaning rules, and generate cleaned files plus data quality reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spreadsheet inputs may contain sensitive business or personal data. <br>
Mitigation: Process only files the user explicitly provides, keep backups of originals, and review cleaned outputs and reports before use. <br>
Risk: Optional web lookup or Feishu export can expose sensitive fields outside the local cleaning workflow. <br>
Mitigation: Do not allow web search or Feishu export for customer, financial, ID, phone, address, or other sensitive data unless the exact fields and destination are approved first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lijinhao123-dot/excel-auto-cleaner-pro) <br>
- [Publisher profile](https://clawhub.ai/user/lijinhao123-dot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown guidance with optional Python data-cleaning code and generated spreadsheet or report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce cleaned XLSX, CSV, or JSON files and Markdown reports from user-provided spreadsheet data.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
