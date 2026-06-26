## Description: <br>
Sends Feishu text messages, local images, and workspace files to a configured Feishu user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zh6](https://clawhub.ai/user/zh6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to send Feishu messages with text, supported image files, or supported document files from the local workspace to a configured recipient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages or files could be sent to the wrong Feishu recipient. <br>
Mitigation: Confirm the Feishu user ID and message content before sending. <br>
Risk: Workspace files may contain secrets or private documents. <br>
Mitigation: Inspect file paths and contents before sharing them through Feishu. <br>
Risk: Downloaded network images may come from untrusted sources before forwarding. <br>
Mitigation: Download images only from trusted URLs and review the saved file before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zh6/feishu-zh6) <br>
- [Publisher profile](https://clawhub.ai/user/zh6) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with message_tool examples and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local workspace files for Feishu image and file messages.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
