## Description:

Patterns for adding safety, trust, and policy enforcement to AI agent systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boleyn](https://clawhub.ai/user/boleyn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design governance controls for AI agents that call external tools, operate in multi-agent systems, or handle sensitive workflows. It provides patterns for policy enforcement, intent classification, trust scoring, audit trails, and framework integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security-control examples may be materially unsafe or misleading if copied directly into production.

Mitigation: Review and adapt the examples before production use, treating them as conceptual patterns rather than production-ready controls.

Risk: The file path check, rate limiting, structured argument validation, and audit storage examples are called out by the security scan as insufficient for sensitive agents.

Mitigation: Use path-aware containment, request-scoped rate limits, recursive structured-argument validation, and non-overwriting or append-only audit storage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/boleyn/skills/agent-governance)
- [Agent-OS Governance Engine](https://github.com/imran-siddique/agent-os)
- [AgentMesh Integrations](https://github.com/imran-siddique/agentmesh-integrations)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration]

**Output Format:** [Markdown with inline Python, YAML, and checklist examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces governance patterns and example snippets rather than executable deployment artifacts.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
