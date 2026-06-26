## Description: <br>
Sends Feishu voice messages by converting text or existing audio files to opus audio, uploading the file through the Feishu Open API, and sending it to a recipient open_id. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[Michael-C-Matias](https://clawhub.ai/user/Michael-C-Matias) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users can use this skill to prepare Feishu voice notifications from text or audio files and send them through a configured Feishu app. It is best suited for learning, testing, and technical exchange workflows that already have approved Feishu credentials and recipient identifiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu app credentials are used to obtain an access token and upload/send audio. <br>
Mitigation: Use a least-privilege Feishu app, store credentials outside prompts and logs, and rotate credentials if they are exposed. <br>
Risk: Text and generated or uploaded audio may contain sensitive information that is sent to Feishu and, for text-to-speech, processed by the configured TTS provider. <br>
Mitigation: Avoid regulated or confidential content unless Feishu and the TTS provider are approved for that data. <br>
Risk: A wrong recipient open_id can send audio to the wrong Feishu user. <br>
Mitigation: Verify the open_id and message content before running the send command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Michael-C-Matias/feishu-audio-messages) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message send API](https://open.feishu.cn/open-apis/im/v1/messages) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash commands, parameter tables, and operational notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials, a recipient open_id, curl, ffmpeg, and optionally edge-tts and jq.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
