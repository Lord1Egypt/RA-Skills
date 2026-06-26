## Description: <br>
A Feishu voice companion skill that helps an agent configure a role-play persona, transcribe user audio with SenseAudio ASR, generate persona-aligned replies, and send SenseAudio TTS output as native Feishu OPUS voice messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KLilyZ](https://clawhub.ai/user/KLilyZ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Feishu bot operators use this skill to run a customizable persona-based voice assistant in Feishu private chats. It supports first-use persona setup, voice transcription, persona prompt generation, speech synthesis, OPUS conversion, and Feishu voice-message delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private Feishu chat content and voice audio may be processed by external services. <br>
Mitigation: Use a dedicated low-permission Feishu bot, restrict it to intended chats, and inform users that SenseAudio and Feishu may process audio and generated replies. <br>
Risk: The scripts can install the Python requests package at runtime. <br>
Mitigation: Preinstall and pin required dependencies in a controlled environment before deployment instead of relying on runtime package installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KLilyZ/feishu-senseaudio-persona) <br>
- [OpenClaw homepage metadata](https://clawhub.ai/Anightmare2/feishu-voice-skill) <br>
- [SenseAudio API base](https://api.senseaudio.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line oriented text for agent workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persona prompts and workflow commands; successful Feishu replies are intended to appear as voice messages rather than chat text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
