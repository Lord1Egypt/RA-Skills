## Description: <br>
Voice-to-voice AI assistant using Gemini Live API for natural spoken conversations with Google's Gemini models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AliMostafaRadwan](https://clawhub.ai/user/AliMostafaRadwan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to send text or voice prompts to Google's Gemini models and receive spoken responses for natural AI conversations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Typed or spoken conversation content can be sent to Google Gemini for processing. <br>
Mitigation: Install only when users are comfortable providing a Gemini API key and having conversation content processed by Google Gemini. <br>
Risk: Broad WhatsApp text triggers may invoke the assistant in chats that contain private or sensitive information. <br>
Mitigation: Narrow the configured triggers or require explicit opt-in before use in sensitive chats. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AliMostafaRadwan/gemini-voice-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, audio, JSON] <br>
**Output Format:** [JSON response containing a message field with an audio media path when voice output is available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY and may write temporary OGG audio output under /tmp.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
