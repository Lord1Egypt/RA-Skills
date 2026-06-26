## Description: <br>
Designs refreshable Excel dashboards (Power Query + structured tables + validation + pivot reporting). Use when you need a repeatable weekly KPI workbook that updates from files with minimal manual work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KOwl64](https://clawhub.ai/user/KOwl64) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external operators, and developers use this skill to design repeatable weekly KPI workbooks in Excel with Power Query ingestion, structured tables, validation checks, pivot dashboards, and refresh status reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Power Query snippets or workbook guidance could be applied to the wrong folder or unsuitable business data. <br>
Mitigation: Use a dedicated source folder, review snippets before applying them, and keep visible refresh status checks for row counts, query errors, and latest week coverage. <br>
Risk: PDF or DOCX table extraction can be unreliable for repeatable reporting pipelines. <br>
Mitigation: Require user-provided CSV or XLSX exports when extraction reliability is uncertain, or clearly mark the extraction risk before building the workbook workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KOwl64/excel-weekly-dashboard) <br>
- [Power Query folder ingest template](assets/power-query-folder-ingest-template.pq.md) <br>
- [Weekly refresh checklist](assets/refresh-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with Power Query M snippets and structured workbook guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces plans by default; generates workbook specification, Power Query template, and refresh checklist artifacts only when explicitly requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
