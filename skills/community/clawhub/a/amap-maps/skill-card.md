## Description: <br>
Amap LBS services. Call Amap services via Streamable HTTP MCP, supporting geocoding, route planning, POI search, weather query, distance measurement, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elric2011](https://clawhub.ai/user/elric2011) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to query Amap location services from a Node.js CLI for geocoding, POI lookup, route planning, weather, distance measurement, IP location, and Amap URI generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map, route, IP-location, and place queries are sent to Amap and may include sensitive location or travel data. <br>
Mitigation: Avoid submitting home, customer, internal, or sensitive travel-location data unless sharing it with Amap is acceptable. <br>
Risk: The Amap API key could be exposed through logs, shell history, shared terminals, or copied command output. <br>
Mitigation: Use a dedicated Amap API key, keep it in the AMAP_KEY environment variable, avoid printing it, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [Amap MCP Server Official Documentation](https://lbs.amap.com/api/mcp-server/summary) <br>
- [Amap API Key Registration Guide](https://lbs.amap.com/api/javascript-api-v2/guide/abc/register) <br>
- [ClawHub Skill Page](https://clawhub.ai/elric2011/amap-maps) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown instructions and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18+ and an AMAP_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
