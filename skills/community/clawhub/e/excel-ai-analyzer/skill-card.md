## Description:

Automatically analyzes Excel files to summarize structure and statistics, identify anomalies, and generate Markdown reports with data insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oct1st85](https://clawhub.ai/user/oct1st85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and business users can use this skill to inspect local Excel workbooks, produce statistical summaries, flag unusual values, and create Markdown analysis reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill parses user-provided Excel workbooks with an xlsx dependency identified by the security evidence as a known vulnerable parser.

Mitigation: Review the package before installation, avoid untrusted or attacker-supplied spreadsheets, and replace or constrain the xlsx dependency before broader deployment.

Risk: Generated Markdown reports may include workbook-derived content that could be unsafe if rendered directly or passed into another AI workflow.

Mitigation: Treat generated reports as untrusted output, review them before publishing, and sanitize or escape report content before rendering in downstream systems.

Risk: The README installation command uses the latest ClawHub installer version.

Mitigation: Prefer a pinned ClawHub installer version for repeatable installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oct1st85/skills/excel-ai-analyzer)
- [README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)
- [Package manifest](artifact/package.json)
- [Test report](artifact/test-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [JSON result object containing analysis data and a Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a local Excel file path, analyzes the first worksheet, and returns row and column summaries, statistics, anomaly details, and generated insights.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, README, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
