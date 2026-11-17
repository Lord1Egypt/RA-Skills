## Description:

Combined agent that synthesizes speech via Volcengine TTS, uploads the audio to TOS, and returns a presigned temporary URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[day253](https://clawhub.ai/user/day253)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to turn text into speech, upload the resulting audio to Volcengine TOS, and return a shareable temporary URL for downstream workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input text is sent to Volcengine services for synthesis.

Mitigation: Avoid sensitive text unless the user accepts that external processing path.

Risk: Cloud credentials can grant broader object storage access than the workflow needs.

Mitigation: Use Volcengine credentials scoped to the required TOS bucket and prefix.

Risk: Presigned URLs can expose uploaded audio while they remain valid.

Mitigation: Keep URL expirations short and share generated links only with intended recipients.

Risk: Runtime dependencies are installed from package indexes.

Mitigation: Install in an isolated environment and pin dependency versions where possible.

## Reference(s):

- [Volcengine TTS documentation](https://www.volcengine.com/docs/6561/196768)
- [Volcengine TTS source skill reference](skills/ai/audio/volcengine-ai-audio-tts/SKILL.md)
- [Volcengine TOS source skill reference](skills/storage/tos/volcengine-storage-tos/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [Console text with optional JSON result and generated audio object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns text, voice type, duration, TOS bucket and key, presigned URL, expiration, audio size, and optional local file path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
