## Description:

Provides Gaode Map tools for geocoding, POI search, nearby search, driving, transit, walking and cycling route planning, weather lookup, district lookup, and IP-based location.

This skill is ready for commercial/non-commercial use.

## Publisher:

[travel-skills](https://clawhub.ai/user/travel-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent workflows use this skill to search places, convert addresses and coordinates, plan routes across several travel modes, check weather, and request IP-based location data through a Gaode Map proxy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map queries, addresses, coordinates, route endpoints, weather cities, and optional IP-location lookups are sent to a remote proxy and downstream map API.

Mitigation: Avoid highly sensitive home, work, medical, or private travel locations unless the proxy operator is trusted; set PROXY_TOKEN only to a token intended for this proxy service.

Risk: Route, weather, and place results depend on live external services and may fail or return stale or incomplete data.

Mitigation: Treat critical travel or safety decisions as requiring independent verification, and handle request errors or empty results before relying on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/travel-skills/skills/gaode-map-pro)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON API responses that an agent can summarize as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the remote proxy and downstream Gaode Map API; the skill returns data responses and does not render map tiles or provide voice navigation.]

## Skill Version(s):

2.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
