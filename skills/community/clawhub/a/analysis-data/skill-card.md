## Description:

Use this skill to ask ChartGen to create charts, dashboards, diagrams, Gantt views, PPTs, reports, and data analyses from text prompts or selected spreadsheet files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chartgen-ai](https://clawhub.ai/user/chartgen-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users can use this skill to route confirmed analysis and visualization requests to ChartGen, including optional CSV, TSV, XLS, and XLSX files. The skill is suited for generating visual artifacts, analysis summaries, reports, and presentations from user-approved inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confirmed prompts and selected CSV, TSV, XLS, or XLSX files are sent to ChartGen.

Mitigation: Use the skill only with data that is approved for submission to ChartGen, and confirm each request before it is sent.

Risk: Generated artifacts may be downloaded and local HTML content may be prepared for rendering.

Mitigation: Review artifact download and HTML handling before installation, especially in environments with sensitive internal network access or permissive HTML renderers.

Risk: The release security verdict is suspicious because of under-scoped external download and rendering behavior.

Mitigation: Treat the skill as requiring review before deployment and scan or restrict it according to the installing organization's policy.

## Reference(s):

- [ClawHub Analysis Data Skill](https://clawhub.ai/chartgen-ai/skills/analysis-data)
- [ChartGen](https://chartgen.ai)
- [ChartGen API Key Page](https://chartgen.ai/chat)
- [Skill Upgrade Procedure](references/upgrade-skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON tool results and local artifact paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce analysis text, edit links, chart images, dashboard images, PPT previews, PPT downloads, and spreadsheet/file downloads.]

## Skill Version(s):

1.0.6 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
