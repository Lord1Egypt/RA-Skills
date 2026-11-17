## Description:

Provides MediaKit CLI video tools for enhancement, video understanding, subtitle removal, scene segmentation, matting, OCR, ASR subtitles, metadata probing, and highlight generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcvnebot](https://clawhub.ai/user/volcvnebot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-operation teams use this skill to call MediaKit video-domain capabilities through mediakit-cli for media analysis, repair, subtitle processing, scene segmentation, matting, and highlight generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Most operations send media to MediaKit cloud services.

Mitigation: Submit only media you are authorized to process; avoid confidential, internal, private, or regulated content unless cloud processing is approved.

Risk: MediaKit API keys are required for cloud mode and may be exposed if pasted directly into commands or stored with weak file permissions.

Mitigation: Use environment variables or a protected secret store for MEDIAKIT_API_KEY, avoid embedding real keys in shell commands, and check permissions on ~/.mediakit/config.json.

Risk: The workflow depends on the third-party @volcengine/mediakit-cli package.

Mitigation: Verify trust in the package before installation and pin or review the version where possible.

## Reference(s):

- [MediaKit Shared Rules](reference/shared.md)
- [Highlight Segment Extraction](reference/analyze-video-highlights.md)
- [Storyline Analysis](reference/analyze-video-storyline.md)
- [ASR Subtitles](reference/asr-subtitles.md)
- [Video Enhancement](reference/enhance-video.md)
- [Generative Video Enhancement](reference/enhance-video-generative.md)
- [Standard Subtitle Removal](reference/erase-video-subtitle.md)
- [Precise Subtitle Removal](reference/erase-video-subtitle-pro.md)
- [Microdrama Highlight Editing](reference/generate-highlights-microdrama.md)
- [Minigame Highlight Editing](reference/generate-highlights-minigame.md)
- [Green Screen Video Matting](reference/matte-greenscreen-video.md)
- [Portrait Video Matting](reference/matte-portrait-video.md)
- [Video Metadata Probing](reference/probe-video-metadata.md)
- [Scene Segmentation](reference/segment-scenes.md)
- [Video OCR](reference/video-ocr.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with mediakit-cli shell commands and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Most video operations are asynchronous and return task_id and request_id values for follow-up query-task polling.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
