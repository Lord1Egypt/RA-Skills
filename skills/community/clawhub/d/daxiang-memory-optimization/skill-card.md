## Description:

Optimizes memory management by scoring, pruning low-value entries, controlling memory size, and retrieving top relevant memories for efficient agent access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep agent memory useful and bounded by scoring memories, retrieving the most relevant items, and pruning or archiving low-value entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic pruning can remove or overwrite useful agent memory.

Mitigation: Review defaults before use, disable auto-prune or require dry-run confirmation, and keep backups or rollback before saving pruned memory.

Risk: Archived memory can expose retained context if stored in plaintext or an unsafe path.

Mitigation: Use workspace-relative archive locations, protect or encrypt archived memory, and apply retention controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daxiangnaoyang/skills/daxiang-memory-optimization)
- [Artifact skill documentation](artifact/SKILL.md)
- [Artifact configuration](artifact/config.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python, PowerShell, JSON, and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes configurable memory window, pruning threshold, retrieval limit, scoring weights, cache settings, and archive behavior.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
