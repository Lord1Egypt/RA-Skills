## Description:

Scrapes Douyin creator videos, downloads audio (Playwright+ffmpeg with yt-dlp fallback), and transcribes with Whisper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gpttang](https://clawhub.ai/user/gpttang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations users use this skill to track Douyin creator accounts, collect recent video metadata, extract audio, and generate Whisper transcripts for review or downstream analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live Douyin session cookies.

Mitigation: Use a dedicated low-risk Douyin account, keep .douyin_cookies.json out of repositories and backups, and avoid --cookies-from-browser unless the account risk is understood.

Risk: The workflow executes external tools and mutable dependencies.

Mitigation: Run the skill in an isolated environment and pin or review MediaCrawler and Python dependencies before using it on important machines.

## Reference(s):

- [Pipeline Reference](references/pipeline.md)
- [Troubleshooting Reference](references/troubleshooting.md)
- [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler)
- [ClawHub skill page](https://clawhub.ai/gpttang/skills/douyin-content-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local data outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces CSV metadata, M4A audio files, Markdown transcript files, and progress report text under OUTPUT_BASE_DIR.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
