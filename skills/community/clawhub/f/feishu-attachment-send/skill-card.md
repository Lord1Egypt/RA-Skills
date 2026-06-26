## Description: <br>
Guides agents through reliable Feishu attachment delivery by sending text and files separately and checking mediaLocalRoots path constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yujunyanyanya](https://clawhub.ai/user/yujunyanyanya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent operators, and Feishu-facing assistants use this skill to deliver generated or edited files in Feishu DMs or groups and to troubleshoot missing attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A file could be sent to the wrong recipient, channel, or group. <br>
Mitigation: Confirm the exact recipient and channel before sending any attachment. <br>
Risk: Attachments may fail or expose unintended local paths if mediaLocalRoots is too broad or the file is outside an allowed directory. <br>
Mitigation: Keep mediaLocalRoots limited to intended workspace directories and place outgoing files under an allowed workspace path before sending. <br>
Risk: Combining explanatory text and an attachment in one Feishu message can make the attachment unreliable for the recipient. <br>
Mitigation: Send a short text message first when needed, then send the attachment as a separate file-only message. <br>


## Reference(s): <br>
- [Feishu file sending notes](references/feishu-file-sending-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions] <br>
**Output Format:** [Markdown guidance with workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include Feishu message sequencing, file path checks, and mediaLocalRoots troubleshooting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
