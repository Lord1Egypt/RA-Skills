## Description: <br>
Run a Feishu or Lark English game with lightweight group-chat interaction for vocabulary challenges, word guessing, and speaking practice with voice messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hei-MaoM](https://clawhub.ai/user/Hei-MaoM) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Feishu and Lark group-chat users use this skill to run short English learning games with deterministic vocabulary scoring, clue-based guessing, and ASR-assisted speaking feedback. It is intended for lightweight, chat-native learning sessions rather than formal pronunciation assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice messages in speaking mode are sent to an external ASR service. <br>
Mitigation: Tell group participants before using speaking mode and use a dedicated low-privilege SenseAudio API key. <br>
Risk: Changing SENSEAUDIO_BASE_URL could send audio to an untrusted transcription endpoint. <br>
Mitigation: Keep SENSEAUDIO_BASE_URL set to the trusted HTTPS provider unless the deployment owner has approved another endpoint. <br>
Risk: ASR transcripts are not sufficient for precise phoneme-level pronunciation grades or accent judgments. <br>
Mitigation: Limit speaking feedback to what was heard, clarity, practical corrections, and more natural phrasing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Hei-MaoM/english-game) <br>
- [ASR provider notes](references/asr_provider_notes.md) <br>
- [Feishu/Lark integration notes](references/integration_cn.md) <br>
- [Mode design notes](references/modes_cn.md) <br>
- [SenseAudio API base URL](https://api.senseaudio.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Natural-language chat replies with occasional Markdown and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains round state in chat context and avoids exposing raw JSON or debug payloads to Feishu/Lark users.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
