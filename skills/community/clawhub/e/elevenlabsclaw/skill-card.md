## Description: <br>
Converts text to natural speech using ElevenLabs for clinical and healthcare use cases, including patient instructions, discharge summaries, medication reminders, multilingual health messages, and accessible voice content for the OpenClaw Clinical Hackathon. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arunnadarasa](https://clawhub.ai/user/arunnadarasa) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and clinical hackathon participants use this skill to help OpenClaw agents generate patient-facing speech, reminders, multilingual health messages, and accessible audio content through ElevenLabs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text sent to ElevenLabs may contain patient identifiers or regulated clinical content. <br>
Mitigation: Use only in environments where ElevenLabs use is approved, avoid PHI unless compliance controls are in place, and keep sensitive data out of logs and prompts unless explicitly allowed. <br>
Risk: The skill depends on an ElevenLabs API key for external audio generation. <br>
Mitigation: Store the API key securely, load it from the environment or an approved secret store, and rotate or revoke it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/arunnadarasa/elevenlabsclaw) <br>
- [ElevenLabs Text-to-Speech API](https://elevenlabs.io/docs/api-reference/text-to-speech) <br>
- [ElevenLabs Music API](https://elevenlabs.io/docs/capabilities/music) <br>
- [ElevenLabs Healthcare Use Cases](https://elevenlabs.io/use-cases/healthcare) <br>
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/skills) <br>
- [ClawHub CLI Documentation](https://docs.openclaw.ai/tools/clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, API Calls] <br>
**Output Format:** [Markdown instructions with inline shell, JSON, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ELEVENLABS_API_KEY; agents may use an existing TTS tool or call the ElevenLabs API directly when approved.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
