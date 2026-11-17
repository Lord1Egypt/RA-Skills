## Description:

Writes and publishes SEO-optimized blog posts for canmarket.ai, including topic research, article drafting, Nuxt page creation, build verification, Git deployment, and optional DEV.to cross-posting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and CanMarket maintainers use this skill to create, SEO-check, publish, and deploy blog posts for CanMarket's production website.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can push directly to the CanMarket production site with broad Git staging.

Mitigation: Require a clean working tree, stage only known blog files, review the full diff, and prefer a feature branch or pull request before deployment.

Risk: Published posts may contain unreviewed claims, bylines, or simulation data.

Mitigation: Review all claims, bylines, and cited CanMarket simulation data before publishing or cross-posting.

## Reference(s):

- [Canlah AI](https://canlah.ai)
- [CanMarket](https://canmarket.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/canmarket-blog)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with Vue/Nuxt, TypeScript, JSON-LD, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify blog page files and Git commits when executed in the target site repository.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
