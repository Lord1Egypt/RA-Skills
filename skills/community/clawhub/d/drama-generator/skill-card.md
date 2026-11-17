## Description:

Automated drama video generator - from script to multi-character drama videos with OpenAI TTS, Whisper, and Remotion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, educators, marketers, and developers use this skill to turn formatted drama scripts into multi-character short-form videos with voice synthesis, timed dialogue, scene transitions, and rendered MP4 output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to install mutable external code globally through npm or from GitHub.

Mitigation: Prefer a pinned package version or verified commit, install in a limited workspace, and review the package before running it.

Risk: Drama scripts and generated audio may be sent to cloud TTS or transcription providers.

Mitigation: Use narrowly scoped provider credentials and avoid confidential or regulated scripts unless the selected provider is approved for that data.

## Reference(s):

- [OpenClaw Drama Generator homepage](https://github.com/ZhenRobotics/openclaw-drama-generator)
- [OpenClaw Drama Generator documentation](https://github.com/ZhenRobotics/openclaw-drama-generator#readme)
- [openclaw-drama-generator npm package](https://www.npmjs.com/package/openclaw-drama-generator)
- [Drama Generator on ClawHub](https://clawhub.ai/zhenstaff/skills/drama-generator)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files, Code]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The described workflow may produce script text files, parsed JSON, synthesized audio, timestamp data, Remotion scene data, and vertical MP4 video output.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact documentation and release changelog mention 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
