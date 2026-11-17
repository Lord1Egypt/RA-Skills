## Description:

Captures browser games frame by frame and assembles the footage into a beat-synced trailer MP4.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vargai](https://clawhub.ai/user/vargai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to turn a browser game or three.js/WebGL scene into a polished gameplay trailer. It captures deterministic frames, adds a soundtrack and titles, and produces a checked MP4.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious for reported risky file handling and a path validation flaw; six files were only partially inspected.

Mitigation: Review and correct the reported issues before installing. If proceeding, use a disposable environment with no important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vargai/skills/code-game-trailer)
- [Director format](artifact/references/director-format.md)
- [Virtual clock guide](artifact/references/virtual-clock.md)
- [Sound and cut guide](artifact/references/sound-and-cut.md)
- [Example trailer](https://s3.varg.ai/files/4325c578-378d-4c43-ae53-3cc3218df1ea/file_b715771f882f.mp4)

## Skill Output:

**Output Type(s):** [Video, Audio, Images, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [MP4 trailer, WAV audio tracks, captured image frames, JSON manifests and cut data, plus commands and director configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video dimensions and frame rate are set in the director configuration; the example outputs a 1920×1080 MP4.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
