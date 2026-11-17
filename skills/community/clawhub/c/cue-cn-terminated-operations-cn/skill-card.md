## Description:

将年报中终止经营与持有待售附注整理为带原文引句和锚点的登记表，并核对损益分项与现金流合计。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

面向阅读中国公司年报的分析人员，将终止经营及持有待售相关附注整理成可回查原文的七节 Markdown 登记稿，并检查损益分项和现金流合计。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment rates the skill suspicious and incomplete, citing behavior inconsistent with its stated financial-reporting purpose and concerns about external document handling.

Mitigation: Before providing documents or CUE_API_KEY, clarify what external services receive and how credentials are handled; avoid installation until those behaviors are understood.

## Reference(s):

- [ClawHub release](https://clawhub.ai/huhoo/skills/cue-cn-terminated-operations-cn)
- [Cue MCP catalog](https://cuecue.cn/api/mcp-catalog)
- [Cue Omni Reader](https://cuecue.cn/hub/omni-reader)
- [Cue API key information](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Markdown, Analysis]

**Output Format:** [Seven-section Markdown register with quoted source text, anchors, and source IDs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Missing items are identified explicitly; arithmetic checks cover profit components and cash flow totals; no investment recommendation.]

## Skill Version(s):

0.1.0 (source: artifact/SKILL.md frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
