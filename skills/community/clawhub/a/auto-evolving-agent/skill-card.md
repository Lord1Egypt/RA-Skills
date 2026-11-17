## Description:

Self-evolving agent-development skill that uses a hybrid evolutionary strategy, combining Darwinian exploration and Lamarckian optimization to generate candidate improvements, score them, preserve successful patterns, and keep users in the approval loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuqingsonga](https://clawhub.ai/user/zhuqingsonga)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw developers use this skill to design and supervise agent self-improvement workflows, including proposal generation, multi-dimensional fitness scoring, gene-pool updates, and crystallizing repeated successes into reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose persistent changes to its own instructions, memory, workflows, SOUL.md, and installed capabilities.

Mitigation: Use it in proposal-only or tightly supervised mode, review exact diffs and module metadata, and approve only changes with clear scope and rollback paths.

Risk: Broad memory reuse and gene-pool updates can preserve low-quality, stale, or unintended patterns.

Mitigation: Require explicit user approval for memory admission, periodically prune stored patterns, and keep fitness criteria tied to observed task outcomes.

Risk: Automatic evolution can create supply-chain and file-scope risk if it installs or replaces capabilities without review.

Mitigation: Avoid enabling automatic evolution until file scope, rollback, memory hygiene, and supply-chain checks are enforced.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhuqingsonga/skills/auto-evolving-agent)
- [README](README.md)
- [Evolution History Template](references/evolution-history-template.md)
- [Fitness Scoring Template](references/fitness-scoring-template.md)
- [Gene Pool Template](references/gene-pool-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with structured proposals, scoring tables, checklists, and implementation snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Human approval is expected before persistent changes, especially changes to instructions, memory, workflows, SOUL.md, or installed capabilities.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
