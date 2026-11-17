## Description:

Records inventory, receivables, and contract asset balances, ageing, and provisions from Chinese listed-company filings, anchoring each item to its source and labeling calculations when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhoo](https://clawhub.ai/user/huhoo)

### License/Terms of Use:

MIT-0

## Use Case:

Financial analysts and documentation teams use this skill to prepare source-anchored working-capital notes from A-share annual, interim, and quarterly reports. It records disclosed figures and calculation bases while leaving quality and compliance judgments to a human.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flagged external MCP service discovery and privacy concerns, with partial analysis of one shell script; report links, credentials, or local paths may be sensitive.

Mitigation: Review the MCP services and data being provided before use; avoid supplying private links, credentials, or local paths unless needed, and inspect the incompletely analyzed shell script before running it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huhoo/skills/cue-cn-working-capital-quality)
- [CUE MCP catalog](https://cuecue.cn/api/mcp-catalog)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Five-section Markdown working-capital note with filing quotations, source anchors, and any calculation bases]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers inventory, receivables, contract assets, provisions, and explicitly named data gaps.]

## Skill Version(s):

0.1.1 (source: release evidence, SKILL.md frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
