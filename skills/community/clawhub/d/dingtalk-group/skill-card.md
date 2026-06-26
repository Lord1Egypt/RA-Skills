## Description: <br>
调用钉钉开放平台 API，提供群聊管理功能（创建群、修改群、解散群、成员管理等）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[n-wen](https://clawhub.ai/user/n-wen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and administrators use this skill to create DingTalk internal group conversations for project collaboration, events, or managed announcements through DingTalk Open Platform credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create DingTalk internal groups using organization app credentials. <br>
Mitigation: Use a least-privilege DingTalk app and manually confirm owner and member IDs before running group-management commands. <br>
Risk: Debug output may expose request parameters or operational details in shared terminals, CI logs, or retained logs. <br>
Mitigation: Avoid --debug in CI or shared environments and keep DingTalk app secrets out of shared terminals and logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/n-wen/dingtalk-group) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration, code, JSON data] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON success or error output from the TypeScript script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DingTalk app credentials in environment variables and emits logs to stderr while writing result JSON to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
