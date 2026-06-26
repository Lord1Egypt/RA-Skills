## Description: <br>
Send customized voice messages to Feishu chats by generating and uploading TTS audio with configurable credentials and voice options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jisuwudou](https://clawhub.ai/user/jisuwudou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to create Feishu voice-message scripts, configure Feishu app credentials and chat targets, generate TTS audio, and send the resulting audio to Feishu chats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu app credentials, message content, generated audio, and recipient identifiers are sent to Feishu and may be present in local configuration. <br>
Mitigation: Use a least-privilege Feishu app, protect the config file containing the app secret, and only send content acceptable for Feishu processing. <br>
Risk: A wrong chat ID can send generated voice messages to an unintended Feishu chat. <br>
Mitigation: Verify the chat ID with a low-risk test message before regular use. <br>
Risk: The Edge TTS variant may install the `edge-tts` Python package at runtime. <br>
Mitigation: Manually install or pin `edge-tts` in a controlled environment before running the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jisuwudou/free-feishu-voice) <br>
- [Feishu OpenAPI](https://open.feishu.cn/open-apis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown containing JSON configuration examples, Bash scripts, shell commands, and usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Feishu credential placeholders, environment variable overrides, dependency checks, and status or error messages for troubleshooting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
