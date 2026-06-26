## Description: <br>
Retrieves related Alibaba Cloud search terms when provided an ALIYUN_RPA_RobotId value. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xnlc-qft](https://clawhub.ai/user/xnlc-qft) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve related Alibaba Cloud search queries through a trusted MCP tool by supplying the required robotId parameter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The robotId may identify an Alibaba Cloud or RPA setup and could be sensitive in some environments. <br>
Mitigation: Confirm which MCP server receives the robotId, use only trusted servers, and treat the value as sensitive unless your Alibaba Cloud/RPA setup confirms it is only a non-secret identifier. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xnlc-qft/get-ali-searches) <br>
- [Publisher profile](https://clawhub.ai/user/xnlc-qft) <br>


## Skill Output: <br>
**Output Type(s):** [Text] <br>
**Output Format:** [List of related search query strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the robotId parameter.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
