## Description:

Feishu-integrated wrapper for the capability-evolver that manages the evolution loop lifecycle, sends Feishu card reports, and provides dashboard visualization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linbo405](https://clawhub.ai/user/linbo405)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run a capability-evolver loop with Feishu reporting, monitor lifecycle status, generate evolution dashboards, and export history to Feishu Docs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep itself running through daemon or cron-style lifecycle behavior.

Mitigation: Require explicit approval for persistence, disable watchdog setup by default, and run it only in a controlled workspace.

Risk: The skill can mutate workspace memory and skill files, install sibling-skill packages, and push repository changes.

Mitigation: Constrain filesystem and git permissions, review diffs before publication, and gate package installation behind operator approval.

Risk: The skill can send logs, telemetry, dashboards, or raw history to Feishu.

Mitigation: Limit Feishu recipients and document tokens, redact sensitive logs before export, and verify configured targets before running.

Risk: Delegated-agent behavior may carry prompt-injection or unintended-task risk.

Mitigation: Review delegated prompts and require confirmation before spawning or forwarding agent work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linbo405/skills/feishu-evolver-dashboard)
- [Publisher profile](https://clawhub.ai/user/linbo405)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown dashboards, Feishu card reports, lifecycle command output, and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send reports or history to Feishu when the required Feishu environment variables and tokens are configured.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact package.json reports 1.7.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
