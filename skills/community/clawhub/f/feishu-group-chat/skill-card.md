## Description: <br>
Helps agents participate in Feishu group chats by constructing user-authorized post messages, mentions, and optional image messages for configured groups and contacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clear0](https://clawhub.ai/user/clear0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let configured agents send, reply to, mention, and optionally share generated images in Feishu group chats through a user-authorized account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends Feishu messages through a user-authorized account, so recipients may see messages as coming from a human user identity. <br>
Mitigation: Use a dedicated Feishu account where possible and make sure group participants understand that bot-prefixed messages may be automated. <br>
Risk: The skill stores group and contact identifiers in config.json and can read recent group messages. <br>
Mitigation: Restrict configured groups and contacts, review config.json and contact memory files, and keep sensitive identifiers out of shared artifacts. <br>
Risk: The skill can upload local images to Feishu when image sending is requested. <br>
Mitigation: Avoid uploading sensitive local images and review generated or selected image paths before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clear0/feishu-group-chat) <br>
- [Publisher profile](https://clawhub.ai/user/clear0) <br>
- [README](README.md) <br>
- [Permissions](PERMISSIONS.md) <br>
- [Configuration template](config-template.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces source-friendly shell variables for Feishu message payloads; may upload local images when requested.] <br>

## Skill Version(s): <br>
1.1.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
