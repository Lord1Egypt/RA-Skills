## Description:

Search Allegro marketplaces and retrieve structured offer, product, seller, pricing, sales, and review data across Poland, Czechia, Slovakia, and Hungary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and marketplace researchers use this skill to search Allegro listings, compare seller prices, review product and seller information, and monitor marketplace data across four Central European sites.

### Deployment Geography for Use:

Global; marketplace data covers Poland, Czechia, Slovakia, and Hungary.

## Known Risks and Mitigations:

Risk: The security scan was benign with medium confidence and partial coverage; it does not establish that the external API destination is trustworthy.

Mitigation: Confirm that you trust and need the Scavio API service before providing it an API key.

Risk: The skill documentation notes Allegro terms that may restrict downloading, using, or aggregating marketplace data.

Mitigation: Check applicable Allegro terms and permissions for your intended use before collecting or using the data.

## Reference(s):

- [Allegro API documentation](https://scavio.dev/docs/allegro-search?utm_source=agent-skills&utm_medium=skill&utm_campaign=allegro-api)
- [ClawHub skill release](https://clawhub.ai/scavio-ai/skills/allegro-api)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON marketplace data with concise summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prices are reported with their market currency; listing text is returned in the site's language.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
