## Description:

Guides agents through turning existing screen recordings or product demo videos into Remotion promotional videos with storyboard, edit-spec, subtitle, voiceover, BGM, and render steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[16miku](https://clawhub.ai/user/16miku)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, video producers, and agent users can use this skill to plan and implement promotional edits from existing recordings or demo footage. It helps structure the workflow before Remotion coding, including source clip selection, storyboard and edit-spec files, subtitle and voiceover alignment, BGM, and final rendering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable package and skill install commands can change what code or guidance is pulled into the environment.

Mitigation: Review commands before execution, prefer pinned package versions, and avoid --force unless necessary.

Risk: Cloud transcription and TTS workflows may expose recordings, transcripts, or narration content to external services.

Mitigation: Use cloud transcription or TTS only for material approved for that handling, and choose local alternatives when privacy requirements demand it.

Risk: Third-party companion skills may add behavior outside this skill's reviewed workflow.

Mitigation: Inspect and approve third-party skills before installing them globally or using them in a production workflow.

## Reference(s):

- [ClawHub auto-remotion Skill](https://clawhub.ai/16miku/auto-remotion)
- [Remotion](https://www.remotion.dev/)
- [Remotion + Claude Code](https://www.remotion.dev/docs/ai/claude-code)
- [Remotion Skills](https://www.remotion.dev/docs/ai/skills)
- [video-use](https://github.com/browser-use/video-use)
- [remotion-video-toolkit](https://clawhub.ai/shreefentsar/remotion-video-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, TypeScript, Python, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce storyboard.json, edit-spec.json, subtitle-track.json, voiceover-script.json, Remotion component code, and rendering commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
