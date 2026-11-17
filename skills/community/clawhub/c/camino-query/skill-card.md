## Description:

Search for places using natural language with Camino AI's location intelligence API, returning relevant results with coordinates, distances, and metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to search for real-world places with natural-language queries and optional coordinates. It supports place lookup workflows that need coordinates, distances, place metadata, pagination, and optional natural-language summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends CAMINO_API_KEY with the search query and optional location parameters to Camino's API.

Mitigation: Treat CAMINO_API_KEY as a secret and avoid submitting sensitive queries or precise locations unless that data sharing is appropriate.

Risk: Mutable install commands or unreviewed remote sources can change what code is installed.

Mitigation: Install from a trusted, reviewed ClawHub package or a pinned version/source.

## Reference(s):

- [Query skill page on ClawHub](https://clawhub.ai/james-southendsolutions/skills/camino-query)
- [Camino API key activation](https://app.getcamino.ai/skills/activate)
- [x402 payment protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions, API Calls, Guidance]

**Output Format:** [Markdown usage guidance and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAMINO_API_KEY, curl, and jq; sends the search query and optional location parameters to Camino's API.]

## Skill Version(s):

2.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
