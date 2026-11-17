## Description:

Generate Cantonese TTS audio in OGG/Opus format using Microsoft Edge TTS for WhatsApp and Telegram voice replies with adjustable tone styles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skglau](https://clawhub.ai/user/skglau)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate Cantonese voice-note audio for WhatsApp or Telegram replies from text prompts. It supports neutral, slow, fast, and angry tone styles through preconfigured Edge TTS voice parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on local scripts that are referenced but not included in the artifact.

Mitigation: Inspect and trust the local scripts before running the skill, and deploy only scripts that match the expected Edge TTS and messaging behavior.

Risk: The Telegram example includes a real-looking chat ID, which could route generated audio to an unintended recipient.

Mitigation: Replace example recipient identifiers with the intended chat ID before sending any voice message.

Risk: Input text may be transmitted to Edge TTS or Telegram as part of the voice generation and delivery workflow.

Mitigation: Avoid sending sensitive, regulated, or confidential text through this workflow unless the services and routing are approved for that data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/skglau/skills/edge-tts-cantonese)
- [Publisher Profile](https://clawhub.ai/user/skglau)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces OGG/Opus audio paths or send-command examples for messaging workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
