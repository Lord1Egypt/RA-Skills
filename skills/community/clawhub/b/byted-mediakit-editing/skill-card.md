## Description:

This skill guides agents in using MediaKit CLI editing commands for audio and video trimming, concatenation, mixing, subtitles, filters, speed changes, and media composition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcvnebot](https://clawhub.ai/user/volcvnebot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to have an agent prepare MediaKit CLI commands for common media-editing workflows, including audio/video composition, format-preserving edits, asynchronous task submission, and task-result lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud processing can send media inputs, URLs, and authenticated MediaKit requests to the selected MediaKit processing mode.

Mitigation: Prefer local mode for private media when supported, avoid sensitive or internal URLs unless intended, and verify the CLI package before use.

Risk: Credential handling can expose API keys if secrets are pasted directly into shell commands or saved in shell history.

Mitigation: Use environment variables or the MediaKit configuration file for credentials, and avoid placing real API keys directly in commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcvnebot/skills/byted-mediakit-editing)
- [MediaKit shared rules](reference/shared.md)
- [Add image to video](reference/add-image-to-video.md)
- [Add subtitle to video](reference/add-subtitle-to-video.md)
- [Adjust audio speed](reference/adjust-audio-speed.md)
- [Adjust video speed](reference/adjust-video-speed.md)
- [Adjust video volume](reference/adjust-video-volume.md)
- [Apply video filter](reference/apply-video-filter.md)
- [Concatenate audio](reference/concat-audio.md)
- [Concatenate video](reference/concat-video.md)
- [Extract audio](reference/extract-audio.md)
- [Fade audio](reference/fade-audio.md)
- [Fade video audio](reference/fade-video-audio.md)
- [Flip video](reference/flip-video.md)
- [Image to video](reference/image-to-video.md)
- [Mix audio](reference/mix-audio.md)
- [Mux audio and video](reference/mux-audio-video.md)
- [Trim audio](reference/trim-audio.md)
- [Trim video](reference/trim-video.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with mediakit-cli shell commands and JSON task-response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands commonly submit asynchronous MediaKit tasks that return task_id and request_id, followed by result lookup with mediakit-cli shared query-task.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
