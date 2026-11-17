## Description:

Use this skill when the user wants to create visualizations, analyze spreadsheet or text data, or generate reports and presentations through ChartGen.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chartgen-ai](https://clawhub.ai/user/chartgen-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit confirmed ChartGen requests for charts, dashboards, diagrams, spreadsheet analysis, reports, and PPT generation. The skill returns Markdown analysis text plus locally saved visual or presentation artifacts when ChartGen completes the task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet uploads and analysis prompts may send sensitive user data to an external ChartGen service.

Mitigation: Review before installing, use only if the publisher and ChartGen are trusted, and avoid sensitive spreadsheets unless external processing is acceptable.

Risk: Configuring an unsafe API endpoint can expose API keys, uploaded files, or local network access.

Mitigation: Do not set CHARTGEN_API_URL except to a trusted HTTPS ChartGen endpoint; validate endpoint and artifact-download hosts before use.

Risk: Artifact downloads and polling can be affected by redirects, large responses, or long-running tasks.

Mitigation: Require HTTPS and enforce redirect, response size, and timeout limits around downloads and polling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chartgen-ai/skills/chartgen-ai)
- [Artifact-Declared Skill Homepage](https://github.com/chartgen-ai/chartgen-skill)
- [ChartGen](https://chartgen.ai)
- [ChartGen API Key Setup](https://chartgen.ai/chat)
- [Skill Upgrade Procedure](references/upgrade-skill.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown text with JSON tool responses and saved chart or presentation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CHARTGEN_API_KEY and Node.js >= 14; supports CSV, XLS, XLSX, and TSV inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata; tool helper version matches artifact)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
