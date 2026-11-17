## Description:

记忆整理技能 — 审查结构化记忆，提取洞察，更新 MEMORY.md，清理过期条目。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jobzhao15](https://clawhub.ai/user/jobzhao15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to review persistent memory entries, remove stale or duplicate records, and summarize high-value memories into MEMORY.md.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete persistent memory entries.

Mitigation: Ask the agent to show the memory IDs it plans to delete and the reason for each deletion before applying changes.

Risk: The skill can update MEMORY.md with summaries that may be incomplete or too broad.

Mitigation: Review the MEMORY.md diff before applying changes and keep only long-lived, high-importance information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jobzhao15/skills/enhance-memory-curator)
- [Publisher profile](https://clawhub.ai/user/jobzhao15)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown report with memory review statistics, proposed memory actions, and MEMORY.md update notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May identify memory IDs for deletion or merging and summarize proposed MEMORY.md changes for review.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
