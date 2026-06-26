## Description: <br>
查询并播报耳机设备的电量信息，包括耳机仓、左耳和右耳，并根据用户意图选择播报范围。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dory123456](https://clawhub.ai/user/dory123456) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill when asking an assistant about earbud, charging case, left earbud, or right earbud battery status and estimated remaining use time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can only answer accurately when the assistant already has legitimate access to current device battery values. <br>
Mitigation: Use it only in environments where those values are available, current, and permitted to be used in the response. <br>
Risk: Broad battery and duration trigger phrases may cause the skill to answer ambiguous questions that are not about earbud battery status. <br>
Mitigation: Confirm the intended device or ask a clarifying question when the user request does not clearly refer to the earbuds, charging case, or all device batteries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dory123456/device-battery-query) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Natural-language text response in Chinese] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Formats battery percentages and estimated remaining time for the earbud case, left earbud, and right earbud when those values are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
