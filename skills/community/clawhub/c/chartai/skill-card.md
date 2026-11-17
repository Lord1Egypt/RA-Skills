## Description:

Use this skill to create visualizations, dashboards, diagrams, Gantt charts, PowerPoint slides, data analysis reports, and spreadsheet-based insights with ChartGen.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chartgen-ai](https://clawhub.ai/user/chartgen-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to submit confirmed ChartGen requests, analyze CSV or spreadsheet files, and return reports, visual artifacts, PowerPoint outputs, and edit links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and spreadsheet contents can be sent to ChartGen.

Mitigation: Confirm each request before submission and avoid sensitive files unless the user trusts ChartGen and the runtime environment.

Risk: Changing CHARTGEN_API_URL can route data to an untrusted or non-HTTPS endpoint.

Mitigation: Use the default ChartGen HTTPS endpoint or a trusted, reviewed endpoint only.

Risk: Returned artifacts may be saved from service-provided data or download URLs.

Mitigation: Prefer a fixed version that validates output filenames and download hosts, and review generated artifacts before sharing them.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/chartgen-ai/skills/chartai)
- [ChartGen API setup](https://chartgen.ai/chat)
- [ChartGen service](https://chartgen.ai)
- [Skill upgrade procedure](references/upgrade-skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON tool responses, image and PowerPoint file paths, edit URLs, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CHARTGEN_API_KEY and Node.js 14 or newer; supported upload formats are CSV, XLS, XLSX, and TSV.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
