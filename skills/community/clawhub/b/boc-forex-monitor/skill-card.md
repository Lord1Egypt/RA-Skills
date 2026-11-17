## Description:

Configurable Bank of China forex monitor with per-currency thresholds, price columns, and optional OpenClaw notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiehuapeng](https://clawhub.ai/user/xiehuapeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to set up, configure, and troubleshoot a recurring Bank of China exchange-rate monitor with threshold alerts and optional OpenClaw notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring checks write exchange-rate monitoring configuration, alert data, and notification state under .openclaw-state.

Mitigation: Run the skill only in workspaces where recurring forex monitoring is intended and review .openclaw-state before sharing workspace contents.

Risk: Optional OpenClaw notifications can send alert details outside the local workspace.

Mitigation: Provide notification channels and targets only at runtime or through environment variables, keep recipient IDs private, and avoid routine success notifications unless explicitly desired.

## Reference(s):

- [BOC foreign exchange rates](https://www.boc.cn/sourcedb/whpj/)
- [Configuration](references/configuration.md)
- [ClawHub skill page](https://clawhub.ai/xiehuapeng/skills/boc-forex-monitor)
- [Publisher profile](https://clawhub.ai/user/xiehuapeng)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets; runner scripts produce text and JSON status output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local workspace state files and optional runtime notification parameters.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
