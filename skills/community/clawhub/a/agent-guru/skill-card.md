## Description:

Use when building, designing, or reviewing a multi-agent system for production: routing agents, orchestrating subagents, guarding tools with permissions, managing memory and context windows, adding observability and cost tracking, handling errors, or setting up session persistence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixuanjiang](https://clawhub.ai/user/weixuanjiang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, review, and harden production multi-agent systems, including routing, orchestration, tool safety, memory, observability, resilience, and persistence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples cover high-impact agent features and may be unsafe if copied verbatim into production.

Mitigation: Review examples before use and add workspace-bounded file writes, explicit user and tenant checks, dependency pinning, and cost and runtime limits.

Risk: Tool and permission patterns can affect external systems if defaults are too broad.

Mitigation: Use deny-overrides-allow permission precedence, human approval for irreversible actions, scoped tool access, and audit logging.

Risk: Memory and telemetry examples may expose sensitive data if deployed without controls.

Mitigation: Use opt-in memory loading, redaction, retention controls, encryption where appropriate, and secret-managed database credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixuanjiang/skills/agent-guru)
- [Router Layer](references/router-layer.md)
- [Orchestrator Layer](references/orchestrator-layer.md)
- [Tool + Safety Layer](references/tool-safety-layer.md)
- [Memory Layer](references/memory-layer.md)
- [Observability Layer](references/observability-layer.md)
- [Resilience Layer](references/resilience-layer.md)
- [Persistence Layer](references/persistence-layer.md)
- [Production Readiness Checklist](references/production-checklist.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with checklists, tables, and inline Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reference files are intended to be loaded on demand for the relevant production-agent layer.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
