## Description: <br>
Axiomata Voice converts text messages to speech audio using the ElevenLabs text-to-speech API and documents optional Telegram voice delivery for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to turn text into speech audio for long messages, voice messaging, and accessibility workflows. It is intended for OpenClaw agents configured with ElevenLabs credentials and, when delivery is needed, Telegram bot credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for speech synthesis may be sent to ElevenLabs and, if delivery is used, Telegram. <br>
Mitigation: Use revocable service credentials, prefer a dedicated Telegram bot, and avoid sending secrets or regulated personal data as text-to-speech input. <br>
Risk: The artifact documents Telegram delivery, but the release evidence says the Telegram delivery script is missing. <br>
Mitigation: Verify or add the Telegram delivery script before relying on Telegram voice-message delivery. <br>


## Reference(s): <br>
- [Axiomata Voice ClawHub page](https://clawhub.ai/kofna3369/axiomata-voice) <br>
- [Publisher profile](https://clawhub.ai/user/kofna3369) <br>
- [ElevenLabs text-to-speech API endpoint](https://api.elevenlabs.io/v1/text-to-speech/<voice_id>) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or reference audio files when the user runs the included text-to-speech command with valid service credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
