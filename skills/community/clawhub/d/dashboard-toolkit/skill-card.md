## Description:

A real-time SkillHub operations dashboard skill for monitoring sessions, costs, cron jobs, gateway health, logs, alerts, and deployment-related status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, and automation users use this skill to monitor SkillHub sessions, costs, scheduled tasks, gateway health, logs, and alerts. It can return dashboard status, cron scheduling details, alert events, metric snapshots, troubleshooting guidance, and configuration steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, write, and command execution authority for operational monitoring and management tasks.

Mitigation: Run it in a constrained environment and require explicit, auditable approval for command execution, file writes, cron changes, and deployment actions.

Risk: Operational outputs could lead to incorrect monitoring, alerting, scheduling, or deployment decisions if accepted without review.

Mitigation: Review proposed changes and status interpretations before applying them to production systems.

Risk: API keys or operational credentials may be needed for integrations.

Mitigation: Provide credentials through environment variables or an approved secret manager, avoid logging secret values, and rotate keys if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dashboard-toolkit)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [SkillHub skill homepage](https://skillhub.cn/skill/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured JSON-style responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include execution status, dashboard metadata, logs, cron details, alert events, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.7.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
