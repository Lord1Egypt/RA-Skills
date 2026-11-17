## Description:

个人服务器监控工具，支持CPU/内存/磁盘基础指标与简单告警通知。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and automation agents use this skill to inspect local server CPU, memory, disk, network, process, and basic service status, then configure simple threshold alerts for a single machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may execute local system commands while collecting monitoring data.

Mitigation: Use it only for explicit monitoring requests and inspect or define exact commands before execution.

Risk: Broad or inconsistent instructions could move execution outside a clear monitoring-only scope.

Mitigation: Keep use limited to CPU, memory, disk, network, process, service status, and alert configuration tasks.

Risk: SMTP alerting can send alert metadata through a mail provider.

Mitigation: Enable SMTP only after reviewing the destination, provider, and environment-based credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/auto-monitor-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return monitoring summaries, alert setup guidance, command output, and error-handling steps.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
