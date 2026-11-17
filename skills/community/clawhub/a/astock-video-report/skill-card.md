## Description:

Generates daily A-share market recap videos by pulling market data and news, analyzing likely drivers, creating slides, and composing an MP4 video with a cover image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddiexux](https://clawhub.ai/user/eddiexux)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create daily or intraday China A-share recap videos, cover images, and social posting copy from market data, market news, and AI attribution analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path installs unpinned Python dependencies and external skills, expanding the local trusted code base.

Mitigation: Run setup only in an isolated virtual environment or disposable workspace, and pin and review dependencies before operational use.

Risk: The skill downloads mutable remote assets for fonts and background music.

Mitigation: Prefetch assets from trusted sources, record hashes, and replace the default assets with reviewed local copies where reproducibility matters.

Risk: Generated reports include mandatory promotional slides and hashtags.

Mitigation: Review generated slides and copy before publication, and remove or edit promotional content that does not fit the publisher's requirements.

## Reference(s):

- [行情数据字段说明](artifact/references/data-schema.md)
- [发布文案生成规范](artifact/references/copywriting.md)
- [Pixabay Music](https://pixabay.com/music/)
- [Google Noto Sans SC](https://fonts.google.com/noto/specimen/Noto+Sans+SC)
- [FFmpeg Downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown-style status text plus generated PNG slides, MP4 video, JPG cover image, and social posting copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before video synthesis; financial content is marked as reference-only and not investment advice.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
