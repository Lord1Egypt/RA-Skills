## Description: <br>
Guides agents through ElevenLabs text-to-speech workflows, including voice selection, SSML, batch audio generation, voice cloning, Telegram voice-note delivery, and API error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[producedbysavant](https://clawhub.ai/user/producedbysavant) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation builders use this skill to generate speech with the ElevenLabs API, manage voices, create batch audio assets, and connect synthesized speech to Telegram bot workflows. It also provides guidance for multilingual synthesis, voice cloning requests, audio concatenation, retry handling, and quality tuning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice cloning can misuse a person's voice or process sensitive biometric audio without enough consent guardrails. <br>
Mitigation: Use cloning only for your own voice or speakers who have given explicit informed permission, and keep consent records for professional cloning workflows. <br>
Risk: ElevenLabs and Telegram workflows can expose API credentials, message content, or regulated personal data. <br>
Mitigation: Store credentials in environment variables or a secrets manager, avoid submitting secrets or regulated personal data, and review generated Telegram delivery flows before use. <br>


## Reference(s): <br>
- [ElevenLabs API Documentation](https://docs.elevenlabs.io/) <br>
- [ClawHub release page](https://clawhub.ai/producedbysavant/elevenlabs-voice-pipeline) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce audio files through external ElevenLabs and Telegram API workflows when executed with user-provided credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
