## Description: <br>
Send images, files, audio, video and other media to Feishu users or chats via Feishu direct message or group chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yaqiangsun](https://clawhub.ai/user/yaqiangsun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to send local images, documents, audio, video, and other media to Feishu users or group chats. It is suited for workflows where a user explicitly asks to share a selected file through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected local files through Feishu, including sensitive content if the wrong path or recipient is used. <br>
Mitigation: Confirm the exact file path and Feishu recipient before each send. <br>
Risk: Fallback behavior can convert images to base64 or upload files to Feishu Drive after a failed send. <br>
Mitigation: Allow Feishu Drive fallback only when cloud storage and link sharing are explicitly intended. <br>
Risk: Workspace copies may remain after sensitive transfers. <br>
Mitigation: Delete staged workspace copies after sending sensitive files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yaqiangsun/feishu-send-media) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON tool-call examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to stage a local file, validate its path, send it through Feishu, and apply fallback transfer methods when needed.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
