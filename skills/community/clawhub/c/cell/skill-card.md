## Description: <br>
根据移动/联通/电信基站参数查询大致位置（经纬度与地址）。当用户说：根据基站小区号查大概位置，或类似基站定位问题时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and end users use this skill to query approximate latitude, longitude, address, and accuracy from mobile, Unicom, or Telecom base-station identifiers through JisuAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried base-station identifiers and returned locations may be privacy-sensitive. <br>
Mitigation: Share only necessary tower data with JisuAPI, avoid submitting sensitive or unauthorized location queries, and handle returned coordinates and addresses as sensitive data. <br>
Risk: The skill requires a JISU_API_KEY and sends requests to the JisuAPI cell query service. <br>
Mitigation: Store the API key in the environment, avoid logging or sharing it, rotate it if exposed, and confirm the account is allowed to use the cell query API. <br>
Risk: Returned tower locations are approximate and may be incomplete when the provider has no matching information. <br>
Mitigation: Treat the result as coarse location context, surface uncertainty to users, and verify important decisions with another trusted location source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/cell) <br>
- [JisuAPI cell query API documentation](https://www.jisuapi.com/api/cell/) <br>
- [JisuAPI homepage](https://www.jisuapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request/response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and JISU_API_KEY; returns the API result object or an error object.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
