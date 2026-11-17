## Description:

Extracts text or subtitles from Douyin, TikTok, YouTube, Xiaohongshu, and similar short-video share links using the Videosays service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xwchris](https://clawhub.ai/user/xwchris)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to transcribe supported short-video share links, check Videosays credit balance, and review transcription history. It is useful when a user provides a video link and wants readable captions or transcript text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm package at runtime.

Mitigation: Prefer a pinned, reviewed videosays package version or a lockfile-managed local install before use in sensitive environments.

Risk: The transcription flow sends API keys and video links to the Videosays service.

Mitigation: Use a least-privileged environment, process only videos the user is authorized to handle, and avoid submitting confidential links unless the Videosays service is approved for that data.

## Reference(s):

- [Videosays website](https://videosays.com/zh?utm_source=dy_caption_skill&utm_medium=agent_skill&utm_campaign=douyin_to_text_skill)
- [Videosays API documentation](https://videosays.com/zh/docs?utm_source=dy_caption_skill&utm_medium=agent_skill&utm_campaign=douyin_to_text_skill&utm_content=api_docs)
- [videosays npm package](https://www.npmjs.com/package/videosays)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and transcript text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include setup guidance, transcription results, account balance, or transcription history returned by Videosays.]

## Skill Version(s):

1.1.3 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
