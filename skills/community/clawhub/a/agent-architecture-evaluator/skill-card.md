## Description:

Use when evaluating, testing, and optimizing an agent architecture or multi-agent system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ada01325150-alt](https://clawhub.ai/user/ada01325150-alt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review agent or multi-agent system architecture, map system-level failure modes, define architecture tests, and prioritize reliability, cost, latency, observability, and coordination improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional formatter script reads a JSON file and can write Markdown to a caller-selected path.

Mitigation: Run it only on intended input files and choose output paths deliberately.

Risk: Architecture recommendations can affect reliability, cost, latency, and approval placement in agent systems.

Mitigation: Review recommendations with system owners and validate proposed changes with architecture-level tests before deployment.

## Reference(s):

- [Architecture Review Framework v1.0.0](references/architecture-review-framework-v1.0.0.md)
- [Optimization Patterns v1.0.0](references/optimization-patterns-v1.0.0.md)
- [Architecture Review Template](assets/architecture-review-template.md)
- [Example Architecture Review](assets/example-architecture-review.md)
- [Structured Input Example](assets/architecture-input-example.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, code, shell commands]

**Output Format:** [Markdown guidance with named review sections and optional JSON-to-Markdown formatting script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces architecture inventory, failure mode map, architecture test plan, optimization roadmap, measurement plan, and architecture recommendation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
