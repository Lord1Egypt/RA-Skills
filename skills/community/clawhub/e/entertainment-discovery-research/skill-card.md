## Description:

Researches movies and TV titles across IMDb, TMDB, JustWatch, Rotten Tomatoes, and Metacritic using the Crawlora API. Use for title discovery, cast and crew, ratings, critic and audience reviews, streaming offers, similar titles, and release comparisons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

External users can research and compare movies and TV shows, including cast and crew, platform ratings and reviews, similar titles, and region-specific streaming offers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment was partial and does not establish that the skill is free of risk.

Mitigation: Review the skill's documented behavior and consider whether you are comfortable with its Crawlora API use before installing.

Risk: Research requests send a Crawlora API key to the external Crawlora API service.

Mitigation: Use a key intended for Crawlora; the helper sends it over HTTPS and restricts requests to documented GET routes.

## Reference(s):

- [Endpoint reference](reference/endpoints.md)
- [Crawlora API](https://api.crawlora.net/api/v1)
- [Crawlora skill page](https://clawhub.ai/crawlora-org/skills/entertainment-discovery-research)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Concise research summaries and comparisons with source IDs, score definitions, locale, and retrieval time where applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserve platform-specific scores and counts separately; missing data means unavailable coverage, not zero.]

## Skill Version(s):

1.0.9 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
