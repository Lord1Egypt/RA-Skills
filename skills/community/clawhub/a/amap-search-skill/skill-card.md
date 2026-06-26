## Description: <br>
Gaode/Amap all-in-one map skill for POI search, route planning, weather, bus or transit lookups, real-time traffic, geocoding, reverse geocoding, IP location, and input tips. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mahongting](https://clawhub.ai/user/mahongting) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Amap Web Service APIs for map search, routing, weather, traffic, geocoding, reverse geocoding, and related location lookup tasks from an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the Amap API key and location-related inputs such as addresses, coordinates, route endpoints, city names, and IP-location lookups to Amap services. <br>
Mitigation: Use a revocable Amap API key, prefer environment-variable configuration, and avoid submitting sensitive exact home, work, or travel details unless needed. <br>


## Reference(s): <br>
- [Amap Open Platform](https://lbs.amap.com/) <br>
- [ClawHub skill page](https://clawhub.ai/mahongting/amap-search-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Plain text or JSON command output with Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided AMAP_API_KEY and sends map queries to Amap services.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
