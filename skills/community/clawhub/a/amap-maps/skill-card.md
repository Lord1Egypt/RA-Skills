## Description:

Amap LBS services. Call Amap services via Streamable HTTP MCP, supporting geocoding, route planning, POI search, weather query, distance measurement, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elric2011](https://clawhub.ai/user/elric2011)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to call Amap location services from command-line workflows for weather, geocoding, POI search, route planning, distance measurement, IP location, and Amap URI generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends places, coordinates, routes, POI lookups, weather cities, IP addresses, and the Amap API key to Amap's remote service.

Mitigation: Use the skill only when sharing that location or routing data with Amap is intended, and avoid submitting sensitive home, workplace, or travel-pattern data.

Risk: The skill requires an AMAP_KEY for remote API access.

Mitigation: Store the key in the environment, rotate it if exposed, and avoid placing it in prompts, logs, or shared command transcripts.

## Reference(s):

- [Amap MCP Server Official Documentation](https://lbs.amap.com/api/mcp-server/summary)
- [Amap API Key Registration Guide](https://lbs.amap.com/api/javascript-api-v2/guide/abc/register)
- [ClawHub skill page](https://clawhub.ai/elric2011/skills/amap-maps)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and an AMAP_KEY environment variable; command results may include map, route, weather, POI, distance, IP-location, and URI data returned by Amap.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
