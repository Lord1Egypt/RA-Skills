## Description:

Amazon Category Research helps sellers automate ASIN analysis, competitor research, and market intelligence for Amazon categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuancheng888](https://clawhub.ai/user/yuancheng888)

### License/Terms of Use:

MIT

## Use Case:

External sellers and operators use this skill to collect Amazon category, ASIN, competitor, SellerSprite, and SIF signals and turn them into a structured Feishu research report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Feishu authorization and uploads full research reports to Feishu.

Mitigation: Use it only when Feishu retention, sharing, and account authorization are acceptable for the research being handled.

Risk: The skill stores complete Markdown research reports locally before upload.

Mitigation: Run it in a workspace with appropriate access controls and avoid confidential product strategy unless local retention is approved.

Risk: The selector self-healing workflow can persist selector changes.

Mitigation: Disable or restrict selector self-healing in production agent environments unless changes are reviewed by a maintainer.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuancheng888/skills/amz-cat-research)
- [Output Template](references/output-template.md)
- [Negative Rules](references/negative-rules.md)
- [Selectors](references/selectors.md)
- [BSR Node Mapping](references/bsr-node-mapping.md)
- [SellerSprite](https://www.sellersprite.com/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown report saved locally and published as a Feishu cloud document, with a short link summary returned to the user.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires browser access, Feishu authorization, and SellerSprite/SIF browser plugins for complete data collection.]

## Skill Version(s):

5.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
