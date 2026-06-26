## Description: <br>
A simple skill send files to feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bingothreed](https://clawhub.ai/user/bingothreed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to send selected local image or video files through a configured Feishu app by obtaining a tenant token, uploading media, and sending a Feishu message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu App Secret or tenant access tokens could be exposed in logs, chat, or command history. <br>
Mitigation: Keep the App Secret and tenant token confidential, avoid pasting them into logs or chat, and review commands before execution. <br>
Risk: The agent could send the wrong local file or send media to the wrong Feishu recipient. <br>
Mitigation: Confirm the file path and recipient open_id before running file upload or message-send commands. <br>
Risk: The Feishu app could be configured with broader permissions than needed for the task. <br>
Mitigation: Use the least Feishu permissions needed for media upload and message sending. <br>


## Reference(s): <br>
- [OpenClaw Feishu channel documentation](https://docs.openclaw.ai/channels/feishu) <br>
- [Feishu app base information](https://open.feishu.cn/app/cli_a937fd6055791bca/baseinfo) <br>
- [Feishu message API explorer](https://open.feishu.cn/api-explorer/cli_a937fd6055791bca?apiName=create&project=im&resource=message&version=v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Feishu app credentials and local file paths supplied by the user.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
