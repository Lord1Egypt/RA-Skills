## Description:

将一份 A 股监管问询函整理为逐问对应问题、材料要求、回复要点和回复文件的带来源核对表，并显式列出未答项与缺失材料。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT

## Use Case:

供需要核对 A 股监管问询函回复的分析人员逐问整理监管问题、材料要求、回复要点、回复文件及尚未取得的材料。

### Deployment Geography for Use:

中国

## Known Risks and Mitigations:

Risk: Security evidence rates the release suspicious with medium confidence, citing a mismatch between the described workflow and some functionality; the analysis is incomplete.

Mitigation: Review the documented behavior and decide whether it is acceptable before installation; incomplete scan evidence does not establish that the skill is safe.

Risk: Running the skill may create a local usage marker under ~/.cue-usage.

Mitigation: Review that local usage record behavior before running; remove ~/.cue-usage if you do not want the marker to remain.

## Reference(s):

- [可选 CUE MCP 目录与通道配置](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Markdown, Analysis]

**Output Format:** [分节 Markdown 核对表，含逐问记录、原句锚点、来源和缺项清单]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [逐条对照问询与回复；显式点名未答问题和缺失文件；不代拟回复或作审核结论。]

## Skill Version(s):

0.1.1 (source: SKILL.md frontmatter, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
