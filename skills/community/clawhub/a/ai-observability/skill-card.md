## Description:

A Chinese-first AI observability playbook and local toolkit for designing runtime monitoring across logs, metrics, traces, AI quality, cost, guardrails, alerting, and rollout practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

AI platform, SRE, operations, and quality teams use this skill to plan production observability for AI applications, including monitoring scope, metric selection, alert design, tracing standards, and rollout roadmaps. Agents can also use the bundled local toolkit to produce structured checklists and guidance for these monitoring tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package mixes MIT licensing with restrictive knowledge-use language in the publisher materials.

Mitigation: Review the license and copyright terms before redistribution, model-training use, or commercial reuse of the knowledge content.

Risk: The observability thresholds and monitoring recommendations are guidance rather than a deployed monitoring system.

Mitigation: Calibrate metrics, alert thresholds, and data-retention practices against the production application's risk level, traffic, and compliance requirements.

Risk: The bundled security audit is publisher-provided context, while server evidence reports a clean scan.

Mitigation: Use the server security summary as the authoritative release signal and re-scan or review locally before deployment in controlled environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoxinghua09-cell/skills/ai-observability)
- [01 可观测性全景](references/01-可观测性全景.md)
- [02 调用追踪与日志](references/02-调用追踪与日志.md)
- [03 质量监控指标](references/03-质量监控指标.md)
- [04 性能与成本监控](references/04-性能与成本监控.md)
- [05 护栏与安全监控](references/05-护栏与安全监控.md)
- [06 告警体系](references/06-告警体系.md)
- [07 平台与落地](references/07-平台与落地.md)
- [08 常见问题 FAQ](references/08-FAQ.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with optional local shell commands and plain-text toolkit output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled Python toolkit is zero-dependency and prints local observability checklists, metric tables, alert designs, tracing standards, and rollout plans.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
