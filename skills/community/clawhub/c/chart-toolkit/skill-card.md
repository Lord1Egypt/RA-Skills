## Description:

Create and export line, bar, pie, scatter, heatmap, candlestick, dashboard, and report visualizations using Python charting libraries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiuwenxi416488212-ship-it](https://clawhub.ai/user/qiuwenxi416488212-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and operations teams use this skill to generate Python charting code, dashboards, and exportable visualization reports from structured data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chart and report exports can overwrite or place files in unintended locations when output paths or filenames are not chosen carefully.

Mitigation: Run the skill in a normal project workspace, use explicit output directories, and choose unique filenames for generated artifacts.

Risk: Untrusted labels, table values, or report names may be embedded in generated HTML snippets.

Mitigation: Escape HTML content and validate paths before using untrusted input in HTML reports or dashboards.

Risk: README mentions database and Feishu imports that are not part of the reviewed chart toolkit behavior.

Mitigation: Treat those integrations as out of scope unless they receive separate review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiuwenxi416488212-ship-it/skills/chart-toolkit)
- [README.md](artifact/README.md)
- [README_CN.md](artifact/README_CN.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python and shell code blocks; generated PNG, HTML, PDF, and chart artifact paths when executed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may depend on optional visualization packages such as Plotly, Kaleido, WordCloud, and Folium.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
