## Description:

Creates charts, dashboards, diagrams, slide decks, reports, and spreadsheet-based analyses through the ChartGen service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chartgen-ai](https://clawhub.ai/user/chartgen-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request ChartGen-generated visualizations, dashboards, reports, slide decks, and spreadsheet analyses from natural-language prompts and supported data files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, uploaded spreadsheet files, and API credentials can be sent to ChartGen.

Mitigation: Use the skill only with data approved for ChartGen processing, and avoid business-sensitive or regulated data unless that use has been reviewed.

Risk: The ChartGen API endpoint can be overridden with CHARTGEN_API_URL.

Mitigation: Leave CHARTGEN_API_URL unset unless it points to a trusted HTTPS ChartGen endpoint.

Risk: Server-provided artifacts can be downloaded and saved locally.

Mitigation: Review downloaded files before opening or sharing them, and treat generated artifacts as externally produced content.

Risk: Generated charts, reports, and analyses may be incomplete or misleading.

Mitigation: Validate important outputs against source data before using them for operational, financial, or customer-facing decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chartgen-ai/skills/chart-generator-pro)
- [ChartGen API key setup](https://chartgen.ai/chat)
- [ChartGen service](https://chartgen.ai)
- [Skill upgrade procedure](references/upgrade-skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, guidance]

**Output Format:** [Markdown or plain text with JSON tool responses and locally saved image, presentation, or spreadsheet artifacts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CHARTGEN_API_KEY and Node.js 14 or newer; generated artifacts may be saved to the local media or workspace directory.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
