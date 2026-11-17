## Description:

Proactive cron job health monitoring, failure detection, and auto-repair delegation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ygq19901001](https://clawhub.ai/user/ygq19901001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to inspect cron job health, identify common failure patterns, and prepare repair actions for failed or silently unhealthy scheduled jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic cron repair can change scheduled job behavior, output paths, alert routing, or model/provider settings.

Mitigation: Confirm the cron jobs, output paths, alert channels, and update permissions the agent may use before enabling automatic repair.

Risk: Cron health findings may lead to incorrect or incomplete repair actions if applied without checking the affected job state.

Mitigation: Review proposed changes, run the repaired cron job once, and verify lastRunStatus and output content before relying on the fix.

## Reference(s):

- [Source repository](https://github.com/Ygq19901001/biobrain-cron-health-monitor)
- [ClawHub skill page](https://clawhub.ai/ygq19901001/skills/biobrain-cron-health-monitor)
- [Common Cron Error Catalog](references/common-errors.md)
- [Cron Repair Playbook](references/repair-playbook.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with cron command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose cron updates, alert settings, fallback model configuration, and repair verification steps.]

## Skill Version(s):

0.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
