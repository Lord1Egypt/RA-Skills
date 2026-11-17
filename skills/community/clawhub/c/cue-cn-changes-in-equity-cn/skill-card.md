## Description:

将合并所有者权益变动表整理为逐项附原文与定位锚点的 Markdown 登记稿，并核对行列算术及三项勾稽。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

财务分析人员、审阅者及需要复核中国企业年报的使用者，可用它把合并所有者权益变动表整理为逐项可追溯的登记稿，并核验已取得数据的勾稽关系。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marks the release suspicious because it reports external service access and credential use that do not clearly fit the financial-document task; scan coverage is incomplete.

Mitigation: Before using private financial documents or credentials, confirm and trust the external services and how routing destinations are checked.

Risk: Wide or cross-page statement tables and screenshots may leave figures unavailable, so some arithmetic checks may not run.

Mitigation: Record missing items explicitly, review the original report, and treat only checks reported as performed as verified.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huhoo/skills/cue-cn-changes-in-equity-cn)
- [CUE MCP service](https://cuecue.cn/hub/mcp)
- [CUE Omni Reader](https://cuecue.cn/hub/omni-reader)
- [CUE API key information](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Markdown, Analysis]

**Output Format:** [Chinese Markdown registration draft with source quotations, location anchors, and arithmetic check results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports unavailable source items explicitly; checks only figures present in the source and does not infer missing values.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
