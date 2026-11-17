## Description:

Free, unlimited text-to-speech using Microsoft Edge neural voices via Python edge-tts for long-form audio, podcasts, voice notes, spoken briefs, and headless or server-side TTS without API keys, credits, or character limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dannyshmueli](https://clawhub.ai/user/dannyshmueli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content creators, and operators use this skill to generate long-form MP3 speech from text or files with selectable Microsoft Edge neural voices and simple presets. It is useful when cost and length matter more than voice cloning, real-time streaming, or premium voice acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can automatically run an unpinned external Python package and may install it into the active environment.

Mitigation: Review the skill before installing, run it in an isolated environment, and prefer a reviewed, pinned edge-tts version.

Risk: Text submitted for synthesis may be sent to the Edge TTS service.

Mitigation: Use the skill only for text that is appropriate to send to that service, and avoid sensitive or confidential input unless that use is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dannyshmueli/skills/edge-tts-unlimited)

## Skill Output:

**Output Type(s):** [Shell commands, Files]

**Output Format:** [Shell command output and MP3 audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can list available voices and writes generated audio to the requested output path.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata, released 2026-03-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
