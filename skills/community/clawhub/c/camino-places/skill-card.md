## Description:

Locate places using flexible query formats, including free-form search and structured address components, and return coordinates, addresses, and optional street-level photos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[james-southendsolutions](https://clawhub.ai/user/james-southendsolutions)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to geocode addresses, look up named places, and retrieve structured place details from Camino's location API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer examples include mutable remote installation paths and an option to install a broad companion skill suite.

Mitigation: Install a pinned, reviewed version and choose only camino-places unless the additional Camino skills are required.

Risk: Place lookups send submitted location data to Camino's API.

Mitigation: Use a limited Camino API key where possible and avoid submitting private home addresses or sensitive locations unless that data sharing is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/james-southendsolutions/skills/camino-places)
- [Publisher profile](https://clawhub.ai/user/james-southendsolutions)
- [Camino API activation](https://app.getcamino.ai/skills/activate)
- [Camino search endpoint](https://api.getcamino.ai/search)

## Skill Output:

**Output Type(s):** [shell commands, JSON, guidance]

**Output Format:** [JSON API results with Markdown usage guidance and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAMINO_API_KEY, curl, and jq; accepts a free-form query or structured address fields.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
