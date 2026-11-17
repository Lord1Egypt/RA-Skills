## Description:

Generates text-to-speech audio with `uvx edge-tts`, including voice selection, speech rate, volume, pitch, and subtitle options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[al-one](https://clawhub.ai/user/al-one)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill when they need generated speech audio for accessibility, multitasking, or voice-output workflows, with controls for voice, speed, pitch, volume, and subtitles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User text or filenames interpolated into shell command strings could lead to unsafe shell execution.

Mitigation: Run `edge-tts` with a safe process API using separate arguments, sanitize filenames, and avoid constructing shell strings from user input.

Risk: Using `uvx edge-tts` without a pinned reviewed version can execute mutable third-party code.

Mitigation: Pin and review the `edge-tts` version before installation or execution.

Risk: Text sent to the speech service may contain sensitive information.

Mitigation: Use the skill only with non-sensitive text, as directed by the security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/al-one/skills/edge-tts-uvx)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands generate audio media files and may optionally emit subtitles.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
