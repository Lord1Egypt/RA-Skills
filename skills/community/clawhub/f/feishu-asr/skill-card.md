## Description: <br>
Transcribes Feishu voice messages into text using Whisper or configured ASR services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Richardcoder849](https://clawhub.ai/user/Richardcoder849) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Teams using Feishu can have an agent retrieve voice-message audio, convert it, and return transcription text for follow-up or accessibility. Operators should review message-read permissions and ASR provider choices before workplace use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports a mismatch between offline/no-network claims and behavior that can involve remote model downloads or cloud ASR setup. <br>
Mitigation: Confirm where audio is processed before use, pin trusted model sources, and disable remote downloads or cloud ASR paths unless explicitly approved. <br>
Risk: The skill may access sensitive Feishu voice messages through message-read permissions. <br>
Mitigation: Grant only the narrow Feishu permissions required for the deployment, limit use to approved chats or workspaces, and avoid processing sensitive workplace audio without authorization. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Richardcoder849/feishu-asr) <br>
- [Hugging Face mirror endpoint](https://hf-mirror.com) <br>
- [Alibaba Cloud ASR console](https://d.console.aliyun.com) <br>
- [Tencent Cloud ASR](https://cloud.tencent.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcription with Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Feishu message-read credentials, audio conversion dependencies, model downloads, or cloud ASR credentials depending on the configured path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
