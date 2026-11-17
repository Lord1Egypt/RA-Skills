## Description:

将年报和半年报中的主要会计数据、财务指标、非经常性损益及分季度数据整理为逐项引用原文的登记稿，并提供结构与数字核对。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

面向整理上市公司年报或半年报的分析人员，把主要会计数据、财务指标、非经常性损益和分季度数据逐项登记，并为数值附上原文、定位锚点和来源编号。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marks the skill suspicious because it reports credentialed requests to a configurable remote service and external processing of report attachments; the scan was partial.

Mitigation: Review the destination and data flow before enabling remote retrieval, provide CUE_API_KEY only when needed, and send report attachments for external processing only when that is acceptable.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-key-financial-data-cn)
- [CUE MCP setup](https://cuecue.cn/hub/mcp)
- [CUE Omni Reader setup](https://cuecue.cn/hub/omni-reader)
- [CUE API key](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Chinese Markdown report draft with per-value quotations, source anchors, and source IDs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Values are transcribed from source documents, missing items are identified, and the included checker validates structure and selected numeric relationships. It does not assess performance or provide investment recommendations.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
