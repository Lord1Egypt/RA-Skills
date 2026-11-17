## Description:

Lightweight command monitoring tool that periodically executes local commands/scripts in batches, detects output changes, and triggers alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengyun8](https://clawhub.ai/user/mengyun8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Cmdnotify to configure periodic local command checks, detect command output or exit-code changes, and route alerts through stderr or a configured notification command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured monitoring commands may capture sensitive local command output.

Mitigation: Review each monitored command before use and avoid collecting secrets or unnecessarily broad command output.

Risk: Custom notification commands can send monitored output to external services or persistent logs.

Mitigation: Review every notify_cmd, limit alert payload content, and avoid webhooks or logs that retain sensitive data.

Risk: The skill repeatedly runs local commands at configured intervals.

Mitigation: Install and use it only when recurring local command execution is intended, and set conservative intervals and timeouts.

## Reference(s):

- [Cmdnotify ClawHub skill page](https://clawhub.ai/mengyun8/skills/cmdnotify)
- [Publisher profile](https://clawhub.ai/user/mengyun8)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with JSON configuration examples and bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
