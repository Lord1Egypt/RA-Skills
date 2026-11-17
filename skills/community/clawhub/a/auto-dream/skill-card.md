## Description:

Consolidate long-running agent memory with a 4-phase Orient -> Gather -> Merge -> Prune pass for stale, duplicated, contradictory, or oversized memory while preserving durable facts and avoiding secrets, customer data, or raw transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brasco05](https://clawhub.ai/user/brasco05)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users use this skill to consolidate persistent agent memory after long sessions, daily reflection, or handoff. It helps merge durable facts, remove stale or duplicate entries, resolve contradictions, and keep memory concise.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may modify or delete persistent agent memory without a clear confirmation or rollback step.

Mitigation: Run it manually, review proposed memory changes before applying them, and keep approval, logging, and restore mechanisms available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brasco05/skills/auto-dream)
- [Publisher profile](https://clawhub.ai/user/brasco05)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports merged facts, pruned entries, fixed contradictions, memory size change, and open questions.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
