## Description:

Analyzes Garmin Ultimate Frisbee activity, health, and recovery data to generate performance summaries, interactive HTML dashboards, and season or tournament comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evelyndevelops](https://clawhub.ai/user/evelyndevelops)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and users use this skill to analyze Garmin Connect data for Ultimate Frisbee performance, recovery, tournament fatigue, and training trends. It helps produce post-game reports, health summaries, and dashboard-generation commands from Garmin activity and wellness data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Garmin credentials and session tokens.

Mitigation: Use a virtual environment, avoid storing Garmin passwords in shell profiles or command-line history, and remove local session tokens when access should be revoked.

Risk: Generated dashboards and exported activity files can contain sensitive health and location data.

Mitigation: Store generated HTML, JSON, FIT, and GPX files privately, avoid sharing them publicly, and delete reports that are no longer needed.

Risk: Generated HTML dashboards may load chart assets from an external CDN.

Mitigation: Prefer offline or bundled chart assets, or verify script integrity before viewing private reports.

## Reference(s):

- [Garmin Connect API Reference](references/api.md)
- [Extended Capabilities](references/extended_capabilities.md)
- [Health Analysis Reference](references/health_analysis.md)
- [MCP Setup Guide](references/mcp_setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON summaries, and generated HTML dashboard files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local HTML, JSON, FIT, or GPX files containing sensitive health and location data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
