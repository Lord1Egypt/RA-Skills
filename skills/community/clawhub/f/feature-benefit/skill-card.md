## Description:

把 Amazon 商品特性连接到评论证据支持的用户利益，并提出 Listing 表达建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers use this skill to connect product features with benefits supported by customer review evidence and shape listing copy. It is intended for evidence-based listing recommendations, not advertising bids, unsupported claims, or automatic page publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This release includes broader account controls and may spend credits during an operation presented as a free preview.

Mitigation: Prefer a release restricted to listing/benefits. Before connecting this version, set ARI to ask before every charge, use quote commands for previews, and keep collection manual unless recurring costs are approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/funewa/skills/feature-benefit)
- [Amazon 特性利益点表达工作流](references/operation-workflow.md)
- [ARI CLI 与 API 参考](references/reference.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown with review-evidence-based listing recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations should stay within the available product and review evidence.]

## Skill Version(s):

1.5.3 (source: server-resolved release metadata, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
