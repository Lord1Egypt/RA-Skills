## Description: <br>
Sends local image, voice, video, and file media to DingTalk users or groups through the bundled Python script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shyzhen](https://clawhub.ai/user/shyzhen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers use this skill when a user explicitly asks to send a known local file, screenshot, recording, video, or attachment to a DingTalk user or group. It helps an agent select the account, media type, and recipient target before running the send command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads the selected local file to DingTalk, which can expose sensitive content if the wrong file is chosen. <br>
Mitigation: Confirm the exact local file path and whether the file contains sensitive information before running the send command. <br>
Risk: A mistyped user ID, group ID, or target type can send media to the wrong DingTalk recipient. <br>
Mitigation: Verify the recipient user or group ID and use --group or --user when automatic target detection is ambiguous. <br>
Risk: Multiple DingTalk accounts or missing credentials can cause the command to fail or use an unintended account. <br>
Mitigation: Confirm the DingTalk account when more than one account is configured, and check the required DingTalk credential variables or OpenClaw configuration before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shyzhen/dingtalk-send-media) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [DingTalk Open Platform](https://open.dingtalk.com/) <br>
- [DingTalk connector issue 456](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/issues/456) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; the script returns JSON status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python or python3 and DingTalk credentials from environment variables or OpenClaw configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
