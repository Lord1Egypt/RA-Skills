## Description: <br>
钓鱼热点推送聚合高德 POI、和风天气和社交文本情报，按位置、天气和鱼情推荐附近钓点并生成 HTML 报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to discover nearby fishing hotspots, combine current weather and location signals with fishing reports, and prepare a ranked HTML summary for trip follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse AMap and QWeather credentials from fishing-trip-planner without a separate per-skill consent boundary. <br>
Mitigation: Review or remove ~/.fishing-planner/config.json sharing and configure separate credentials when credential isolation is required. <br>
Risk: The skill stores location-based fishing reports under the user's home directory. <br>
Mitigation: Review generated ~/.fishing-hotspot reports and restrict or delete stored location history when it is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bettermen/fishing-hotspot-push) <br>
- [Skill homepage](https://github.com/bettermen/fishing-hotspot-push) <br>
- [API 密钥获取指南](references/api_guide.md) <br>
- [高德地图 API](https://lbs.amap.com/) <br>
- [和风天气 API](https://dev.qweather.com/) <br>
- [fishing-trip-planner integration](https://github.com/bettermen/fishing-trip-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash commands; the bundled script produces HTML reports and JSON history/configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AMap and QWeather API keys; may reuse fishing-trip-planner credentials and stores reports under the user's home directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
