## Description:

Guides the design and review of agent routing between local responses, cloud reasoning, tool proposals, and abstention while keeping authorization separate from model confidence and availability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vitorgabriel27](https://clawhub.ai/user/vitorgabriel27)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, assess, and document agent routing and authorization workflows, including constraint changes, tool safety gates, and evaluation criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Following instructional routing guidance alone does not enforce permissions on tool calls.

Mitigation: Implement authorization and effect controls in guarded tools, plugins, wrappers, or a policy service.

Risk: Untrusted content or stale authorization may lead to an unsafe tool proposal.

Mitigation: Treat retrieved content as data and check current authoritative permissions and policy immediately before any effectful action.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/vitorgabriel27/skills/constraint-aware-safe-routing)
- [Architecture and decision model](artifact/references/architecture.md)
- [Decision contract schema](artifact/references/decision-contract-v1.schema.json)
- [Evaluation protocol](artifact/references/evaluation.md)
- [OpenClaw integration guidance](artifact/references/openclaw-integration.md)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Shell commands]

**Output Format:** [Markdown guidance or a structured JSON routing decision]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decision fields follow a closed schema; optional audit-log validation commands.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
