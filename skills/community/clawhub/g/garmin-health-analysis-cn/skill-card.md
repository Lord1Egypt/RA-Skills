## Description:

Connects to Garmin Connect to answer natural-language questions about running, activities, and more than 20 health metrics, and can create interactive dashboards and analyze FIT or GPX activity files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earthaveeman](https://clawhub.ai/user/earthaveeman)

### License/Terms of Use:

MIT-0

## Use Case:

Runners and Garmin Connect users can query sleep, recovery, heart rate, training, and activity data, review trends, and generate interactive charts for personal monitoring and training analysis.

### Deployment Geography for Use:

Global; supports Garmin Connect accounts in China and internationally.

## Known Risks and Mitigations:

Risk: The skill can expose Garmin account identity details and personal health and activity data.

Mitigation: Provide credentials through a trusted local environment or configuration, keep credential and token files private, and review results before sharing them.

Risk: The scanner reports unclear activation and tool scope, and the guidance may apply to broad questions.

Mitigation: Limit use to explicit Garmin health or activity requests and review commands and results when the active tool permissions are unclear.

## Reference(s):

- [Health Analysis Guide](artifact/references/health_analysis.md)
- [Garmin Connect API Notes](artifact/references/api.md)
- [Extended Capabilities](artifact/references/extended_capabilities.md)
- [Garmin Connect China](https://connect.garmin.cn)
- [Garmin Connect International](https://connect.garmin.com)
- [ClawHub Skill Release](https://clawhub.ai/earthaveeman/skills/garmin-health-analysis-cn)

## Skill Output:

**Output Type(s):** [Analysis, JSON, HTML dashboards, FIT/GPX files, Guidance]

**Output Format:** [Natural-language summaries and analysis, JSON data, interactive HTML charts, and downloaded or parsed FIT/GPX activity files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Health and activity analysis is based on available Garmin account data and device-supported metrics.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
