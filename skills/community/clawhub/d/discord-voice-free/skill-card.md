## Description: <br>
Provides a basic Discord voice assistant workflow for joining and leaving voice channels, checking connection status, transcribing speech with local Whisper, and playing responses with OpenAI TTS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users can use this skill to prototype a basic Discord voice question-answering loop with local speech-to-text, agent processing, text-to-speech playback, and simple voice connection management. It is not intended for low-latency live captioning or enterprise multi-user moderation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Discord voice-channel speech may be captured, transcribed locally, processed by the agent, and spoken back through OpenAI TTS. <br>
Mitigation: Install the skill only in voice channels where participants understand the audio processing flow, avoid sensitive conversations, and remove the bot when it is not in use. <br>
Risk: The skill requires Discord and OpenAI credentials for voice-channel access and TTS playback. <br>
Mitigation: Use a dedicated Discord bot token and OpenAI API key, store credentials outside version control, and rotate them if exposed. <br>
Risk: The free version does not provide an allowed-users whitelist, so any user in the connected channel may trigger the voice loop. <br>
Mitigation: Use the bot only in controlled servers and channels, grant the minimum Discord permissions needed, and disconnect it after testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/discord-voice-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, CLI commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Discord join, leave, and status guidance plus a basic local Whisper and OpenAI TTS voice assistant workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
