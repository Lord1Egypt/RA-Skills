## Description: <br>
Data visualization tool producing SVG charts, ASCII charts, HTML chart files, tables, sparklines, gauges, and other visualizations from raw numbers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shendingyi](https://clawhub.ai/user/shendingyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to turn structured numeric data into terminal charts, SVG charts, HTML chart files, tables, dashboards, progress bars, and compact trend summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chart generation can write SVG or HTML files to local paths, which may expose sensitive input data if files are created in shared or synced locations. <br>
Mitigation: Specify intended output paths, review generated files before sharing, and avoid using sensitive datasets unless local storage of the chart output is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shendingyi/alex-chart-generator) <br>
- [Data visualization best practices](tips.md) <br>
- [Feedback and feature requests](https://bytesagain.com/feedback) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, files, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated outputs may be ASCII text, SVG files, or HTML files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chart commands accept numeric values, label:value pairs, delimited table rows, titles, colors, and output file paths.] <br>

## Skill Version(s): <br>
2.3.4 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
