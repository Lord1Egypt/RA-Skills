## Description:

Three-layer storage plus four mechanisms and a P0-P3 truth hierarchy for long-term agent memory using MEMORY.md, structured memory/core facts, local vector search, Engramory curation, WAL protocol, and context management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chen6896qqwee](https://clawhub.ai/user/chen6896qqwee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to structure durable local memory for an agent, including a central index, structured fact files, semantic search, write-ahead logging, context summaries, and memory promotion rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can capture personal, financial, account, or trading data beyond the current session.

Mitigation: Require explicit approval before writing sensitive data, define the allowed memory scope, and keep an auditable delete or rollback process.

Risk: Startup memory and boot behavior changes can make future agent sessions rely on promoted information without enough review.

Mitigation: Require review before changing boot or soul files and before promoting any item into startup memory.

Risk: Memory used around real-time or trading decisions can become stale or conflict with authoritative account data.

Mitigation: Use live APIs or other authoritative systems for current positions and account state, and keep historical memory for context or post-mortem use only.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chen6896qqwee/skills/dawn-memory-arch)
- [ClawHub publisher profile](https://clawhub.ai/user/chen6896qqwee)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown guidance with file-layout examples, configuration steps, and operational rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed for local filesystem, SQLite, and LanceDB-based memory workflows; no external API dependency is described.]

## Skill Version(s):

9.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
