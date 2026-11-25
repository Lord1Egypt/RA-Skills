## Description:

将年报附注中的股份支付信息整理为逐项可追溯的登记稿，并核对权益结算与现金结算费用合计及可行权数量变动。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

财务报告分析人员可用此技能把年报附注中的股份支付项目整理成有原句和定位锚点的登记稿，并检查两类费用合计和可行权数量变动。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unexplained network integration and external document processing, creating uncertainty about how disclosure documents are handled.

Mitigation: Clarify the network and document-processing behavior before installation; provide only the disclosure material needed for the task until handling is understood.

Risk: The security review says the checker may not distinguish incomplete checks from successful ones, and the scan was partial.

Mitigation: Review the checker's result and its completeness for each draft, and have a person verify reconciliations before relying on them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-share-based-payment-cn)
- [MCP service catalog](https://cuecue.cn/api/mcp-catalog)
- [MCP setup](https://cuecue.cn/hub/mcp)
- [Omni Reader setup](https://cuecue.cn/hub/omni-reader)
- [API key setup](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown structured-note with source quotations and anchors; text findings from the reconciliation checker]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records disclosed values and missing items; does not assess incentive-plan merits or provide investment recommendations.]

## Skill Version(s):

0.1.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
