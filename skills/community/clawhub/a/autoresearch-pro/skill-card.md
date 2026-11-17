## Description:

Improves existing skills, prompts, articles, plugins, and workflows through small reversible edits and same-task before-and-after comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other creators use this skill to improve an existing artifact through a bounded experiment, comparing actual outputs before retaining or reverting an edit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An edit could weaken existing behavior or introduce misleading guidance.

Mitigation: Preserve a recoverable baseline, review the proposed change, compare actual outputs on the same tasks, and revert inconclusive edits.

Risk: Optimization could extend beyond the authorized target or require external actions.

Mitigation: Keep edits within the authorized scope and seek explicit approval before paid evaluations, external writes, production access, or permission changes.

## Reference(s):

- [Autoresearch Pro on ClawHub](https://clawhub.ai/0xcjl/skills/autoresearch-pro)
- [Mutation strategies](references/mutation_strategies.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration]

**Output Format:** [Revised artifact in its original format, with a brief before-and-after comparison]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports observed results and unresolved limitations; marks unavailable runtime validation as unverified.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
