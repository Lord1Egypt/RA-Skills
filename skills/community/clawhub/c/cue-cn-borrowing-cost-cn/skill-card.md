## Description:

将年报借款费用资本化附注整理成逐项附有原文与定位锚点的登记表，并核对资本化和费用化金额。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

财务分析人员可将年报中的借款费用资本化披露整理为可追溯登记表，并核对专门借款、一般借款及资本化期间的披露。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marked the skill suspicious because it describes external MCP discovery and sending a credential to a configurable endpoint; analysis was partial.

Mitigation: Leave CUE_API_KEY unset when working from user-supplied notes. Before enabling retrieval, verify the endpoint and credential handling, and check figures against the cited filing text.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-borrowing-cost-cn)
- [CUE MCP catalog](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown ledger with source quotations, location anchors, and labeled missing items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Organizes disclosed figures for human review; does not provide investment recommendations or forecasts.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
