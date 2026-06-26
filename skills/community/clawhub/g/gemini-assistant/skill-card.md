## Description: <br>
General-purpose AI assistant using Gemini API with voice and text support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AliMostafaRadwan](https://clawhub.ai/user/AliMostafaRadwan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to ask general questions, have short conversations, and process text or voice prompts through Google's Gemini API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad WhatsApp text, voice, and audio triggers may activate the skill on ordinary chat messages. <br>
Mitigation: Narrow the configured triggers before using the skill in chats where accidental activation matters. <br>
Risk: Text and audio handled by the skill are sent to Google's Gemini API under the user's API key. <br>
Mitigation: Use a dedicated Gemini API key, monitor billing or quota, and avoid sensitive or regulated data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AliMostafaRadwan/gemini-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON response containing message text and optional generated voice media path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce OGG Opus voice output in /tmp when audio response data is returned.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
