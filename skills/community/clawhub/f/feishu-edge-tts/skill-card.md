## Description: <br>
使用微软 Edge TTS（免费）生成语音，发送到飞书。无需 API key，音质优秀，支持多语言多音色。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Anightmare2](https://clawhub.ai/user/Anightmare2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to generate spoken audio from supplied text with Edge TTS, optionally tune voice, speed, and pitch, and send the resulting audio message to a configured Feishu chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provided text is sent to Edge TTS for speech generation. <br>
Mitigation: Install only if you are comfortable sending that text to Edge TTS, and avoid using sensitive text unless approved for the target environment. <br>
Risk: Generated audio is uploaded to Feishu and sent to the configured chat. <br>
Mitigation: Verify FEISHU_CHAT_ID before sending, and use --no-send when only local audio generation is intended. <br>
Risk: FEISHU_APP_SECRET is required for sending messages. <br>
Mitigation: Protect FEISHU_APP_SECRET and use a least-privilege Feishu app. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Anightmare2/feishu-edge-tts) <br>
- [Skill usage guide](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, environment configuration, and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate a local OPUS audio file with --no-send or send the audio to Feishu when credentials and chat ID are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, clawhub.yaml, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
