## Description:

把 A 股权益分派实施公告整理为三日期时间轴和五类股东的税率、计税基数及税后实得记录，并为每条信息附上公告原句与出处锚点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT

## Use Case:

投资者和金融信息分析人员可用它从 A 股权益分派实施公告核对股权登记日、除权除息日、现金红利发放日，以及公告明确披露的分类型扣税信息。公告未披露的类别会标记为“未取到”，投资与税务判断留给人工。

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The security review flagged remote MCP service discovery that was not clearly aligned with the dividend timeline purpose; it also reports that the scan was incomplete and notes a missing privacy warning.

Mitigation: Before use, review the remote service connection and what announcement information it receives, and confirm privacy handling for any supplied credentials. Treat the scan as incomplete: 13 of 14 components were fully inspected.

## Reference(s):

- [Dividend tax terms and criteria](artifact/references/dividend-tax-terms.md)
- [Cue MCP catalog](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Structured Markdown timeline with quoted announcement text and source anchors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Three date nodes and five shareholder classes; undisclosed details are marked 未取到.]

## Skill Version(s):

0.1.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
