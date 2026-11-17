## Description:

AgentOps is an OpenClaw operations toolkit for health checks, log analysis, performance monitoring, configuration optimization, alerting, multi-agent coordination, diagnostics, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keybryant](https://clawhub.ai/user/keybryant)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect and manage OpenClaw agents through local health checks, log analysis, performance monitoring, configuration review, alert rules, coordination checks, diagnostics, and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw logs, configuration, workspace metadata, process lists, and system metrics.

Mitigation: Run it only in environments where local operational inspection is intended, and review generated reports before sharing them.

Risk: Troubleshooting and configuration guidance can include restart, cleanup, or configuration-change recommendations.

Mitigation: Review recommendations against the target environment before applying operational changes.

Risk: Alert rules and performance reports are written locally when the related commands are invoked.

Mitigation: Choose output paths deliberately and review alert thresholds before enabling automated checks.

## Reference(s):

- [OpenClaw 配置参考](references/openclaw_config_reference.md)
- [性能指标说明](references/metrics_reference.md)
- [常见问题排查](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, and terminal text with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated local report files or alert rule files when those actions are invoked.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
