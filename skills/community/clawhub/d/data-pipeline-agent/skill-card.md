## Description: <br>
Builds ETL pipelines for business data, including API extraction, data cleaning, transformation, warehouse loading, recurring syncs, and data quality checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and operations teams use this skill to design ETL workflows that extract data from APIs or files, clean and normalize it, merge sources, load outputs into warehouses or spreadsheets, and schedule recurring syncs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ETL workflows may request broad access to APIs, files, sheets, or database tables. <br>
Mitigation: Define the allowed sources and destinations before use, and provide least-privilege credentials only for that scope. <br>
Risk: Database load examples can overwrite or replace existing tables if used without safeguards. <br>
Mitigation: Use staging tables, backups, row-count validation, and explicit approval before replace-style loads. <br>
Risk: Pipeline examples involve credentials for business systems and financial data sources. <br>
Mitigation: Keep secrets in environment variables or a vault, and test pipelines on sample data before full runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/data-pipeline-agent) <br>
- [Publisher profile](https://clawhub.ai/user/samledger67-dotcom) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ETL patterns, data quality checks, scheduling examples, and database load guidance.] <br>

## Skill Version(s): <br>
98.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
