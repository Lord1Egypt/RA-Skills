## Description:

Finds YouTube micro-influencers and niche creators for sponsorship or partnership outreach using apidojo's YouTube scraper on Apify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External marketing, sponsorship, podcast, and affiliate teams use this skill to discover smaller YouTube channels in a niche, filter by subscriber count and engagement, and prepare ranked outreach lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify tokens can be exposed if the token-in-URL REST fallback is used or command output is logged.

Mitigation: Use a narrowly scoped APIFY_TOKEN through environment variables or authenticated tooling, and avoid putting tokens in URLs, shell history, or logs.

Risk: The skill collects creator contact information for outreach workflows.

Mitigation: Use contact data only for appropriate business outreach, follow YouTube terms, privacy laws, and anti-spam rules, and avoid bulk messaging without consent or legitimate basis.

Risk: YouTube metrics and contact information may be stale or incomplete.

Mitigation: Manually verify top recommendations, channel fit, subscriber counts, engagement, and contact details before outreach.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-youtube-micro-influencers)
- [Publisher profile](https://clawhub.ai/user/apidojo-io)
- [Apify Actor: apidojo/youtube-scraper](https://apify.com/apidojo/youtube-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, ranked lists, and inline bash/API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save Apify results as JSON or CSV when the agent uses the documented runner.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
