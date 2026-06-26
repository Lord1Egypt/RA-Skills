## Description: <br>
Gaode Map All-in-One provides POI search, route planning, weather lookup, bus/transit queries, traffic status, geocoding, reverse geocoding, IP location, and input suggestions through the Gaode/Amap Web Service API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mahongting](https://clawhub.ai/user/mahongting) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to query AMap location services from an agent workflow, including place search, address lookup, routing, weather, traffic, and JSON-formatted results. Users must provide their own Gaode/Amap API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map searches, addresses, coordinates, route endpoints, IP-location lookups, and the Gaode/Amap API key are sent to AMap services. <br>
Mitigation: Use the skill only when this disclosure is acceptable, avoid sensitive location queries unless necessary, and review AMap account and service terms before use. <br>
Risk: Passing an API key directly on the command line can expose it through shell history or process inspection. <br>
Mitigation: Prefer the AMAP_API_KEY environment variable, keep shell profile files private, and rotate the key if it may have been exposed. <br>


## Reference(s): <br>
- [Amap Search on ClawHub](https://clawhub.ai/mahongting/amap-search) <br>
- [Gaode Open Platform](https://lbs.amap.com/) <br>
- [OpenClaw Community](https://clawd.org.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an AMAP_API_KEY environment variable or command-line API key; commands may call external Gaode/Amap web services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
