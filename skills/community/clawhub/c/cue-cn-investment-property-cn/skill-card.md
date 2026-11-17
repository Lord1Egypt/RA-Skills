## Description:

将投资性房地产披露整理为逐条附有原句、文档锚点和来源编号的登记表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

财务分析人员可用它将年报、半年报、公告或已解析的披露材料整理为投资性房地产逐项登记表，保留原文、文档锚点与来源编号，并标明未取到的信息。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the release suspicious: report attachments may be sent to an external parsing service, with recipient and consent requirements unclear.

Mitigation: Before sending attachments for parsing, confirm the recipient and data handling, and obtain authorization to share the material.

Risk: ClawScan reports undeclared remote tool discovery and an absent declared tool scope; scan coverage is partial.

Mitigation: Review the requested tools and network destinations before enabling the skill, and allow only expected access.

Risk: A local usage marker may be created, and the checker may fail to catch an incorrect transfer amount.

Mitigation: Review local file changes and verify transfer amounts against the cited disclosure text.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-investment-property-cn)
- [Cue data MCP directory](https://cuecue.cn/hub/mcp)
- [Cue Omni Reader](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Text]

**Output Format:** [中文 Markdown 登记表，含原句、文档锚点和来源编号]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [按七个有序章节组织；未取到的信息明确标出，数字保留披露原文。]

## Skill Version(s):

0.1.1 (source: SKILL.md frontmatter; server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
