## Description:

End-to-end AI video generation - create videos from text prompts using image generation, video synthesis, voice-over, and editing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate short videos from text prompts, optionally adding voice-over narration and assembling images, video clips, and audio with FFmpeg.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, narration text, local media paths, and generated assets may be sent to configured third-party AI providers.

Mitigation: Avoid sensitive or regulated input, review provider terms before use, and configure API keys only for providers approved for the intended content.

Risk: The Runway video option is implemented as a fallback to LumaAI in this release.

Mitigation: Treat Runway selection as unavailable until the implementation is corrected, and verify which provider receives each request before production use.

Risk: FFmpeg helpers process local filenames and media paths.

Mitigation: Run the helpers in trusted directories with trusted filenames and validate media inputs before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/ai-video-gen-cn)
- [OpenAI Platform](https://platform.openai.com)
- [Luma Labs](https://lumalabs.ai)
- [Runway](https://runwayml.com)
- [ElevenLabs](https://elevenlabs.io)
- [Replicate](https://replicate.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and generated media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local image, audio, and MP4 video assets through configured AI providers and FFmpeg.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact _meta.json, and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
