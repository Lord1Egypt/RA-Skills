## Description: <br>
智能通勤助手，实时查询驾车、公交、骑行、步行路线，结合天气和路况，推荐最优通勤方案并可生成高德导航二维码。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[f0ll0wwind](https://clawhub.ai/user/f0ll0wwind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Commuters use this skill to compare driving, public transit, cycling, and walking routes for daily trips, factoring in AMAP traffic, weather, route restrictions, nearby facilities, and optional monthly commute summaries. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Commute addresses, coordinates, and optional license plate numbers may be sent to AMAP for route, weather, traffic, and restriction checks. <br>
Mitigation: Use the skill only when this third-party data sharing is acceptable, and provide license plate numbers only when restriction checks are needed. <br>
Risk: commute_log.json can contain sensitive location history used for monthly commute reports. <br>
Mitigation: Avoid creating or updating the log unless monthly reports are desired, and delete the file regularly when it is no longer needed. <br>
Risk: The skill requires an AMAP Web Service API key. <br>
Mitigation: Store AMAP_API_KEY as a local secret or environment variable and avoid exposing it in prompts, logs, screenshots, or shared outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/f0ll0wwind/commute-survival-guide) <br>
- [AMAP Open Platform](https://lbs.amap.com/) <br>
- [AMAP Web Service API Overview](https://lbs.amap.com/api/webservice/summary) <br>
- [AMAP Direction API Documentation](https://lbs.amap.com/api/webservice/guide/api/direction) <br>
- [AMAP Weather API Documentation](https://lbs.amap.com/api/webservice/guide/api/weather) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style commute recommendations, API request examples, terminal QR code output, and JSON commute log records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call AMAP Web Service APIs with AMAP_API_KEY and may append commute history to commute_log.json when monthly reports are requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
