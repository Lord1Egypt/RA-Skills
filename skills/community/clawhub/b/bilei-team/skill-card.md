## Description:

Coordinates four roles to research products, audit sources, compare costs and risks, and produce an evidence-based buying recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhashushu](https://clawhub.ai/user/zhashushu)

### License/Terms of Use:

MIT

## Use Case:

For Chinese-speaking shoppers weighing expensive purchases or safety-critical products. It organizes evidence checks, quantitative comparisons, and current price research into a recommendation with an audit trail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command is unpinned.

Mitigation: Review the source and pin the release or commit before installing.

Risk: The skill's tool scope is unclear.

Mitigation: Review the tools and permissions it needs before enabling it.

Risk: The scan reports possible calculation and evidence-rating reliability issues, and some references were unresolved.

Mitigation: Check calculations and cited evidence independently, and resolve unavailable references before relying on a recommendation.

## Reference(s):

- [避雷选品团.skill release on ClawHub](https://clawhub.ai/zhashushu/skills/bilei-team)
- [Category profiles](references/category_profiles.md)
- [Source-audit guide](references/agent1_blacklist.md)
- [Decision framework](references/agent3_verdict.md)
- [Output templates](references/output_template.md)
- [Related lightweight skill: 避雷.skill](https://github.com/zhashushu/bilei-skill)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Chinese Markdown buying report and shareable Markdown summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Evidence-led recommendations, source notes, comparisons, and time-sensitive price findings; report depth varies with budget and risk.]

## Skill Version(s):

1.0.8 (source: frontmatter; server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
