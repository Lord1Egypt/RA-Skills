## Description:

帮助代理从财报或公告中整理外币折算披露，逐条记录货币性项目、折算汇率、汇兑损益去向、境外经营折算与记账本位币变更，并为每项附原文锚点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要梳理财报或公告中外币折算披露的分析人员，用于生成带原句、来源定位和缺项清单的登记稿。它不提供汇率预测或投资建议，也不替用户作会计判断。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags undeclared external service use and persistent local usage tracking; its analysis is partial.

Mitigation: Before installing, review the external-service flow and local marker behavior, and only provide documents appropriate for the service's data handling.

## Reference(s):

- [Cue data access setup](https://cuecue.cn/hub/mcp)
- [Cue Omni Reader setup](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Seven-section Markdown disclosure register with quoted source passages, location anchors, source IDs, and explicit missing-field entries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records disclosed wording and sources; does not fill missing exchange rates or infer accounting treatment.]

## Skill Version(s):

0.1.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
