## Description: <br>
Guides agents in sending Feishu text, image, and file messages through OpenClaw, including recipient targeting and relative media paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanl754](https://clawhub.ai/user/hanl754) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send Feishu notifications, screenshots, logs, and documents from an OpenClaw environment. It is suited for human-approved messaging workflows where an agent prepares or runs openclaw message send commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages or attached files may disclose secrets, personal data, logs, screenshots, or other confidential material to a Feishu recipient. <br>
Mitigation: Verify the target user or chat before sending, redact sensitive content, and send only material approved for that Feishu destination. <br>
Risk: Media and file examples depend on relative paths, so incorrect path handling may send the wrong file or cause delivery failures. <br>
Mitigation: Place intended files in the OpenClaw workspace, use relative ./ paths, and inspect the selected file before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanl754/feishu-messenger) <br>
- [Feishu Open Platform](https://open.feishu.cn/) <br>
- [OpenClaw message documentation](https://docs.openclaw.ai/tools/message) <br>
- [Feishu message API](https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2ATN) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require a Feishu target ID and may include a relative media path; media examples assume files are placed in the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
