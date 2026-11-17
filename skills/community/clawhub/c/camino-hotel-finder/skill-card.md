## Description:

Search for hotels, hostels, and lodging near landmarks, conference venues, or neighborhoods using Camino AI's location intelligence with AI-powered ranking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find hotels, hostels, and other lodging near landmarks, conference venues, neighborhoods, airports, or coordinates, with Camino AI ranking results for proximity and relevance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and optional coordinates are sent to Camino.

Mitigation: Avoid submitting sensitive travel plans or exact coordinates unless sharing them with Camino is acceptable.

Risk: Install examples are not pinned.

Mitigation: Install a trusted, specific skill release or version when possible.

Risk: The skill requires CAMINO_API_KEY.

Mitigation: Store and handle the API key as a credential, and avoid exposing it in logs, prompts, or shared configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/james-southendsolutions/skills/camino-hotel-finder)
- [Camino API key activation](https://app.getcamino.ai/skills/activate)
- [Camino API](https://api.getcamino.ai/query)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON lodging search results with a human-readable answer field, plus Markdown usage guidance and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and CAMINO_API_KEY for the provided shell script path.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
