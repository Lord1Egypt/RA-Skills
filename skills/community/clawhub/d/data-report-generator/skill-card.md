## Description:

Automatically analyzes CSV or Excel files and generates professional data analysis reports with charts, summaries, and insights as Word (.docx) or PDF outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suntianchong](https://clawhub.ai/user/suntianchong)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and analysts use this skill to turn uploaded CSV, TSV, or Excel data into structured business reports with profiling, charts, insights, and recommendations. It is suited to operations, sales, marketing, finance, and similar tabular reporting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask the agent to install Python packages with --break-system-packages or install OS fonts, which can alter a shared machine.

Mitigation: Run it in an isolated virtual environment or container, and avoid system-level installation commands on shared hosts.

Risk: Generated charts and reports may retain sensitive spreadsheet contents or derived sensitive data.

Mitigation: Review input spreadsheets and generated output files before sharing, and store outputs only in approved locations.

Risk: Fixed or shared output paths can expose generated reports to other workflows or users on the same environment.

Mitigation: Write report artifacts to a controlled per-user output directory and clean temporary chart files after delivery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/suntianchong/skills/data-report-generator)
- [Chart Styling Reference](references/chart-styling.md)
- [General Analysis Reference](references/general.md)
- [PDF Generation Fallback](references/pdf-fallback.md)
- [Sales & Performance Analysis Reference](references/sales-analysis.md)
- [Segmentation Analysis Reference](references/segmentation.md)
- [Statistical Analysis Reference](references/statistical.md)
- [Time Series Analysis Reference](references/time-series.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks; generated Word (.docx), PDF, and chart image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a brief chat summary alongside generated report artifacts when files are delivered.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
