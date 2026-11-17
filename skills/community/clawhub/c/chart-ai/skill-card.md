## Description:

Chart AI helps agents submit ChartGen requests to create visualizations, dashboards, diagrams, reports, PPTs, and data analyses from natural language or spreadsheet files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chartgen-ai](https://clawhub.ai/user/chartgen-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Chart AI to route charting, data analysis, and reporting requests to ChartGen after user confirmation, including Excel/CSV analyses and visual artifact generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected spreadsheet contents are sent to ChartGen for processing.

Mitigation: Install only when ChartGen is approved for the intended data, and avoid confidential, regulated, or secret data unless organizational approval exists.

Risk: The documented shell-style invocation can be unsafe for requests containing shell metacharacters.

Mitigation: Review generated commands before execution and prefer argument-safe invocation or hardened execution before handling untrusted inputs.

Risk: The tool can download generated PPT files from service-provided URLs.

Mitigation: Review downloaded artifacts before sharing or opening them in sensitive environments.

## Reference(s):

- [Chart AI ClawHub Listing](https://clawhub.ai/chartgen-ai/skills/chart-ai)
- [ChartGen Skill Homepage](https://github.com/chartgen-ai/chartgen-skill)
- [ChartGen API Key Setup](https://chartgen.ai/chat)
- [Skill Upgrade Procedure](references/upgrade-skill.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON tool results, plus local artifact file paths for generated charts or PPT files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CHARTGEN_API_KEY and Node.js >= 14; supports CSV, XLS, XLSX, and TSV uploads; polling may run up to about 25 minutes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
