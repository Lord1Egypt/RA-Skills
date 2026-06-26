## Description: <br>
中国快递物流查询工具，可查询顺丰、圆通、中通、申通、韵达、京东、EMS等中国快递公司的物流信息，并展示物流轨迹，无需API Key。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huanyuai](https://clawhub.ai/user/huanyuai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up Chinese courier tracking status and present current delivery state, tracking history, and a Kuaidi100 detail link. It is intended for explicit package-tracking requests where the user provides a tracking number and, when needed, the courier code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tracking numbers, and sometimes a phone-number last-four suffix for some SF lookups, are sent to Kuaidi100. <br>
Mitigation: Use the skill only for explicit courier tracking requests and avoid collecting or sending extra personal details unless the carrier lookup requires them. <br>
Risk: Frequent repeated lookups may cause temporary blocking or stale/no-result responses. <br>
Mitigation: Avoid repeated queries for the same tracking number more often than the documented 30-minute interval. <br>


## Reference(s): <br>
- [Courier Codes Reference](references/courier-codes.md) <br>
- [Kuaidi100 Query Endpoint](https://www.kuaidi100.com/query) <br>
- [ClawHub Skill Page](https://clawhub.ai/huanyuai/cn-express-tracker-noapi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text with inline shell commands and tracking results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes courier name, tracking number, current status, timestamped tracking events, and a Kuaidi100 detail link when data is available.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
