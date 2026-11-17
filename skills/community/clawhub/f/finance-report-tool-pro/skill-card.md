## Description:

财报分析专业版 helps agents process financial reports in batches, extract content with OCR, compare industry benchmarks, run forecasts, and generate reports in PDF, DOCX, HTML, and Markdown formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External finance analysts, investment research teams, and institutions use this skill to analyze annual reports, compare companies against industry benchmarks, forecast financial trends, and produce formatted analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, write, and command execution authority for financial-file processing.

Mitigation: Use it only on files and output directories explicitly selected by the operator, and require confirmation before running batch jobs or generated shell commands.

Risk: Security evidence notes inconsistent guidance about local-only processing versus external API or network use.

Mitigation: Do not permit network callbacks or external API use unless the publisher clarifies exactly what data is sent and where.

Risk: Financial analysis, OCR, benchmarking, and forecasting outputs may be incomplete or misleading without human review.

Mitigation: Have qualified analysts review extracted data, assumptions, comparable-company choices, and forecast conclusions before business or investment use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/finance-report-tool-pro)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate report files in HTML, PDF, DOCX, and Markdown depending on the requested workflow.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
