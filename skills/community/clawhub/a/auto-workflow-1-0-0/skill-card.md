## Description:

Builds automation workflows from repetitive tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangyingzhuangk](https://clawhub.ai/user/zhangyingzhuangk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to identify repetitive manual tasks and turn them into automation workflows, scripts, and configurations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may push an agent to write scripts, configurations, scheduled jobs, or outbound workflows without explicit user approval.

Mitigation: Require the agent to present a plan listing files, commands, schedules, data sources, and destinations, then wait for explicit approval before making changes or sending anything.

Risk: Automation proposals may introduce incorrect or misleading workflow logic.

Mitigation: Review proposed workflows and test them on a small scope before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with workflow steps, script examples, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose scripts, scheduled jobs, data sources, destinations, and outbound workflow actions that require user review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
