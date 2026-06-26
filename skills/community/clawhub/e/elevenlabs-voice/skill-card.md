## Description: <br>
Text-to-Speech and Speech-to-Text using ElevenLabs AI for converting text to speech, transcribing voice messages, and working with voice across multiple languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amreahmed](https://clawhub.ai/user/amreahmed) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to add ElevenLabs text-to-speech, speech-to-text, voice listing, and voice message workflows to assistants or messaging integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text and audio selected by the user are sent to ElevenLabs for cloud processing. <br>
Mitigation: Use the skill only for content approved for ElevenLabs processing, and avoid confidential, regulated, or highly personal voice or text content unless that use is approved. <br>
Risk: Shared or long-lived ElevenLabs API keys can expose account access if stored carelessly. <br>
Mitigation: Use a dedicated ElevenLabs API key and keep it out of shared .env files and public artifacts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/amreahmed/elevenlabs-voice) <br>
- [ElevenLabs pricing](https://elevenlabs.io/pricing) <br>
- [ElevenLabs API endpoint](https://api.elevenlabs.io/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, API Calls, Guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, JSON status objects, and generated or transcribed audio/text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ELEVENLABS_API_KEY and sends selected text or audio to ElevenLabs for processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
