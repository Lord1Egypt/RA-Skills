## Description:

将年报或半年报附注中所有权或使用权受到限制的资产逐项整理为带原文引用与定位锚点的登记表，并检查合计、分项和受限比例。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

财务分析人员和研究人员可用它整理年报或半年报中受限资产的类型、原因、期限及对应负债，并保留每项金额的原文依据。它不评估偿债能力或资产质量，也不计算可动用资金或提供投资建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports undeclared MCP discovery and risks involving endpoint credentials and external document processing.

Mitigation: Review the live MCP tools and destination services before connecting, and avoid sending sensitive reports unless their handling is approved.

Risk: The scan reports that the amount-to-quotation comparison described by the skill is missing.

Mitigation: Manually compare each reported amount with its cited source passage and verify totals and ratios before relying on the report.

Risk: The security analysis is partial, including partial inspection of the fixture runner.

Mitigation: Review behavior not covered by the scan before using the skill with sensitive documents or credentials.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huhoo/skills/cue-cn-restricted-assets-cn)
- [MCP setup](https://cuecue.cn/hub/mcp)
- [Omni Reader setup](https://cuecue.cn/hub/omni-reader)
- [API key setup](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown report with seven sections, source quotations, and location anchors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each reported figure is linked to its source passage; automated checks recalculate totals and ratios and flag prohibited conclusions.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
