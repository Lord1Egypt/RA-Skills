## Description:

General-purpose AI assistant using Gemini API with voice and text support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alimostafaradwan](https://clawhub.ai/user/alimostafaradwan)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to send text or voice prompts to Google's Gemini models and receive conversational responses, including voice output when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text and voice content may be sent to Google Gemini without enough user scoping or consent.

Mitigation: Use only where users knowingly opt in to external Gemini processing for text and voice content.

Risk: Broad WhatsApp routing could process unrelated text or audio messages.

Mitigation: Constrain routing and require confirmation before connecting the skill to broad WhatsApp text or audio flows.

Risk: Caller-supplied audio_path or system_instruction values can expose local files or alter assistant behavior if accepted from untrusted callers.

Mitigation: Accept audio paths only from trusted upload storage, restrict caller control over system instructions, and use safer temporary output handling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alimostafaradwan/skills/gemini-assistant)

## Skill Output:

**Output Type(s):** [text, audio, guidance]

**Output Format:** [JSON response with optional audio media path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GEMINI_API_KEY; may produce temporary OGG voice output.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
