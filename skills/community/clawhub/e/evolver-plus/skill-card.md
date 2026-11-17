## Description:

Agent self-evolution workflow that activates on repeated errors, capability gaps, inefficient processes, or explicit evolution requests, with L1-L4 safety gates, Gene records, backups, approvals, and restricted paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsangho](https://clawhub.ai/user/tsangho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to capture recurring failures or process gaps as proposed Gene changes, route them through safety-level review, and preserve backups and audit records before changes become persistent agent behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically alter persistent agent memory and skill documentation under broad self-modification triggers.

Mitigation: Require approval and an exact diff for every write to MEMORY.md, SKILL.md, GENES.md, PENDING.md, and rollback targets; keep use scoped to a dedicated workspace.

Risk: Untrusted task content could be converted into durable agent rules or skill changes.

Mitigation: Do not allow untrusted task content to become persistent rules automatically; review proposed Genes before accepting them.

## Reference(s):

- [Gene format reference](artifact/references/gene-format.md)
- [Safety levels reference](artifact/references/safety-levels.md)
- [ClawHub release page](https://clawhub.ai/tsangho/skills/evolver-plus)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with structured Gene records and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or write persistent files such as PENDING.md, GENES.md, audit logs, backups, MEMORY.md, SKILL.md, or approved rollback targets depending on safety level.]

## Skill Version(s):

1.0.2 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
