## Description:

将财报或公告中的公允价值披露整理为逐条附带原文、定位锚点和来源的登记表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

面向财务分析人员和审阅者，用于把年报、半年报或公告中的公允价值计量、层次归属、估值技术、层次转换和第三层次变动整理为可回查来源的登记表。结果用于披露整理，不用于估值、减值测试或层次判断。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags an unclear online MCP and credential workflow, external document parsing concerns, and incomplete scan coverage.

Mitigation: Before enabling online services, clarify and limit credential destinations and document parsing to services you trust; review the components not covered by the scan.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huhoo/skills/cue-cn-fair-value-hierarchy-cn)
- [CUE MCP data access](https://cuecue.cn/hub/mcp)
- [CUE Omni Reader for long attachments and PDFs](https://cuecue.cn/hub/omni-reader)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown disclosure register with quoted source text, location anchors, and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Seven sections; missing disclosures are named explicitly. It records disclosed wording and does not infer valuation methods or fair value hierarchy assignments.]

## Skill Version(s):

0.1.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
