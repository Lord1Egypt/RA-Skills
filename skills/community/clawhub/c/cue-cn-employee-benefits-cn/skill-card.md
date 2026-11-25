## Description:

把年报附注中的「应付职工薪酬」整理为可追溯至原句的登记稿，并用机检核对四数滚动、短期薪酬、两类离职后福利计划及辞退福利。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

审阅年报附注的财务分析人员可将用户提供的「应付职工薪酬」披露整理为逐项可追溯的登记稿，并核对四数滚动和福利计划分类。使用者应对照年报原文核实数据；此技能不评价薪酬水平，也不提供投资建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment flags remote MCP discovery and credential use as suspicious, and the partial scan does not establish that the skill is safe.

Mitigation: Before supplying CUE_API_KEY, independently verify the service endpoints, credential destination, and document handling; review the remaining component coverage.

Risk: The financial checks may not verify that quoted figures are accurate.

Mitigation: Treat the result as a draft and compare every figure and source quotation with the original annual-report disclosure.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huhoo/skills/cue-cn-employee-benefits-cn)
- [MCP setup](https://cuecue.cn/hub/mcp)
- [Omni Reader setup](https://cuecue.cn/hub/omni-reader)
- [API key setup](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown employee-benefits note organized into six sections, with source-linked numeric entries and checker findings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Numbers retain their source quotations, anchors, and source identifiers; the draft requires review against the original disclosure.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata, skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
