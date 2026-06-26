## Description: <br>
Sends local files to Feishu chats from OpenClaw bot triggers or command line calls, with search and batch selection support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangxusong637](https://clawhub.ai/user/zhangxusong637) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and workspace operators use this skill to send one or more local workspace files to Feishu chats or users through a bot mention or an explicit CLI command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad chat triggers and keyword search can cause unintended files to be selected or uploaded. <br>
Mitigation: Use explicit bot mentions or CLI calls, verify the file list before sending, avoid broad searches and "all", and restrict usage to non-sensitive workspace paths. <br>
Risk: A missing or incorrect recipient can send files to the wrong Feishu chat or user. <br>
Mitigation: Always specify and verify the recipient, especially when using CLI mode with the --to parameter. <br>
Risk: The skill can upload arbitrary readable local files. <br>
Mitigation: Do not send sensitive paths, review requested file paths before upload, and limit runtime access to only the workspace files intended for sharing. <br>
Risk: World-writable log permissions may expose or alter runtime logs. <br>
Mitigation: Replace 0777 log permissions with owner-only permissions before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangxusong637/feishu-send-files) <br>
- [Publisher profile](https://clawhub.ai/user/zhangxusong637) <br>
- [ClawHub manual install link](https://clawhub.com) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, API Calls, Configuration] <br>
**Output Format:** [Plain text status messages and Feishu file-message API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, OpenClaw Feishu configuration, and readable local file paths; can send multiple selected files.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
