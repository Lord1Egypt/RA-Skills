## Description: <br>
在百度/Google 坐标系下做经纬度与地址互转。当用户说：把这个地址转成经纬度、这两个坐标是什么地方？或类似地图坐标问题时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to convert addresses to coordinates or coordinates to addresses through JisuAPI. It supports Baidu and Google coordinate types for location lookup workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Addresses and coordinates submitted to the skill are sent to JisuAPI for conversion. <br>
Mitigation: Use a dedicated JISU_API_KEY, monitor quota, and avoid submitting sensitive private locations unless third-party processing is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/geoconvert) <br>
- [JisuAPI profile](https://clawhub.ai/user/jisuapi) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>
- [JisuAPI geoconvert documentation](https://www.jisuapi.com/api/geoconvert/) <br>
- [JisuAPI coord2addr endpoint](https://api.jisuapi.com/geoconvert/coord2addr) <br>
- [JisuAPI addr2coord endpoint](https://api.jisuapi.com/geoconvert/addr2coord) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [JSON from the geoconvert script, with human-facing guidance from the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; sends submitted addresses or coordinates to JisuAPI.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata, released 2026-04-03) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
