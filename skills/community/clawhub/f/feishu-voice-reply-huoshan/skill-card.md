## Description: <br>
Feishu Voice Reply generates voice audio with Volcengine TTS, converts it to Opus, and sends it through the Feishu API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaqzsd](https://clawhub.ai/user/kaqzsd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Feishu workspace operators use this skill to turn supplied text into voice messages and send them to a specified Feishu user. It supports command-line use, configurable voices, and environment-based credentials for Volcengine and Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Typed message text is sent to Volcengine for TTS processing, and generated audio is uploaded to Feishu. <br>
Mitigation: Avoid secrets or regulated data in messages unless the connected services and workspace policies permit that data sharing. <br>
Risk: The skill requires Feishu and Volcengine credentials with permissions to create audio and send messages. <br>
Mitigation: Use dedicated least-privilege credentials, remove unused Feishu permissions where possible, and rotate credentials if they are exposed. <br>
Risk: A misconfigured recipient can send generated voice messages to the wrong Feishu user. <br>
Mitigation: Verify the recipient Open ID or default recipient environment variable before running the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaqzsd/feishu-voice-reply-huoshan) <br>
- [Volcengine TTS documentation](https://www.volcengine.com/docs/6561/195562) <br>
- [Volcengine voice list](https://www.volcengine.com/docs/6561/1257544?lang=zh) <br>
- [Feishu Open Platform](https://open.feishu.cn/document/home) <br>
- [Feishu message types](https://open.feishu.cn/document/ukTMukTMukTM/uEjNwUjLxYDM14SM2ATN) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown documentation with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an Opus audio file transiently during execution, uploads it to Feishu, and sends an audio message to the configured recipient.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
