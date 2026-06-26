## Description: <br>
飞书消息直接发送文件附件技能。当用户需要直接通过飞书消息发送文件附件（而不是文档链接）时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gongjieliu](https://clawhub.ai/user/gongjieliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external collaborators, and developers use this skill to send local files as Feishu message attachments instead of document links. It is intended for single-file and reviewed batch sends where the sender controls the file path and display name. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports local file discovery and batch upload patterns that could send unintended files. <br>
Mitigation: Use explicit file paths, review each selected file, and approve each send before calling the message tool. <br>
Risk: Files sent through Feishu may contain sensitive, regulated, or confidential content. <br>
Mitigation: Verify the recipient or channel and avoid sending sensitive or regulated files unless the user has explicitly approved the transfer. <br>
Risk: Broad directory scans, automatic compression, previews, or unsupervised batch sends increase the chance of accidental disclosure. <br>
Mitigation: Keep sends tightly user-directed and avoid broad scans or automated batch behavior without review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gongjieliu/feishu-send-file-directly) <br>
- [OpenClaw message tool documentation](https://docs.openclaw.ai/tools/message) <br>
- [OpenClaw file write tool documentation](https://docs.openclaw.ai/tools/write) <br>
- [OpenClaw workspace management](https://docs.openclaw.ai/guides/workspace) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration instructions] <br>
**Output Format:** [Markdown with JavaScript-style tool-call examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces file-sending workflow guidance; it does not generate file content unless paired with the agent's write tool.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
