## Description:

Design a multi-agent team that actually routes work. Pick roles by what they refuse, wire reporting lines, bound hand-offs, and place human gates, before writing any orchestration code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[delasy](https://clawhub.ai/user/delasy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design or diagnose multi-agent systems by defining bounded roles, reporting lines, hand-off limits, and human approval gates before orchestration code is written.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A generated org chart may be implemented with overly broad tool permissions, third-party write actions, pull request behavior, or durable memory outside the skill's control.

Mitigation: Review the actual runtime permissions, approval policies, pull request rules, and durable memory behavior before implementing the proposed design.

Risk: Poorly bounded multi-agent designs can create delegation loops, excessive fan-out, or shared-state conflicts.

Mitigation: Enforce tree-shaped reporting lines, local reachability, fan-out and depth caps, and single-writer access for shared mutable resources.

## Reference(s):

- [Role Archetypes](reference/role-archetypes.md)
- [Failure Modes](reference/failure-modes.md)
- [Aldena Org Chart](https://aldena.ai/features/org-chart)
- [Aldena Agents](https://aldena.ai/features/agents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown text spec with role entries, reporting edges, hand-off caps, and approval policies.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces planning guidance only; it does not execute commands, call tools, or modify runtime systems.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
