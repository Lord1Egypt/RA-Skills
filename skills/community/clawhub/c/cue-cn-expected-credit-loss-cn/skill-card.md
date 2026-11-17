## Description:

整理年报或半年报附注中的预期信用损失信息，逐项记录三阶段、组合及单项计提和前瞻性依据，并为数字附原句与定位锚点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

财报分析人员可用它将年报或半年报附注中的预期信用损失信息整理为逐项可追溯的登记稿，并运行离线检查核对引用、阶段归属、计提比例和准备金滚动关系。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags unclear credential handling and external document processing, and its analysis was partial.

Mitigation: Before supplying CUE_API_KEY or financial reports, review the connected retrieval and document processing services and confirm the documents are authorized for that use.

Risk: The security assessment notes weaknesses in financial validation checks; script checks do not establish that the source figures or accounting treatment are correct.

Mitigation: Verify each entry against the cited report note and have a qualified reviewer assess accounting judgments; do not use the output to decide whether provisions are adequate or to make investment recommendations.

## Reference(s):

- [CUE MCP hub](https://cuecue.cn/hub/mcp)
- [CUE Omni Reader](https://cuecue.cn/hub/omni-reader)
- [CUE API key information](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown structured-note register with source quotations and location anchors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Seven sections; figures are transcribed from source notes, with disclosed ratios and roll-forward totals checked offline.]

## Skill Version(s):

0.1.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
