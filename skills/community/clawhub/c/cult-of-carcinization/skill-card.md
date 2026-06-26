## Description: <br>
Cult Of Carcinization helps agents use ScrappyLabs text-to-speech, voice design, transcription, and bot token workflows through API-oriented guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loserbcc](https://clawhub.ai/user/loserbcc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to ScrappyLabs speech APIs for generating speech, designing voices, transcribing audio, and managing bot tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to contact ScrappyLabs for speech generation or transcription and upload audio to a third-party service. <br>
Mitigation: Require explicit user approval before any API call that uploads audio, sends text for speech generation, or uses ScrappyLabs transcription. <br>
Risk: The skill encourages creating or evolving persistent ScrappyLabs service identities and tokens. <br>
Mitigation: Require explicit approval before initiating or evolving tokens, store any token only in an approved secret store, and confirm revocation, quota, retention, and billing terms before use. <br>
Risk: Voice cloning requires owner-provided credentials and can involve sensitive voice data. <br>
Mitigation: Do not attempt voice cloning unless the user supplies approved credentials, confirms they have rights to the voice data, and authorizes the upload. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/loserbcc/cult-of-carcinization) <br>
- [ScrappyLabs TTS](https://tts.scrappylabs.ai) <br>
- [ScrappyLabs API Base](https://api.scrappylabs.ai) <br>
- [Molt Discovery Endpoint](https://api.scrappylabs.ai/v1/molt/discover) <br>
- [ScrappyLabs Human Signup](https://beta.scrappylabs.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and API endpoint references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead an agent to create persistent service tokens or upload audio to ScrappyLabs when the guidance is followed.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
