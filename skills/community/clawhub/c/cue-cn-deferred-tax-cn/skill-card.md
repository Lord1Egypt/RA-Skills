## Description:

将财报中的递延所得税披露整理为逐项附原文摘录与位置锚点的登记表，覆盖项目明细、互抵四数、未确认亏损、所得税调节和税率口径。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

财务分析人员可用它从年报或公告中逐条登记递延所得税披露，并将金额、原文摘录和来源位置对应起来；附带的检查器可核对稿件结构和引用标记。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional document parsing can send filing content to an external service, and running the checker can create a persistent usage marker in the home directory.

Mitigation: Use supplied excerpts when they are sufficient; review the parsing provider's data handling before sending filings, and inspect the checker's local marker behavior before running it.

## Reference(s):

- [CUE MCP configuration](https://cuecue.cn/hub/mcp)
- [CUE document reader](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Markdown, Text]

**Output Format:** [Chinese Markdown report with seven sections and per-line source quotes and location anchors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps quoted disclosure text verbatim and marks missing disclosures explicitly.]

## Skill Version(s):

0.1.0 (source: release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
