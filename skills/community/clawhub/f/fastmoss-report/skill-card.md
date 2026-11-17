## Description:

Fastmoss Report generates TikTok FastMoss hot-product daily and weekly top-10 reports with data insights and product-selection recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[islcy1208](https://clawhub.ai/user/islcy1208)

### License/Terms of Use:


## Use Case:

E-commerce operators and agents use this skill to collect FastMoss TikTok hot-product rankings for a configured category and region, then generate a shareable HTML report with insights and sourcing recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill text exposes a plaintext FastMoss password.

Mitigation: Remove the plaintext password before installation and rotate any exposed FastMoss credential.

Risk: The skill can automatically deploy reports and share report links using configured credentials.

Mitigation: Require explicit user approval before any Vercel deployment or Feishu group sharing.

Risk: The skill documents storing credential rotation dates in memory.

Mitigation: Disable memory storage of credential rotation dates and keep credential handling outside persistent agent memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/islcy1208/skills/fastmoss-report)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [HTML report and Markdown-style progress messages with links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces daily and weekly Top 10 product tables, summary cards, insights, product-selection recommendations, and risk notes.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
