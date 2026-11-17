## Description:

Researches public Bluesky accounts, posts, conversations, follower networks, account search, and trending topics through Crawlora.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and developers use this skill to investigate public Bluesky profiles, post threads and engagement, follower relationships, account search results, and trending topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bluesky handles, post URIs, search terms, and the Crawlora API key are sent to Crawlora.

Mitigation: Use a dedicated key stored in the environment, never in files or prompts; avoid sensitive or private research queries.

## Reference(s):

- [Bluesky research endpoint reference](artifact/reference/endpoints.md)
- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/bluesky-research)
- [Crawlora](https://crawlora.net)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Markdown summaries or JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Bluesky data; some result lists support cursor pagination.]

## Skill Version(s):

1.0.18 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
