## Description: <br>
飞书TTS Pro converts Chinese text to speech with Edge-TTS, transcodes it with FFmpeg, uploads it to Feishu, and sends it as an audio message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minybear](https://clawhub.ai/user/minybear) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs to reply by voice or send TTS narration through Feishu. It generates speech from supplied text, converts the audio to Feishu-compatible opus format, and sends it to a configured recipient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Feishu app credentials and can send generated voice messages. <br>
Mitigation: Use least-privileged Feishu app permissions, protect FEISHU_APP_SECRET, and install only in environments where outbound Feishu messaging is approved. <br>
Risk: A misconfigured default recipient can send audio messages to the wrong Feishu user. <br>
Mitigation: Set FEISHU_DEFAULT_USER carefully, pass an explicit recipient when needed, and test with non-sensitive text before routine use. <br>
Risk: Text supplied to the TTS workflow may be processed by external services and sent through Feishu. <br>
Mitigation: Avoid sending secrets, regulated data, or sensitive personal information unless the organization permits this workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/minybear/feishu-tts-pro) <br>
- [Publisher profile](https://clawhub.ai/user/minybear) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Audio files, Status text] <br>
**Output Format:** [Command-line text output with generated audio uploaded through Feishu APIs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials, a recipient open_id, Python with edge-tts, and FFmpeg.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
