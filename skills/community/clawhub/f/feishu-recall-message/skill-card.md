## Description: <br>
撤回飞书群聊或单聊中的消息，支持单条撤回、批量撤回和按时间范围撤回。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tz826](https://clawhub.ai/user/tz826) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
开发者和运维人员可以用此技能指导代理以已授权的飞书用户身份撤回群聊或单聊消息，包括引用消息、批量消息和指定时间范围内的消息。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk or time-range recall could remove many Feishu messages through the user's account. <br>
Mitigation: Require the agent to show the chat, time window, message count, senders, and message IDs, then obtain explicit confirmation before executing the recall. <br>
Risk: The recall operation uses user OAuth authority and may affect messages beyond the intended scope. <br>
Mitigation: Use a least-privileged Feishu account where possible and confirm that the account has only the permissions needed for the intended recall. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tz826/feishu-recall-message) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides Feishu message recall workflows, required OAuth scope, API action examples, pagination notes, and result reporting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
