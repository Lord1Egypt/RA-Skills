## Description: <br>
Generate Cantonese TTS audio using Edge TTS for WhatsApp and Telegram voice replies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skglau](https://clawhub.ai/user/skglau) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to produce Cantonese OGG/Opus voice-note audio for WhatsApp or Telegram replies, with tone presets for neutral, slow, fast, and angry delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local script paths and example recipient identifiers may not match the user's environment or intended recipient. <br>
Mitigation: Verify referenced local scripts, replace hard-coded paths and chat IDs, and require confirmation before sending WhatsApp or Telegram voice messages. <br>
Risk: Text submitted for voice generation may be processed by Microsoft Edge TTS and the selected messaging platform. <br>
Mitigation: Avoid sensitive text unless the user accepts processing by Microsoft Edge TTS and the messaging platform. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skglau/edge-tts-cantonese) <br>
- [Publisher profile](https://clawhub.ai/user/skglau) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and parameter examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for generating OGG/Opus audio files; sending through WhatsApp or Telegram depends on local scripts and recipient details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
