## Description: <br>
Converts batches of place names into BD-09 longitude and latitude coordinates with Baidu Maps APIs and saves CSV and JSON results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ggyybb](https://clawhub.ai/user/ggyybb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and data analysts use this skill to turn place-name lists into Baidu BD-09 coordinates for mapping workflows that rely on Baidu Maps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searched place names and the Baidu Maps AK are sent to Baidu Maps APIs. <br>
Mitigation: Use a restricted AK where possible and avoid processing sensitive location lists. <br>
Risk: CSV and JSON outputs are saved locally in the run directory. <br>
Mitigation: Treat generated files as local artifacts and delete or protect them when they contain sensitive locations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ggyybb/address2lnglat) <br>
- [Baidu Maps Open Platform](https://lbsyun.baidu.com/) <br>
- [Baidu Maps Place API endpoint](https://api.map.baidu.com/place/v2/search) <br>
- [Baidu Maps Geocoding API endpoint](https://api.map.baidu.com/geocoding/v3/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files, Text] <br>
**Output Format:** [Markdown guidance with shell commands plus generated CSV and JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Baidu Maps AK and saves CSV/JSON outputs in the run directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
