## Description:

Big Memory helps OpenClaw agents capture structured task snapshots before context compaction and recover exact working state afterward.

This skill is ready for commercial/non-commercial use.

## Publisher:

[obekt](https://clawhub.ai/user/obekt)

### License/Terms of Use:


## Use Case:

Developers and agent users use Big Memory to preserve task state across context compaction during long, multi-step coding or project sessions and to restore the latest saved snapshot when context is lost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist detailed project context, including file paths, decisions, code snippets, and task state.

Mitigation: Review the skill before installation when working with secrets, private customer data, proprietary code, or regulated information.

Risk: Automatic compaction capture may save sensitive or untrusted content before redaction rules are in place.

Mitigation: Prefer explicit save and recall commands, and avoid automatic compaction capture until appropriate redaction rules are added.

Risk: Optional session transcript indexing or cloud embeddings can make conversation content searchable or provider-processed.

Mitigation: Do not enable session transcript indexing or cloud embeddings unless that processing is acceptable for the workspace.

## Reference(s):

- [Big Memory Homepage](https://github.com/obekt/big-memory)
- [Task Snapshot Template](references/TASK-SNAPSHOT.md)
- [Recommended OpenClaw Configuration](references/openclaw-config.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown task snapshots with optional JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes append-only task snapshots to memory/YYYY-MM-DD.md when capture is triggered.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
