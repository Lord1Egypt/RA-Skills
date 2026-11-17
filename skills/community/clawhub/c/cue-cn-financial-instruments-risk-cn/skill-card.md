## Description:

将年报或半年报中“金融工具及其风险”附注整理为逐行可追溯的登记表，并核算到期分档合计与利率、汇率敏感性。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

面向财务、审计及投资研究人员，帮助整理上市公司年报或半年报中的金融工具风险披露，并复核期限分档和敏感性计算。输出用于回查披露原文；流动性与偿债能力判断、评级和目标价仍需人工处理。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence flags possible external document processing and conflicting network assurances in the documented workflows.

Mitigation: Review current endpoints and document handling before use; if external processing is not intended, leave CUE_API_KEY unset and provide only user-supplied text.

Risk: The security scan is incomplete (75% coverage, including degraded tool-misuse analysis), so it does not establish a complete safety assessment.

Mitigation: Review the skill's workflows and dependencies before installation, treating the scan as partial evidence.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huhoo/skills/cue-cn-financial-instruments-risk-cn)
- [Cue MCP hub](https://cuecue.cn/hub/mcp)
- [Cue Omni Reader hub](https://cuecue.cn/hub/omni-reader)
- [Cue API key hub](https://cuecue.cn/hub/api-key)

## Skill Output:

**Output Type(s):** [Markdown, Analysis]

**Output Format:** [Markdown financial-risk register with source quotations, anchors, source IDs, and checker findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Seven-section register; reported figures remain traceable to cited disclosure text.]

## Skill Version(s):

0.1.0 (source: skill frontmatter; server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
