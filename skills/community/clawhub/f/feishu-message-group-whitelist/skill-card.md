## Description: <br>
Filters Feishu group-chat messages against a configurable whitelist so the agent replies only when a message contains an approved keyword. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnhejunlin](https://clawhub.ai/user/johnhejunlin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of Feishu group-chat agents use this skill to reduce noisy or unintended replies by allowing responses only for configured keywords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An empty whitelist allows normal replies instead of suppressing all group-chat responses. <br>
Mitigation: Keep config/whitelist.txt populated before deployment, or change the fail-open behavior if an empty whitelist should mean no replies. <br>
Risk: Group-message inspection may be sensitive or regulated in some environments. <br>
Mitigation: Notify participants or obtain consent where required, and confirm the whitelist keywords are appropriate before installation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [configuration, guidance, text] <br>
**Output Format:** [Markdown and plain-text configuration entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a newline-delimited whitelist file at config/whitelist.txt; an empty whitelist is documented to allow normal replies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
