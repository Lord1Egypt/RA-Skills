## Description:

PKM（个人知识管理）三分支记忆系统。使用时机：(1) 接收记忆，(2) 检索上下文，(3) 搜索记忆，(4) 添加事实，(5) 检查 Qdrant。三分支：L1 复位（索引）、L2 索引、L3 日志、L4 Qdrant、L5 Obsidian、L6 Nebula、L7 情景记忆。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kofna3369](https://clawhub.ai/user/kofna3369)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through a Chinese personal knowledge management memory workflow, including adding memories, retrieving context, searching memory, adding facts, and checking local Qdrant state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted content can be persisted in local memory and vector stores.

Mitigation: Avoid storing secrets or sensitive personal data unless the local PKM and Qdrant services are trusted.

Risk: The skill includes commands that add or query persistent memories through local services.

Mitigation: Prefer explicit confirmation before adding new memories and review target endpoints before running commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kofna3369/skills/chinese-pkm-memory)
- [Publisher profile](https://clawhub.ai/user/kofna3369)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target local PKM API and Qdrant services.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
