## Description: <br>
Guides agents through configuring an OpenClaw DingTalk enterprise bot channel, including plugin installation, channel configuration, verification, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaoyunhao0107](https://clawhub.ai/user/shaoyunhao0107) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect OpenClaw to DingTalk enterprise internal bots, configure Stream mode, and troubleshoot channel installation or message-response failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup guide contains DingTalk Client Secret/AppSecret values and configuration examples that users may accidentally expose in shared files, logs, or screenshots. <br>
Mitigation: Use placeholders in shared examples, keep OpenClaw configuration files private, avoid sharing logs or screenshots containing secrets, and rotate any real secret that was exposed. <br>
Risk: Open DM or group chat settings can broaden who can interact with the DingTalk bot. <br>
Mitigation: Prefer allowlists for DM and group access when deploying beyond a controlled test environment. <br>
Risk: Installing the wrong plugin package could configure an unintended DingTalk integration. <br>
Mitigation: Verify that @soimy/dingtalk is the intended plugin before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shaoyunhao0107/dingtalk-setup) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [DingTalk Open Platform](https://open.dingtalk.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps, troubleshooting checks, and credential-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
