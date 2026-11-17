## Description:

Designs refreshable Excel dashboards with Power Query, structured tables, validation, and pivot reporting for repeatable weekly KPI workbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kowl64](https://clawhub.ai/user/kowl64)

### License/Terms of Use:


## Use Case:

Employees, analysts, and operations teams use this skill to design weekly Excel KPI dashboards that refresh from CSV, XLSX, DOCX-exported table, or PDF-exported table inputs. It helps create repeatable workbook plans, Power Query steps, validation rules, pivot layouts, and refresh checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad Power Query folder path could ingest unrelated personal or business files.

Mitigation: Set the generated folder path to a narrow export directory that contains only the intended weekly source files.

Risk: Incorrect schema, validation, or refresh assumptions could produce misleading KPI reports.

Mitigation: Review generated validation rules, row counts, query errors, and latest-week checks before publishing or sharing dashboard outputs.

Risk: PDF or DOCX table extraction can be unreliable when source tables are not cleanly exported.

Mitigation: Use user-provided CSV or XLSX exports when possible, or clearly mark extraction risk before relying on those inputs.

## Reference(s):

- [Power Query folder ingest template](assets/power-query-folder-ingest-template.pq.md)
- [Weekly refresh checklist](assets/refresh-checklist.md)
- [ClawHub skill page](https://clawhub.ai/kowl64/skills/excel-weekly-dashboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown plans with Power Query M code snippets and optional generated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workbook_spec.md, power_query_steps.pq, and refresh-checklist.md when explicitly requested.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
