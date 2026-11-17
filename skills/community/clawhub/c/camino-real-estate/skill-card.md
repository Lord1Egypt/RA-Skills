## Description:

Evaluate any address for home buyers and renters, including nearby schools, transit, grocery stores, parks, restaurants, and walkability using Camino AI location intelligence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to evaluate residential locations from an address or latitude/longitude and return nearby amenities and walkability context for home-buying or rental decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends evaluated addresses or coordinates, search radius, and CAMINO_API_KEY to Camino's API.

Mitigation: Use it only when Camino's data handling terms are acceptable, and avoid highly sensitive home-location searches.

Risk: The skill depends on shell execution with curl and jq plus an environment-provided API key.

Mitigation: Install from a reviewed, pinned source when possible and keep the API key scoped to the intended agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/james-southendsolutions/skills/camino-real-estate)
- [Camino API key activation](https://app.getcamino.ai/skills/activate)
- [x402 payment protocol](https://x402.org)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON API responses and Markdown instructions with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAMINO_API_KEY, curl, and jq; accepts either an address or a latitude/longitude location plus an optional radius in meters.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
