## Description:

Automatically installs edge-tts and converts input text into Chinese female-voice MP3 audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iiawhite-sir](https://clawhub.ai/user/iiawhite-sir)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users can use this skill to turn supplied text into an MP3 speech file, especially for Chinese narration workflows that use the zh-CN-XiaoxiaoNeural voice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A normal run can make privileged system package changes.

Mitigation: Review before installation and prefer manually installing required dependencies in a controlled environment.

Risk: The skill installs unpinned Python tooling.

Mitigation: Preinstall and manage edge-tts through an approved dependency process where possible.

Risk: The skill writes to a caller-supplied output path.

Mitigation: Restrict output paths to a dedicated audio directory and validate paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iiawhite-sir/skills/edge-tts-auto)
- [Skill documentation](artifact/skill.md)

## Skill Output:

**Output Type(s):** [Files, JSON]

**Output Format:** [MP3 audio file with JSON success status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses caller-provided text and output path; the voice is fixed to zh-CN-XiaoxiaoNeural.]

## Skill Version(s):

1.0.0 (source: skill.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
