## Description:

Analyze and visualize Excel, CSV, and TSV data with automated statistics, data quality checks, charts, and structured insight reports in Markdown or HTML.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cqdev-ai](https://clawhub.ai/user/cqdev-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operators use this skill to inspect structured spreadsheet data, profile quality issues, generate charts, and produce concise insight reports for downstream review or decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe local output handling could write generated files outside the intended folder.

Mitigation: Run the skill in a contained working directory and choose a dedicated output directory before generating analysis, chart, or report files.

Risk: HTML reports created from untrusted spreadsheet data may be risky until escaping and chart filename sanitization are fixed.

Mitigation: Avoid untrusted datasets, prefer Markdown output when possible, and review or sanitize generated HTML before sharing it.

Risk: Reproducibility may vary without fully pinned dependencies or a lockfile.

Mitigation: Install in an isolated environment and use pinned dependency versions or a lockfile for repeatable runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cqdev-ai/skills/excel2insights-pro)
- [Demo walkthrough](artifact/references/demo-walkthrough.md)
- [Demo report preview](artifact/references/demo-report-preview.html)

## Skill Output:

**Output Type(s):** [text, markdown, json, files, shell commands, configuration, guidance]

**Output Format:** [Terminal text, JSON analysis summaries, PNG chart files, and Markdown or HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written to caller-selected local paths; generated reports should be reviewed before sharing.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
