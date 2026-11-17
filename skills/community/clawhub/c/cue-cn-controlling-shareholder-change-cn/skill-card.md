## Description:

登记A股控制权变更与要约收购的八项要素，并将每项锚定到披露原文；比例与对价只采用公告披露内容，不自行计算。

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

A-share investors and analysts use this skill to turn control-change and tender-offer filings into an eight-item, source-anchored record. It keeps missing disclosures explicit and leaves investment judgments for human review.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Sending URLs or local paths to the external parsing service may reveal private information.

Mitigation: Use public filing URLs or sanitized copies; for sensitive material, use the documented user-supplied local-file path.

Risk: A weakness in a financial-data check may leave a reported figure incorrect.

Mitigation: Verify figures against the original filing sentence and its anchor; do not infer ratios or consideration from other values.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-controlling-shareholder-change-cn)
- [CUE MCP catalog](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown structured note with filing quotations, source anchors, and a not-obtained list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Eight control-change items; tender-offer price and premium are separate when applicable.]

## Skill Version(s):

0.1.0 (source: server-resolved release, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
