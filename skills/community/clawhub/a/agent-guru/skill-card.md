## Description: <br>
Use when building, designing, or reviewing a multi-agent system for production: routing agents, orchestrating subagents, guarding tools with permissions, managing memory and context windows, adding observability and cost tracking, handling errors, or setting up session persistence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weixuanjiang](https://clawhub.ai/user/weixuanjiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, build, or review production multi-agent systems with routing, orchestration, tool safety, memory, observability, resilience, and persistence practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example snippets may be copied into production without sufficient hardening. <br>
Mitigation: Review and adapt snippets before deployment, including log redaction, explicit memory trust boundaries, secret-safe database configuration, session-resume access checks, and retention/deletion controls for persisted memory. <br>
Risk: The skill is documentation-only and does not itself enforce runtime safety controls. <br>
Mitigation: Treat the guidance as design input and enforce safety, permissions, observability, and persistence controls in application code. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/weixuanjiang/agent-guru) <br>
- [Memory Layer](references/memory-layer.md) <br>
- [Observability Layer](references/observability-layer.md) <br>
- [Orchestrator Layer](references/orchestrator-layer.md) <br>
- [Persistence Layer](references/persistence-layer.md) <br>
- [Production Readiness Checklist](references/production-checklist.md) <br>
- [Resilience Layer](references/resilience-layer.md) <br>
- [Router Layer](references/router-layer.md) <br>
- [Tool and Safety Layer](references/tool-safety-layer.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline code blocks, command examples, checklists, and implementation patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only reference material; example snippets require review and hardening before production reuse.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
