## Description: <br>
Data visualization tool that produces terminal ASCII charts and exportable HTML or SVG chart files for bar charts, line charts, pie charts, tables, sparklines, gauges, dashboards, progress bars, heatmaps, and trend summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongbai233](https://clawhub.ai/user/kongbai233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other external users can use this skill to generate quick command-line visualizations and shareable HTML or SVG chart artifacts from simple numeric or label-value data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local chart files may be created in user-selected paths or the chart-generator data directory. <br>
Mitigation: Run commands in an intended working directory and review output paths before sharing or retaining generated files. <br>
Risk: Chart titles, labels, and history can contain business-sensitive information. <br>
Mitigation: Avoid secrets or highly sensitive business details in chart inputs, and delete generated files or local history when retention is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kongbai233/chart-generator-2-0-0) <br>
- [Publisher profile](https://clawhub.ai/user/kongbai233) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, files] <br>
**Output Format:** [Markdown guidance with Bash command examples; generated terminal text, HTML files, and SVG files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local Bash and embedded Python chart generation; some commands write chart files or local chart history.] <br>

## Skill Version(s): <br>
2.0.0 (source: artifact frontmatter and artifact/_meta.json; ClawHub release version 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
