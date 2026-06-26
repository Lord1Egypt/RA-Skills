## Description: <br>
Generate visual status cards for your OpenClaw agent as PNG, SVG, or JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LucaL6](https://clawhub.ai/user/LucaL6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to generate OpenClaw status snapshots for chat sharing, daily reports, scheduled updates, and programmatic metrics extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated status cards can expose operational metrics if shared in public channels. <br>
Mitigation: Preview snapshots before posting externally and prefer compact output for chat sharing. <br>
Risk: The skill depends on a separate Claw Insights service and may use bearer tokens or no-auth mode. <br>
Mitigation: Use the service only when trusted, keep bearer tokens private, and enable no-auth mode only on a trusted local machine. <br>
Risk: Detailed reports may include session activity, error counts, and gateway health information. <br>
Mitigation: Avoid posting full-detail reports in public channels or other broadly visible destinations. <br>


## Reference(s): <br>
- [Snapshot JSON Schema](references/json-schema.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/LucaL6/claw-insights-snapshot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides generation of PNG, SVG, or JSON snapshot files through the Claw Insights REST API or CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
