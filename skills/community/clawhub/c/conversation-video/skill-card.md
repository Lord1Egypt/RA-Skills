## Description:

Generate animated conversation videos with multi-voice TTS audio and timed text overlays.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratyushchauhan](https://clawhub.ai/user/pratyushchauhan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to turn dialogue transcripts into synchronized conversation videos with speaker labels, generated voice audio, and either ffmpeg or Remotion rendering paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local Python, ffmpeg, npm, and Remotion code.

Mitigation: Run it in a clean project or sandbox and review generated commands before execution.

Risk: The security summary flags imports from an unrelated local environment and unpinned package execution.

Mitigation: Pin Python and npm dependencies before use and avoid the browser-use virtualenv fallback.

Risk: Transcript and timing manifests influence generated speech, overlays, and renderer command construction.

Mitigation: Render only trusted transcript and timing manifests.

## Reference(s):

- [Conversation Video skill page](https://clawhub.ai/pratyushchauhan/skills/conversation-video)
- [FFmpeg Text Overlay Guide](references/ffmpeg-guide.md)
- [Remotion Patterns Reference](references/remotion-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON manifest examples, shell commands, and generated audio/video file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces transcript timing manifests, WAV audio, and MP4 video outputs when its local scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, and Remotion package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
