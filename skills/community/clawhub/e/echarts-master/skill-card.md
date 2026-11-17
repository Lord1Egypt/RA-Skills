## Description:

ECharts Master helps agents analyze tabular, JSON, or CSV data and generate professional interactive ECharts HTML visualizations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linux2010](https://clawhub.ai/user/linux2010)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to turn user-provided tables, JSON, CSV, or query results into interactive ECharts charts and local HTML previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated client-side HTML charts may expose any data embedded in the chart file.

Mitigation: Use the skill only with data that is acceptable to place in a client-side HTML chart.

Risk: The preview workflow can start a local web server from a broad working directory.

Mitigation: Serve a dedicated chart-only folder, bind the server to 127.0.0.1, and stop it after previewing.

Risk: The documented npx preview option may fetch an unpinned package.

Mitigation: Avoid the npx option unless the package source and version are controlled.

## Reference(s):

- [Chart Design Guide](references/chart-design.md)
- [ClawHub Skill Page](https://clawhub.ai/linux2010/skills/echarts-master)

## Skill Output:

**Output Type(s):** [Analysis, Code, Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with HTML, JavaScript, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local HTML chart files and suggest a local preview workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
