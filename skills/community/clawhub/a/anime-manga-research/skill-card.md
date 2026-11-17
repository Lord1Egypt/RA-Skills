## Description:

Researches anime and manga through the Crawlora API, returning JSON for title details, characters, staff, recommendations, rankings, and airing schedules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Anime and manga fans, researchers, and developers can find titles and characters, check cast and staff, compare recommendations and rankings, and look up airing schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Anime and manga searches and filters are sent to the third-party Crawlora API.

Mitigation: Do not include personal, sensitive, or confidential text in searches.

Risk: The skill requires a Crawlora API key.

Mitigation: Keep the key in the CRAWLORA_API_KEY environment variable; do not include it in prompts, queries, or committed files.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/anime-manga-research)
- [Crawlora](https://crawlora.net)
- [Endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and ranking results may be paginated.]

## Skill Version(s):

1.0.18 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
