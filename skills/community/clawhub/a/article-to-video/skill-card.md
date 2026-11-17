## Description:

Converts articles (docx/pdf/txt/md) to narrated videos with AI-generated visuals and TTS voiceover.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unique-memory](https://clawhub.ai/user/unique-memory)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and developers use this skill to turn uploaded articles or documents into narrated video packages with generated slides, speech, subtitles, and background music.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local cleanup and background-music management can delete files outside the intended output set.

Mitigation: Run the skill only in a contained workspace, review output directories before execution, avoid untrusted filenames and paths, and treat BGM removal operations as administrative actions.

Risk: The skill performs local media generation with document parsing, TTS, FFmpeg processing, generated images, subtitles, background music, and temporary files.

Mitigation: Grant only the filesystem access needed for the current conversion job and review generated manifests, media paths, and final outputs before publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/unique-memory/skills/article-to-video)
- [ClawHub Publisher Profile](https://clawhub.ai/user/unique-memory)
- [Source Homepage](https://github.com/unique-memory/article-to-video)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON manifests, shell commands, generated media files, subtitles, and configuration outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scenes.json, timing.json, slide images, optional ai_image_requests.json, MP4 video, SRT subtitles, thumbnail image, and progress files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
