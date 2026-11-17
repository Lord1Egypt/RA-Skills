## Description:

Generates Chinese text-to-speech audio with Microsoft Edge TTS voices, including curated Mandarin, Cantonese, and Taiwan voice options plus speech-rate, pitch, subtitle, and audio-output controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hamlet0168](https://clawhub.ai/user/hamlet0168)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and developers use this skill to convert Chinese text, articles, notifications, and dubbing scripts into speech audio from a command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled helper scripts can rewrite an installed skill and introduce hidden PowerShell playback behavior.

Mitigation: Review the package before installing; remove or ignore patch.py, fix.py, and speak_temp.txt unless explicitly needed, and avoid running those helpers.

Risk: Text submitted for speech synthesis may be sent to the external Edge TTS service.

Mitigation: Do not synthesize secrets, credentials, or sensitive content unless the user accepts that external-service exposure.

Risk: Generated audio may play automatically when pygame is installed.

Mitigation: Run in an environment where automatic playback is acceptable, or review and disable playback behavior before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hamlet0168/skills/edge-tts-zh)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [MP3 or OGG audio files with command-line status text and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May auto-play generated audio when pygame is installed; speech synthesis uses an external Edge TTS service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
