## Description:

Connects an agent to the Ahrefs API to retrieve real-time SEO data for backlink analysis, keyword research, domain metrics, rank tracking, site audits, SERP review, and competitive intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonathan-sokol](https://clawhub.ai/user/jonathan-sokol)

### License/Terms of Use:


## Use Case:

Developers, marketers, and SEO analysts use this skill to have an agent call Ahrefs API endpoints, interpret returned SEO metrics, and provide actionable recommendations for keyword, backlink, competitor, rank-tracking, and technical-audit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends domains, URLs, keywords, and related SEO targets to the external Ahrefs API.

Mitigation: Use it only when submitting those targets to Ahrefs fits the user's data-handling policy.

Risk: The skill requires an Ahrefs API key and can consume paid API units.

Mitigation: Store the key securely, prefer environment variables, and set a scoped key or monthly API-unit limit where possible.

Risk: Rank Tracker and Site Audit workflows depend on pre-configured Ahrefs projects and plan permissions.

Mitigation: Confirm project setup, workspace permissions, and plan access before relying on those workflows.

## Reference(s):

- [ClawHub Ahrefs Connection listing](https://clawhub.ai/jonathan-sokol/skills/ahrefs-connection)
- [Ahrefs API documentation](https://docs.ahrefs.com/docs/api/reference/introduction)
- [Ahrefs API key management](https://app.ahrefs.com/account/api-keys)
- [Ahrefs pricing and limits](https://ahrefs.com/pricing)
- [Ahrefs limits and usage tracking](https://app.ahrefs.com/account/limits-and-usage/web)
- [Ahrefs API setup guide](references/setup.md)
- [Ahrefs API capabilities reference](references/capabilities.md)
- [Ahrefs API workflow patterns](references/workflows.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with API request examples, setup guidance, and SEO analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl commands, environment variable guidance, parsed JSON response summaries, and recommendations based on Ahrefs API results.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
