## Description:

Extracts transcript text or captions from Douyin, TikTok, YouTube, Xiaohongshu, and similar short-video links through the Videosays CLI and service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xwchris](https://clawhub.ai/user/xwchris)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to transcribe supported short-video sharing links, query Videosays balance, or review transcription history. It is intended for videos the user owns, created, or is otherwise authorized to process.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs an unpinned npm CLI that can access the saved Videosays API key and local environment.

Mitigation: Use a pinned and reviewed videosays version or a locked local install, and run it with least privilege.

Risk: Video links and the Videosays API key are sent to the Videosays service for transcription.

Mitigation: Confirm this data flow is acceptable before use and process only videos the user owns, created, or is authorized to handle.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xwchris/skills/douyin-to-text)
- [Videosays website](https://videosays.com/zh?utm_source=dy_caption_skill&utm_medium=agent_skill&utm_campaign=douyin_to_text_skill)
- [Videosays API documentation](https://videosays.com/zh/docs?utm_source=dy_caption_skill&utm_medium=agent_skill&utm_campaign=douyin_to_text_skill&utm_content=api_docs)
- [videosays npm package](https://www.npmjs.com/package/videosays)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and returned transcript text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18 or newer and sends video links plus a Videosays API key to the Videosays service when used.]

## Skill Version(s):

1.1.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
