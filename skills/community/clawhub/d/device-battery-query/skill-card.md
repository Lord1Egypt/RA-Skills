## Description:

设备电量查询与播报。当用户询问电量、剩余电量、还有多少电、电池状态、耳机电量、耳机仓电量、左耳电量、右耳电量时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dory123456](https://clawhub.ai/user/dory123456)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to answer Chinese-language questions about headphone, charging case, left earbud, and right earbud battery level and estimated remaining use time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases such as “还有多少电” or “还能用多久” may activate the skill when the user intended a different battery context.

Mitigation: Review and narrow trigger phrases before installing if the agent handles multiple battery-related devices or workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dory123456/skills/device-battery-query)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Chinese natural-language battery status response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses cover the charging case, left earbud, and right earbud according to user intent.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
