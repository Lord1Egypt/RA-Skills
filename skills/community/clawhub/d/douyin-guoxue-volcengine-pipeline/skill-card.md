## Description:

Create and publish Chinese metaphysics, guoxue, and I Ching short videos for Douyin using Volcengine image and video generation, Edge TTS dubbing, ffmpeg stitching, Douyin publishing, and backend verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinhuadeng](https://clawhub.ai/user/jinhuadeng)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and operators use this skill to generate reusable three-shot 9:16 Douyin guoxue videos, assemble voiceover and subtitles, publish them, and verify the posted result in the creator backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can publish public Douyin content from the user's account.

Mitigation: Require explicit user approval after showing the final video, title, target account, AI-content declaration status, and backend verification plan before any publish step.

Risk: A script success message may not prove that the content was actually posted or declared as AI-generated.

Mitigation: Verify the creator backend after publishing and report the posted item, timestamp, duration, title snippet, and AI-content declaration status.

## Reference(s):

- [Prompt Patterns](references/prompt-patterns.md)
- [Publish Notes](references/publish-notes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration paths, prompt patterns, and publishing checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to produce local video assets, publish metadata, backend verification results, and AI-content declaration status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
