## Description:

Fetches Fortune China 500 ranking data for requested years, checks release availability, and produces an Excel workbook with rank, company, industry, revenue, and source timestamp.

This skill is for research and development only.

## Publisher:

[hyqdq888](https://clawhub.ai/user/hyqdq888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts can use this skill to retrieve Fortune China 500 company ranking data by year and generate a local Excel workbook for review or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote webpage content is written into an Excel workbook without spreadsheet formula neutralization.

Mitigation: Treat generated workbooks as untrusted, review the workbook before opening or sharing it, and add formula neutralization before operational use.

Risk: The skill fetches public ranking data from an external website at runtime.

Mitigation: Install and run it only in environments where outbound access to caifuzhongwen.com and local workbook creation are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hyqdq888/skills/fortune-china500-skill)
- [Fortune Chinese data source](https://www.caifuzhongwen.com)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, guidance]

**Output Format:** [Markdown guidance and Python-generated Excel files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local .xlsx workbooks containing remote ranking data and source timestamps.]

## Skill Version(s):

1.0.1 (source: server release metadata, released 2026-03-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
