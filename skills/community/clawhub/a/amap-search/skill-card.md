## Description:

Amap Search helps an agent use Gaode/Amap web APIs for POI search, geocoding, reverse geocoding, route planning, weather lookup, traffic status, and input suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahongting](https://clawhub.ai/user/mahongting)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run location-service workflows that query Gaode/Amap for places, addresses, coordinates, routes, weather, and traffic information. Users must provide their own Amap API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Map searches, addresses, coordinates, route endpoints, IP lookup requests, and the Amap API key are sent to Gaode/Amap when the skill is used.

Mitigation: Use a restricted Amap API key, prefer the AMAP_API_KEY environment variable over command-line key entry, and avoid using sensitive locations or shared shell configuration on monitored systems.

## Reference(s):

- [Amap Open Platform](https://lbs.amap.com/)
- [ClawHub Amap Search Release](https://clawhub.ai/mahongting/skills/amap-search)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided AMAP_API_KEY or command-line API key.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
