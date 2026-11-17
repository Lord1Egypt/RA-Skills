## Description:

Terminal ASCII chart toolkit. Create bar charts, sparklines, histograms, and gauges from CSV or JSON data in the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners use this skill to inspect CSV or JSON files, generate terminal charts, summarize numeric fields, and export simple SVG or HTML reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML or SVG reports can preserve unsafe markup from untrusted CSV data.

Mitigation: Use trusted or sanitized input data and avoid opening exported HTML or SVG reports from untrusted sources until output escaping is implemented.

Risk: Export commands write derived .svg or .html files and may replace existing reports.

Mitigation: Run exports in a scratch directory or check for existing output files before invoking export commands.

## Reference(s):

- [Data Visualizer on ClawHub](https://clawhub.ai/xueyetianya/skills/data-visualizer)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands and terminal, CSV, SVG, or HTML outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a local history log under DATAVIZ_DIR and may create derived .svg or .html export files.]

## Skill Version(s):

3.0.1 (source: server release metadata; artifact frontmatter reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
