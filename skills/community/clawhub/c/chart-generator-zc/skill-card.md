## Description:

Generates terminal-friendly ASCII charts and standalone SVG or HTML chart files from simple command-line data inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lean-zhouchao](https://clawhub.ai/user/lean-zhouchao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operators use this skill to generate quick bar, line, pie, table, sparkline, dashboard, heatmap, progress, SVG, and HTML visualizations from command-line data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML or SVG can include unescaped user-provided labels, CSV data, or titles, making shared chart files unsafe to open when inputs are untrusted.

Mitigation: Review chart inputs before generation, avoid opening or publishing generated HTML/SVG from untrusted data, and escape markup before sharing generated files.

Risk: One included script can keep local chart history under the user's data directory.

Mitigation: Set CHART_DIR to an appropriate location or clear the chart history when generated chart metadata should not persist.

## Reference(s):

- [Data Visualization Best Practices](tips.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated ASCII, SVG, or HTML chart files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write chart files to the working directory or user data directory depending on the invoked script.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.1 and artifact _meta reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
