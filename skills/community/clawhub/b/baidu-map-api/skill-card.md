## Description: <br>
使用百度地图Web服务API进行地点搜索、天气查询、路线规划和地理编码。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coreyleung-art](https://clawhub.ai/user/coreyleung-art) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to answer map-related requests through Baidu Maps Web Service APIs, including place search, geocoding, weather lookup, route planning, district lookup, and IP location. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Map queries, addresses, coordinates, and requested IP geolocation data are sent to Baidu Maps APIs. <br>
Mitigation: Use the skill only when the user accepts that data sharing, and avoid IP-based location unless the user clearly asks for it. <br>
Risk: The Baidu Maps Access Key is required for API calls and could be exposed if copied into prompts, logs, or shared output. <br>
Mitigation: Store BAIDU_MAP_AK as a secret environment variable and avoid printing or echoing it during use. <br>


## Reference(s): <br>
- [Baidu Maps Open Platform](https://lbsyun.baidu.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and API response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and a BAIDU_MAP_AK environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
