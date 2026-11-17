## Description:

Excel工作室 helps agents generate Excel-oriented data tables, reports, charts, statistical summaries, and structured outputs for office automation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, office automation users, and teams use this skill to ask an agent for spreadsheet data processing, report generation, chart output, and data analysis guidance in Chinese or English.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests read, write, and shell command access for a broad spreadsheet/reporting workflow.

Mitigation: Restrict use to explicit spreadsheet or report tasks and require approval before shell commands run or files are written.

Risk: The skill may process sensitive datasets or API keys during office automation tasks.

Mitigation: Avoid providing sensitive datasets or API keys unless necessary, keep credentials in environment variables, and review outputs for secret exposure.

Risk: The evidence describes the skill purpose as broad, inconsistent, and under-scoped.

Mitigation: Provide clear task scope, expected input data, desired workbook/report/chart format, and review generated results before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/thcjp/skills/excel-craft)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON examples, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce spreadsheet/report guidance, structured processing results, chart file descriptions, and API key configuration instructions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
