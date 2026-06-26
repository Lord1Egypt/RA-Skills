## Description: <br>
中国生活服务工具包，支持天气查询（街道级）、限行提醒、油价查询、快递物流跟踪、公交换乘查询等日常生活服务。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer China local-life service questions, including street-level weather, traffic restriction reminders, fuel prices, courier tracking, and public transit routing. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: Location, route, address, vehicle, or parcel details may be sent to external China-based service providers during lookups. <br>
Mitigation: Confirm with the user before sending precise addresses, courier tracking numbers, or other sensitive details to third-party services. <br>
Risk: Weather, traffic restriction, fuel price, courier, and transit results can be delayed or temporarily inaccurate. <br>
Mitigation: Present time-sensitive results with source and freshness context, and advise users to confirm critical travel or delivery decisions with official sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/cn-life-toolkit) <br>
- [Artifact README](README.md) <br>
- [Artifact skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown text responses with local-service lookup results and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include weather, traffic restriction, fuel price, courier tracking, or transit details sourced from external China-based service providers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
