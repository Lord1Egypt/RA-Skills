## Description:

Voice-to-voice AI assistant using Gemini Live API for spoken AI conversations powered by Google's Gemini models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alimostafaradwan](https://clawhub.ai/user/alimostafaradwan)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to send text or trusted audio input to Google's Gemini service and receive a spoken assistant response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad WhatsApp text and audio triggers may send unintended messages or recordings to Google's Gemini service.

Mitigation: Narrow triggers to explicit commands and use the skill only where users expect selected text or audio to be processed by Gemini.

Risk: The skill can process arbitrary local audio paths supplied to the handler.

Mitigation: Restrict audio_path inputs to trusted uploaded files and reject paths outside the approved upload area.

Risk: Predictable /tmp voice output paths can be unsafe in shared or multi-user environments.

Mitigation: Use unique temporary output paths with appropriate permissions and clean up generated audio files after use.

Risk: Voice recordings may contain sensitive information.

Mitigation: Avoid sensitive recordings and confirm users are comfortable sending selected audio to Google's Gemini service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alimostafaradwan/skills/gemini-voice-assistant)

## Skill Output:

**Output Type(s):** [text, JSON, audio]

**Output Format:** [JSON object with a message string containing a media path to an OGG voice response, or an error message.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GEMINI_API_KEY and may write OGG output files under /tmp.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
