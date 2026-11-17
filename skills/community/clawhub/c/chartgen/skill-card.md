## Description:

ChartGen helps agents create charts, dashboards, diagrams, reports, PPTs, and data analyses from text prompts and supported spreadsheet files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chartgen-ai](https://clawhub.ai/user/chartgen-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to send confirmed ChartGen requests for visualization, spreadsheet analysis, report generation, and PPT creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confirmed prompts and selected spreadsheet files are sent to ChartGen for processing.

Mitigation: Use the skill only where external ChartGen processing is acceptable, confirm user intent before submission, and avoid sensitive spreadsheets unless the user has approved that handling.

Risk: The security summary flags under-scoped network and data-handling behavior.

Mitigation: Review network and data flows before deployment, and prefer a version that validates API and download hosts.

Risk: A custom CHARTGEN_API_URL can route requests away from the default ChartGen service.

Mitigation: Leave CHARTGEN_API_URL unset or set it only to a trusted HTTPS ChartGen endpoint.

## Reference(s):

- [ChartGen Skill Repository](https://github.com/chartgen-ai/chartgen-skill)
- [ChartGen Chat and API Key Setup](https://chartgen.ai/chat)
- [ChartGen Service](https://chartgen.ai)
- [Skill Upgrade Procedure](references/upgrade-skill.md)
- [ClawHub Skill Page](https://clawhub.ai/chartgen-ai/skills/chartgen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON tool results that may reference generated image, PPT, or spreadsheet files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CHARTGEN_API_KEY and Node.js >= 14; outputs may include text replies, edit URLs, local artifact paths, preview images, and downloadable files.]

## Skill Version(s):

1.0.22 (source: server release metadata and tool version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
