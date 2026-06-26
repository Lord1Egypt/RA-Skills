## Description: <br>
Ask Data helps an agent answer natural-language questions about local Excel spreadsheets by reading user-approved files, generating data queries, and returning tables, visualizations, and insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[15028191702](https://clawhub.ai/user/15028191702) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, operators, and business users can use this skill to ask Chinese natural-language questions about local Excel files, inspect sheet structure, run filtered or aggregated queries, and receive concise result reports with follow-up analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local Excel files selected by the user, which may contain sensitive or unnecessary data. <br>
Mitigation: Confirm file paths before use and avoid running it on spreadsheets containing data that is not needed for the question. <br>
Risk: Large spreadsheets can be slow or resource-intensive to inspect and query. <br>
Mitigation: Prefer smaller extracts for exploratory questions and warn users when files exceed the documented large-file threshold. <br>
Risk: Generated analysis can be misleading if the requested column names, date ranges, or aggregations do not match the workbook. <br>
Mitigation: Show the interpreted query, sheet, filters, and aggregation choices before presenting conclusions. <br>


## Reference(s): <br>
- [Query examples](references/query-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/15028191702/ask-data) <br>
- [Publisher profile](https://clawhub.ai/user/15028191702) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports with JSON query snippets, shell command examples, tables, chart descriptions, and concise data insights.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads only user-selected Excel files and returns local analysis results without modifying the source spreadsheet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
