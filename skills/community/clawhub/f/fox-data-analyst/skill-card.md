## Description:

Data visualization, report generation, SQL queries, and spreadsheet automation for agents that turn raw data into actionable insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tihuaqin-commits](https://clawhub.ai/user/tihuaqin-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations teams use this skill to guide database querying, spreadsheet analysis, data cleaning, visualization, and report generation from configured data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute arbitrary SQL against configured databases, including statements that may alter data.

Mitigation: Use read-only database credentials whenever possible and review SQL statements before execution.

Risk: Configured data sources may expose production, regulated, or otherwise sensitive data to the agent.

Mitigation: Connect only data sources that are appropriate for the intended use case and avoid production or regulated data unless explicitly approved.

Risk: Rerunning the workspace initializer can overwrite its generated template files.

Mitigation: Review the target data-analysis workspace before rerunning initialization and preserve any customized templates first.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tihuaqin-commits/skills/fox-data-analyst)
- [Publisher Profile](https://clawhub.ai/user/tihuaqin-commits)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with SQL, Python, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local workspace templates under the configured data-analysis directory when the initializer script is run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
