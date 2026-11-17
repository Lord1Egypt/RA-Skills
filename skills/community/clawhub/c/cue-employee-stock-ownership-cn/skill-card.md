## Description:

把一份 A 股员工持股计划草案或公告整理为八项带原文引句和来源锚点的条款卡，并标出未检索到的内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

面向阅读 A 股员工持股计划草案或公告的员工与分析人员，逐项提取八类条款原文与定位，并标出缺失信息；参与价值、价格公允性、解锁和税务问题留待人工判断。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: ClawScan flags an unpinned installation source and behavior that may not match the stated purpose.

Mitigation: Review the skill contents and verify or pin the source version before installing.

Risk: The handling of attachments sent to an external parser is not clearly disclosed.

Mitigation: Check where documents go and how they are handled before submitting confidential or unpublished material.

Risk: The security analysis is incomplete because one referenced path could not be resolved.

Mitigation: Review the unresolved path and rerun the security analysis before deployment.

## Reference(s):

- [员工持股条款速查](references/esop-terms.md)
- [ClawHub skill page](https://clawhub.ai/huhoo/skills/cue-employee-stock-ownership-cn)
- [Cue MCP documentation](https://cuecue.cn/hub/mcp)
- [Cue Omni Reader documentation](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown clause card with verbatim quotations and source anchors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Eight clause items; missing information is identified, and investment or tax judgments are reserved for human review.]

## Skill Version(s):

0.1.1 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
