## Description:

Analyze audio quality, detect noise types, and provide improvement recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scikkk](https://clawhub.ai/user/scikkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and audio workflow operators use this skill to check recordings for noise and quality issues, produce quality reports, and generate improvement recommendations or pass/fail quality gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected audio files may contain private conversations, customer data, regulated information, or voice biometrics and are uploaded to SenseAudio for analysis.

Mitigation: Use the skill only on files intentionally selected for upload, obtain appropriate consent, and confirm SenseAudio retention and privacy terms before processing sensitive recordings.

Risk: Microphone-recording workflows can capture audio without a clear per-upload consent step if extended from the provided examples.

Mitigation: Add explicit permission prompts, recording duration limits, and user review before sending captured audio to the analysis API.

## Reference(s):

- [SenseAudio homepage](https://senseaudio.cn)
- [SenseAudio speech recognition API docs](https://senseaudio.cn/docs/speech_recognition)
- [ClawHub skill page](https://clawhub.ai/scikkk/skills/audio-quality-checker)
- [Publisher profile](https://clawhub.ai/user/scikkk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples, plus JSON-shaped analysis reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SENSEAUDIO_API_KEY and sends selected audio files to the SenseAudio API for analysis.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
