## Description:

把年报附注中的租赁信息整理为逐行附有原句和定位锚点的登记表，并核对租赁负债分档合计与使用权资产账面价值。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

面向需要整理中国企业年报租赁附注的分析人员，将租赁负债、使用权资产、租赁期、折现率及相关变动整理成可回查来源的登记稿，并检查关键金额勾稽。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports that the skill fetches an external MCP catalog and sends an API credential to a configurable endpoint, behavior it considers outside the stated lease-note analysis purpose.

Mitigation: Do not provide CUE_API_KEY until the network behavior and credential destination are independently understood; use user-supplied disclosure files without credentials when appropriate.

Risk: ClawScan guidance notes a possible gap in checking registered amounts against source quotations.

Mitigation: Manually verify each registered amount against its cited quotation and anchor before relying on the result.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-lease-liability-cn)
- [Publisher profile](https://clawhub.ai/user/huhoo)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown registration with source quotations, location anchors, source references, and validation findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed to retain source quotations and anchors; figures and conclusions require human review against the source disclosure.]

## Skill Version(s):

0.1.0 (source: release evidence, frontmatter, CHANGELOG.md; released 2026-11-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
