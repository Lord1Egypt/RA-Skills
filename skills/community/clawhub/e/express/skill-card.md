## Description: <br>
查快递物流轨迹与签收状态，支持自动识别公司与顺丰等校验。当用户说：这个单号到哪了？帮我查一下中通物流，或类似快递查询时，使用本技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuapi](https://clawhub.ai/user/jisuapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check shipment tracking status, delivery progress, signed status, and supported courier company codes through JisuAPI. It is intended for user-requested express logistics lookups where the user provides a tracking number and, for some couriers, the last four digits of a phone number. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shipment identifiers, and sometimes the last four digits of a phone number, are sent to JisuAPI. <br>
Mitigation: Use the skill only for user-requested tracking lookups, send only the fields required by the courier, and avoid adding unrelated personal data. <br>
Risk: The skill requires a JisuAPI key. <br>
Mitigation: Use a dedicated JisuAPI key in the JISU_API_KEY environment variable and avoid exposing the key in prompts, command history, logs, or shared outputs. <br>
Risk: Shell execution with user-provided tracking data can be unsafe if raw input is concatenated into commands. <br>
Mitigation: Construct the request as structured JSON and pass it as a quoted argument; strictly escape command arguments when a shell is unavoidable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuapi/express) <br>
- [JisuAPI](https://www.jisuapi.com/) <br>
- [JisuAPI express documentation](https://www.jisuapi.com/api/express) <br>
- [JisuAPI express query endpoint](https://api.jisuapi.com/express/query) <br>
- [JisuAPI express type endpoint](https://api.jisuapi.com/express/type) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON from the Python CLI, with agent-facing summaries derived from that JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the requests package, and JISU_API_KEY; accepts a JSON argument containing number, optional type, and optional mobile.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
