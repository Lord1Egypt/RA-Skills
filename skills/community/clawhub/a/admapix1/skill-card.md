## Description:

AdMapix helps users search ad creatives, analyze apps, view rankings, track downloads and revenue, and explore market trends through the AdMapix API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to query AdMapix for ad creative discovery, app intelligence, rankings, estimated download and revenue trends, and market analysis. It supports English and Chinese responses and formats results for browsing, analysis, comparison, and deeper reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries about rankings, revenue, markets, downloads, apps, or creatives may send the user's query terms to AdMapix.

Mitigation: Use the skill only when you intend to query AdMapix with your own API key, and avoid submitting sensitive or confidential terms.

Risk: Download and revenue figures are third-party estimates and may be mistaken for official app store or publisher data.

Mitigation: Preserve the skill's estimate disclaimer when presenting download or revenue results and treat those numbers as directional intelligence.

Risk: The skill depends on an external API key and service availability.

Mitigation: Confirm SKILLBOSS_API_KEY is configured before use and handle missing credentials, rate limits, forbidden responses, empty results, and temporary upstream failures as described by the skill.

## Reference(s):

- [AdMapix website](https://www.admapix.com)
- [AdMapix API base](https://api.admapix.com)
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/admapix1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown with tables, summaries, links, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs follow the user's language and include disclaimers when presenting third-party estimated download or revenue data.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
