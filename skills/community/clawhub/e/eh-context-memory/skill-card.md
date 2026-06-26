## Description: <br>
Context Memory helps agents manage context windows and preserve knowledge across session handoffs and compaction events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve decisions, rejected options, risks, and remaining work across long-running coding sessions. It provides handoff patterns, periodic compaction snapshots, and token-usage checks so an agent can recover important context after compaction or a session boundary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local handoff and snapshot files may contain sensitive conversation details, decisions, or personal data. <br>
Mitigation: Keep secrets and personal data out of conversations that may be snapshotted, and review or delete saved handoffs periodically. <br>
Risk: Generated memory files may be committed or retained longer than intended. <br>
Mitigation: Add git-ignore or cleanup rules for .working-state and session-memory paths before using the skill in shared repositories. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lanyasheng/eh-context-memory) <br>
- [Handoff Documents](references/handoff-documents.md) <br>
- [Compaction Extract](references/compaction-extract.md) <br>
- [Memory Consolidation](references/memory-consolidation.md) <br>
- [Token Budget](references/token-budget.md) <br>
- [Context Usage](references/context-usage.md) <br>
- [Filesystem Working Memory](references/filesystem-working-memory.md) <br>
- [Compaction Quality Audit](references/compaction-quality-audit.md) <br>
- [Auto-Compact Circuit Breaker](references/auto-compact-circuit-breaker.md) <br>
- [Extended Patterns](references/extended-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with shell commands, JSON hook output, and local handoff files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local session handoff and compaction snapshot files when configured.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release metadata; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
