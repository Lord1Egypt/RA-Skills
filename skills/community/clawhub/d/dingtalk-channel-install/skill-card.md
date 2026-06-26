## Description: <br>
Installs and configures the OpenClaw DingTalk channel, including the @soimy/dingtalk plugin, DingTalk Client ID/Secret settings, and robot connection setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[k55k32](https://clawhub.ai/user/k55k32) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to install the DingTalk channel plugin, configure DingTalk credentials and message settings, and connect DingTalk bots to an OpenClaw gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated OpenClaw configuration stores the DingTalk Client Secret. <br>
Mitigation: Protect ~/.openclaw/openclaw.json, avoid committing real credentials, and use only placeholder credentials in shared examples. <br>
Risk: The default DingTalk channel configuration enables broad chat access with open DM/group policies and allowFrom set to all sources. <br>
Mitigation: Restrict allowFrom and chat policies to only trusted DingTalk users or groups before production use. <br>
Risk: The installer can restart the OpenClaw gateway immediately after changing configuration. <br>
Mitigation: Use --skip-restart until the generated configuration has been reviewed and approved. <br>
Risk: The skill installs and enables the third-party @soimy/dingtalk plugin. <br>
Mitigation: Verify the plugin source and version before production deployment. <br>


## Reference(s): <br>
- [DingTalk Open Platform](https://open.dingtalk.com/) <br>
- [OpenClaw DingTalk Channel Documentation](https://github.com/soimy/openclaw-channel-dingtalk) <br>
- [DingTalk Channel Install on ClawHub](https://clawhub.ai/k55k32/dingtalk-channel-install) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown instructions with bash commands, JSON configuration snippets, and a Python installer script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes OpenClaw channel configuration and may restart the OpenClaw gateway unless --skip-restart is used.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
