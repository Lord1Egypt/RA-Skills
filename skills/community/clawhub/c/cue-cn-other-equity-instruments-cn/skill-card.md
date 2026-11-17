## Description:

从财报或公告中登记其他权益工具（永续债与优先股）的披露，为条款和会计分类依据保留原文、定位锚点与来源编号，并标记缺失信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

面向整理中国企业财报与公告的分析人员，用于逐项登记永续债和优先股条款、利息股利处理及发行方披露的分类依据，并回查原文；分类判断、每股收益测算和投资评价由人工处理。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan 将该技能评为可疑：扫描报告指出网络活动与披露整理用途存在不匹配，并涉及凭据和文档上传风险；扫描覆盖不完整。

Mitigation: 在使用前澄清 MCP 活动与任务的关系，核实携带凭据的请求目标，并明确披露和授权外部文档上传；完成澄清前避免安装。

## Reference(s):

- [数据通道配置](https://cuecue.cn/hub/mcp)
- [长附件与 PDF 解析](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [中文 Markdown 登记稿，逐项附原文引句、定位锚点和 [S#] 来源编号。]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [缺失信息明确标记；不作独立会计分类判断、每股收益测算、估值或评级。]

## Skill Version(s):

0.1.0 (source: release evidence, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
