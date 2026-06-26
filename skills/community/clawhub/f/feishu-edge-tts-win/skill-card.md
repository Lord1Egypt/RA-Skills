## Description: <br>
Sends Feishu voice messages on Windows by generating speech with Microsoft Edge TTS and delivering it as Feishu audio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ztxdcyy](https://clawhub.ai/user/ztxdcyy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill on Windows to convert provided text into the zh-CN-XiaoxiaoNeural voice and send it to a Feishu user as an audio message. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Message text and generated audio may leave the user's machine for Edge TTS and Feishu processing. <br>
Mitigation: Avoid sending secrets, regulated data, or other sensitive content through this workflow. <br>
Risk: The skill uses Feishu app credentials and sends audio to a supplied recipient open_id. <br>
Mitigation: Protect the OpenClaw configuration file, use least-privilege Feishu app credentials, and verify the recipient open_id before running the command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ztxdcyy/feishu-edge-tts-win) <br>
- [Feishu Open API](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command guidance for generating audio and sending a Feishu voice message; runtime success depends on Edge TTS, ffmpeg, Feishu credentials, and a valid recipient open_id.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
