## Description:

跨平台内容自动化发布工作流，支持AI原创内容生成、视频制作、自动发布到小红书、抖音等平台，支持国内视频搬运去重后发布到TikTok/YouTube。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiatian5](https://clawhub.ai/user/xiatian5)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, social-media operators, and developers use this skill to generate social-media content, prepare images or video assets, and fill publishing workflows for Xiaohongshu, Douyin, TikTok, and YouTube. It also supports workflow scaffolding for reposting or localizing videos when the user has the right to use the source media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses browser automation with real social-media accounts and saved login sessions.

Mitigation: Use test accounts first, keep saved auth files out of repositories and backups, restrict file permissions, and review account access before installation.

Risk: Video reposting and deduplication workflows can create copyright or platform-policy exposure if source media is not owned or licensed.

Mitigation: Avoid repost workflows unless the user owns or has licensed the media, and manually verify rights and platform compliance before upload.

Risk: Generated uploads or automated posting can publish incorrect, low-quality, or policy-violating content.

Mitigation: Review all generated titles, descriptions, images, videos, tags, and upload settings manually before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiatian5/skills/cross-platform-auto-poster)
- [xiaohongshu-content-automation](https://clawhub.ai/skills/xiaohongshu-content-automation)
- [playwright-browser-automation](https://clawhub.ai/skills/playwright-browser-automation)
- [remotion-video-toolkit](https://clawhub.ai/skills/remotion-video-toolkit)
- [image_generate](https://clawhub.ai/skills/image-generate)
- [FFmpeg downloads](https://ffmpeg.org/download.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with JavaScript and shell snippets, JSON-style workflow results, and generated media or log file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create browser session state files, generated media assets, and JSONL publishing logs under configured auth and output directories.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
