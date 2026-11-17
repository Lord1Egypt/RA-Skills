## Description:

Stop agents from "forgetting, mixing projects, and rotting over time" by giving them a practical memory operating system: global memory, project memory, promotion rules, validation cases, and a maintenance loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aslan-ai-labs](https://clawhub.ai/user/aslan-ai-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to design structured long-term and project-specific memory for AI agents, including routing, promotion, validation, and maintenance practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Memory files can contain private names, paths, IDs, document URLs, or raw conversation details if users publish them without abstraction.

Mitigation: Keep private data out of public or shareable outputs and replace personal or project-specific details with neutral placeholders.

Risk: Unvalidated project lessons can become misleading global rules if promoted too early.

Mitigation: Require evidence, validation history, and clear scope boundaries before promoting lessons into reusable or canonical memory.

Risk: A memory system can decay when status, asset indexes, lessons, or global rules are not reviewed.

Mitigation: Use the maintenance loop to update project state, review candidates, promote proven lessons, and deprecate stale rules on a regular cadence.

## Reference(s):

- [Architecture Decision Guide](references/architecture-decision-guide.md)
- [Architecture](references/architecture.md)
- [Failure Modes](references/failure-modes.md)
- [Routing](references/routing.md)
- [Promotion](references/promotion.md)
- [Validation](references/validation.md)
- [Maintenance](references/maintenance.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with reusable file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce project memory structures, routing rules, promotion rules, validation cases, and maintenance runbooks.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
