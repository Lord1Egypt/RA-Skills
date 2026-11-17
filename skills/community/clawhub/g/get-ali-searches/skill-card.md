## Description:

Retrieves related Aliyun (Alibaba Cloud) search suggestions through an MCP call that requires a robotId value.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xnlc-qft](https://clawhub.ai/user/xnlc-qft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve Aliyun-related search terms by supplying the required ALIYUN_RPA_RobotId value through an MCP tool call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An incorrect or untrusted ALIYUN_RPA_RobotId could route the MCP call to the wrong Aliyun workflow.

Mitigation: Confirm that the MCP tool and ALIYUN_RPA_RobotId value are from a trusted Aliyun workflow before installing or using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xnlc-qft/skills/get-ali-searches)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown guidance with a list-shaped text result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a trusted ALIYUN_RPA_RobotId value.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
