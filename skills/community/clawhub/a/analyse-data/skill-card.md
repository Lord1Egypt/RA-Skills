## Description:

Analyse Data helps agents use ChartGen to analyze spreadsheet or text requests and produce charts, dashboards, diagrams, reports, and PPT outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chartgen-ai](https://clawhub.ai/user/chartgen-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route data analysis, charting, dashboard, diagram, report, and presentation generation requests through ChartGen. It supports text-only analysis and spreadsheet uploads for CSV, TSV, XLS, and XLSX files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User prompts and supported spreadsheet files may be sent to the external ChartGen service.

Mitigation: Use only when sharing that data with ChartGen is approved, and avoid secrets, regulated data, or sensitive business data unless policy permits it.

Risk: The release evidence reports unsafe execution and download patterns that deserve review before installation.

Mitigation: Prefer runtimes that pass tool arguments without shell interpolation and restrict outbound downloads to trusted ChartGen origins.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chartgen-ai/skills/analyse-data)
- [ChartGen API Setup](https://chartgen.ai/chat)
- [ChartGen Service](https://chartgen.ai)
- [Skill Upgrade Procedure](references/upgrade-skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown responses with JSON tool results and generated artifact file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return text_reply, edit_url, image paths, PPT previews and downloads, or spreadsheet/file downloads depending on the ChartGen task result.]

## Skill Version(s):

1.0.4 (source: release evidence and tool version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
