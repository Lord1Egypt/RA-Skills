## Description:

Creates educational videos from a course topic by guiding script writing, TTS voiceover, visual design, Remotion code development, preview review, and final video export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linhongbijkm-dot](https://clawhub.ai/user/linhongbijkm-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and content creators use this skill to produce instructional videos with narration, subtitles, visual scene plans, Remotion project code, preview renders, and final exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on local tools and project dependencies that may be missing or unpinned.

Mitigation: Run the documented environment checks first, stop on missing prerequisites, and consider pinning npm package versions before creating or adding project dependencies.

Risk: The skill relies on a companion remotion-video-toolkit skill for Remotion implementation guidance.

Mitigation: Review and allow the companion skill before using this workflow.

Risk: Default voice and language settings are Chinese unless changed by the user.

Mitigation: Specify the target language and edge-tts voice explicitly when producing non-Chinese content.

## Reference(s):

- [Teaching Styles Reference](references/teaching-styles.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands, SRT subtitles, Remotion source code, audio files, and rendered video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports portrait 1080x1920 and landscape 1920x1080 video workflows; default voice guidance uses zh-CN-XiaoxiaoNeural unless the user chooses another voice.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
