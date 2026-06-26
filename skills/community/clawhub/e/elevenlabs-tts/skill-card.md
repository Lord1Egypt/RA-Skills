## Description: <br>
ElevenLabs TTS helps OpenClaw agents generate expressive ElevenLabs text-to-speech audio with emotional audio tags, multilingual voice synthesis, WhatsApp voice-message workflows, and ffmpeg-based audio conversion guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaharsha](https://clawhub.ai/user/shaharsha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure ElevenLabs voice synthesis, prepare emotionally tagged TTS prompts, convert generated audio for WhatsApp compatibility, and send voice messages with the expected workspace-file handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to an ElevenLabs API key and sends TTS text to ElevenLabs. <br>
Mitigation: Use a scoped ElevenLabs key where possible, keep it out of prompts and logs, and only submit text that is appropriate for processing by ElevenLabs. <br>
Risk: Generated audio may be sent through WhatsApp to an unintended recipient or with unintended message content. <br>
Mitigation: Confirm the recipient, message body, and selected audio file before sending. <br>
Risk: Shell commands are used for audio conversion, file copying, and cleanup. <br>
Mitigation: Use ffmpeg from a trusted source and keep copy or cleanup commands scoped to the current generated temporary audio file. <br>


## Reference(s): <br>
- [Audio Tags Reference](references/audio-tags.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/shaharsha/elevenlabs-tts) <br>
- [ClawHub Metadata Source](https://clawhub.com/skills/elevenlabs-tts) <br>
- [ElevenLabs](https://elevenlabs.io) <br>
- [ElevenLabs Voice Library](https://elevenlabs.io/voice-library) <br>
- [ElevenLabs Voices API](https://api.elevenlabs.io/v1/voices) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, tool calls] <br>
**Output Format:** [Markdown guidance with inline tool-call examples, JSON configuration, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ELEVENLABS_API_KEY, requires ffmpeg, and guides agents to handle generated audio as temporary files before optional WhatsApp sending.] <br>

## Skill Version(s): <br>
2.4.0 (source: server release metadata; artifact metadata reports 2.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
