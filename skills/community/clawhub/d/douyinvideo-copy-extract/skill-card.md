## Description:

Extracts clean transcript-style copy from Douyin, Xiaohongshu, other video links, or local media files, then can generate summaries, rewrites, quotes, shot outlines, translations, and other prompt-directed content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External creators, media teams, and developers use this command skill to turn reviewed video or audio sources into reusable copy, summaries, subtitles, meeting notes, and social-media drafts through the GuaiKei service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan verdict is suspicious because the skill can upload arbitrary local files and fetch arbitrary URLs despite narrower documentation.

Mitigation: Run it only on explicit reviewed media inputs, avoid sensitive local paths or untrusted URLs, and restrict usage in enterprise or cloud environments until validation, size limits, and domain controls are added.

Risk: Video inputs and prompts are sent to the third-party GuaiKei service for transcription and generation.

Mitigation: Confirm publisher and service trust, data-handling terms, token authorization, and user permission before processing confidential or regulated media.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/douyinvideo-copy-extract)
- [Server-resolved source repository](https://github.com/why20261/douyinvideo-copy-extract)
- [GuaiKei service site](https://www.guaikei.com)
- [node-downloader-helper reference](https://github.com/hgouveia/node-downloader-helper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown-style prose on stdout; progress and logs on stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0 or newer and GUAIKEI_API_TOKEN; accepts one media URL, one local media path, or an existing task ID per run.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter and package.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
