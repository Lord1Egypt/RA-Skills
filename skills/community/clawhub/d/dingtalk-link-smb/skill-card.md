## Description: <br>
DingTalk bot connection configuration guide for installing, configuring, and troubleshooting the OpenClaw DingTalk connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chao980](https://clawhub.ai/user/chao980) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect OpenClaw to DingTalk bots, configure AppKey/AppSecret credentials, validate gateway status, and troubleshoot message delivery issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup guide instructs users to install and trust an external DingTalk connector package. <br>
Mitigation: Confirm the connector package and repository are trusted before installation. <br>
Risk: The configuration flow handles AppSecret and API credentials that could be exposed through committed config files, logs, or screenshots. <br>
Mitigation: Keep ~/.openclaw/openclaw.json private, avoid sharing logs or screenshots containing secrets, restrict local file access where possible, and rotate credentials after any suspected exposure. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chao980/dingtalk-link-smb) <br>
- [DingTalk OpenClaw connector documentation](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector) <br>
- [DingTalk Open Platform](https://open-dev.dingtalk.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
