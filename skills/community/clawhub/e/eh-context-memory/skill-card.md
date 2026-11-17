## Description:

Context Memory helps agents preserve and reuse task context through handoff documents, periodic compaction snapshots, token-budget checks, and filesystem working memory patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage long-running coding sessions where decisions, rejected options, and current plans need to survive compaction, crashes, or handoffs across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist conversation-derived context as local plaintext handoff and memory files.

Mitigation: Avoid sensitive conversations unless local plaintext retention is acceptable, store snapshots in private per-project directories, and apply redaction and retention rules.

Risk: Saved memory may be reinjected into later sessions without enough review.

Mitigation: Require confirmation before reinjecting saved memory and review handoff content for relevance and sensitivity.

Risk: The security summary reports an unsafe session-path write pattern.

Mitigation: Restrict session IDs to safe characters before installing or running the hook scripts.

## Reference(s):

- [Handoff Documents](references/handoff-documents.md)
- [Compaction Extract](references/compaction-extract.md)
- [Compaction Quality Audit](references/compaction-quality-audit.md)
- [Context Usage](references/context-usage.md)
- [Filesystem Working Memory](references/filesystem-working-memory.md)
- [Memory Consolidation](references/memory-consolidation.md)
- [Token Budget](references/token-budget.md)
- [Auto-Compact Circuit Breaker](references/auto-compact-circuit-breaker.md)
- [Extended Patterns](references/extended-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON hook outputs, and file path conventions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local handoff and compaction snapshot files when configured as hooks.]

## Skill Version(s):

2.4.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
