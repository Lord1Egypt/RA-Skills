## Description: <br>
当用户想去某个地方吃饭、探店，或者询问附近有什么好吃的时使用。能根据用户位置、时间、口味偏好和预算推荐合适的餐厅。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[newobject11](https://clawhub.ai/user/newobject11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to find nearby restaurants based on location, meal time, cuisine preference, and budget. It can call Baidu Maps for live nearby search and falls back to bundled city food data when live lookup is unavailable. <br>

### Deployment Geography for Use: <br>
Global; recommendations are most complete for Chinese cities covered by Baidu Maps and the bundled fallback data. <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided address, landmark, or area text and food search terms to Baidu Maps for live restaurant lookup. <br>
Mitigation: Prefer a neighborhood or landmark over an exact home address, and install only if this data sharing is acceptable. <br>
Risk: Live restaurant details may be stale or unavailable, especially for hours, pricing, ratings, and phone numbers. <br>
Mitigation: Confirm important details with the restaurant before traveling or making plans. <br>
Risk: The Baidu Maps API key is a sensitive credential required for live lookup. <br>
Mitigation: Provide it through BAIDU_MAP_API_KEY, use a restricted key, and avoid hardcoding it in files or prompts. <br>


## Reference(s): <br>
- [百度地图API文档参考](references/baidu_map_api.md) <br>
- [城市美食数据库格式说明](references/city_food_db.md) <br>
- [Baidu Maps API documentation](https://lbsyun.baidu.com/) <br>
- [Baidu Maps geocoding API guide](https://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-geocoding) <br>
- [Baidu Maps place search API guide](https://lbsyun.baidu.com/index.php?title=webapi/guide/webservice-placeapi) <br>
- [Baidu Maps API key console](https://lbsyun.baidu.com/apiconsole/key) <br>
- [ClawHub release page](https://clawhub.ai/newobject11/food-explorer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API Calls, Guidance] <br>
**Output Format:** [Markdown-style restaurant recommendations with optional Python usage examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ranked restaurant lists, addresses, phone numbers, prices, ratings, distances, local tips, and fallback recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
