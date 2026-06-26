## Description: <br>
说出你想吃什么，立刻搜索附近餐厅，按评分和距离排序，给出推荐理由。基于高德地图真实 POI 数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[770600682-cyber](https://clawhub.ai/user/770600682-cyber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to find nearby restaurants from natural-language food, price, distance, and location preferences. The agent queries AMap location data, ranks options, and returns concise restaurant recommendations with reasons. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an AMap API key. <br>
Mitigation: Store AMAP_API_KEY securely and avoid sharing it in prompts, logs, or public configuration. <br>
Risk: Address, landmark, and location queries are sent to AMap through the configured MCP server. <br>
Mitigation: Avoid submitting sensitive location details unless the user is comfortable sharing them with AMap for restaurant search. <br>
Risk: The setup runs the external @amap/mcp-server package through npx. <br>
Mitigation: Verify the package and configuration before installation or execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/770600682-cyber/amap-food-radar) <br>
- [AMap Open Platform](https://lbs.amap.com) <br>
- [AMap MCP Server documentation](https://lbs.amap.com/api/mcp-server/summary) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, guidance] <br>
**Output Format:** [Markdown tables and concise natural-language recommendations, with JSON configuration examples for setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations may include restaurant names, ratings, distance, average price, address, phone, hours, and ranked reasons when available from AMap.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
