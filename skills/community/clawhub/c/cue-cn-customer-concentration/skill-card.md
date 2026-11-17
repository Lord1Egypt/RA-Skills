## Description:

为一家公司整理跨期客户集中度与依赖事实台账，逐行标注期间、口径和来源，并列明未取到的信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

面向分析师和研究人员，基于公司披露材料编制带来源锚点的跨期客户集中度台账，便于回查各期口径和客户占比。该技能不判断客户质量或风险大小。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional CUE_API_KEY may be sent to a service selected through the catalog without independent validation of the destination.

Mitigation: Check the current routing destination through a trusted source before configuring or using a key, and avoid sending credentials to an unverified endpoint.

Risk: Private or nonpublic disclosure files could be exposed to a third-party document service.

Mitigation: Use private documents only when authorized and after reviewing the destination and its data-handling terms.

Risk: The installation source is not pinned and the security scan has partial coverage.

Mitigation: Review the package contents and verify the release source before use, especially when handling sensitive material.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-customer-concentration)
- [CUE MCP configuration](https://cuecue.cn/hub/mcp)
- [CUE Omni Reader configuration](https://cuecue.cn/hub/omni-reader)
- [CUE API key setup](https://cuecue.cn/hub/api-key)
- [CUE MCP catalog](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Validation results]

**Output Format:** [Six-section Markdown ledger with period and accounting basis on data rows, source anchors, and individually listed information gaps; an optional fill-in skeleton is also available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes offline format and consistency checks. Per-customer detail depends on available retrieval and document-parsing channels; the skill does not assess customer quality or risk magnitude.]

## Skill Version(s):

0.1.0 (source: server release evidence, CHANGELOG 2026-11-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
