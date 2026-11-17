## Description:

Generates Chinese e-commerce product descriptions with platform, style, audience, batch-count, and report options for conversion-focused sellers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yyq56565656](https://clawhub.ai/user/yyq56565656)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers, brand teams, and marketers use this skill to draft product descriptions for Chinese commerce platforms such as Taobao, JD, and Pinduoduo. It supports style and audience customization and returns descriptions with estimated conversion, click-rate, and recommendation metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted product names or arguments may be copied into terminal commands.

Mitigation: Quote CLI arguments, avoid pasting untrusted text directly into a shell, and review commands before execution.

Risk: Large generation counts can create excessive output because the artifact does not enforce a maximum count.

Mitigation: Use small count values for normal runs and add explicit count limits before unattended or automated use.

Risk: Generated conversion, click-rate, and recommendation metrics may be mistaken for validated business forecasts.

Mitigation: Treat generated metrics as illustrative and validate marketing claims against real campaign or sales data before publication.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/yyq56565656/skills/ai-ecommerce-description-generator-v2)
- [Competitive Analysis Report](artifact/\u7ade\u54c1\u5206\u6790\u62a5\u544a.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown-style CLI report text with product descriptions and estimated performance metrics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated descriptions and metrics are randomized; keep generated counts small until input limits are enforced.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
