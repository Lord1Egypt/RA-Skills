## Description: <br>
高德地图 API 调用工具，返回原始 JSON 数据 for China weather, geocoding, place search, route, distance, navigation, taxi, and trip-planning requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fangtianwd](https://clawhub.ai/user/Fangtianwd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for China-focused AMap weather, address, coordinate, place, route, navigation, taxi, and itinerary lookups. It helps the agent call the local amap command and work with the returned AMap JSON or URI links. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send weather, address, coordinate, route, taxi, itinerary, and IP lookup details to AMap. <br>
Mitigation: Avoid submitting sensitive personal locations or routes unless that disclosure is acceptable, and use a restricted AMap Web Service API key where possible. <br>
Risk: The skill depends on the amap executable installed in the user's PATH. <br>
Mitigation: Install only a trusted amap executable and review it before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Fangtianwd/fangtian-amap) <br>
- [AMap Web Service API key console](https://console.amap.com/dev/key/app) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Configuration guidance] <br>
**Output Format:** [JSON responses and URI links, with shell commands for setup and invocation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and an AMAP_API_KEY environment variable; REST commands return raw AMap JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
