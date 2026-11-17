## Description:

Find and reclaim what an agent accumulates on disk: oversized sessions, duplicated transcripts, stale embedding caches, abandoned trees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[posthuman](https://clawhub.ai/user/posthuman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent maintainers use this skill to audit local agent storage growth, identify duplicated transcripts, stale caches, and abandoned workspace trees, and prepare cautious cleanup reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup guidance can involve deletion, truncation, rebuild, or abandoned-tree removal actions that may remove live data if applied to the wrong target.

Mitigation: Work from a backup or copy, confirm exact targets, prefer the owning application's supported maintenance commands, and verify counts and integrity afterward.

Risk: Database clients without required extensions may be unable to see virtual tables or vector indexes, which can leave derived indexes inconsistent after direct deletes.

Mitigation: Confirm the client can open every schema object, restrict direct deletes to plain tables with no triggers, and test full rebuilds on a copy before running them for real.

Risk: A single rebuild after transcript compaction may appear incomplete because derived indexes can prune later and create a fresh free list.

Mitigation: Plan a second pass and report free-list behavior, bytes returned, and index counts before and after maintenance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/posthuman/skills/agent-storage-maintenance)
- [Publisher profile](https://clawhub.ai/user/posthuman)
- [Classifying what accumulates](artifact/references/classification.md)
- [Worked audit](artifact/examples/audit-session.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with audit findings, classifications, cleanup recommendations, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include counts, byte totals, before-and-after comparisons, and verification steps for storage maintenance.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
