## Description:

Extracts Bilibili video subtitles or GPU-transcribed audio, danmaku, comments, and description data so an agent can summarize the video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gkd2323c](https://clawhub.ai/user/gkd2323c)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to extract transcript, metadata, danmaku, and comment context from Bilibili videos for agent-written summaries. It is useful when an agent needs local extraction and summarization inputs without relying on an external AI API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes outbound requests and accepts video URLs, while security evidence says URL handling is broader than the Bilibili-only purpose requires.

Mitigation: Use explicit Bilibili URLs and run the skill with outbound access constrained to Bilibili and required media hosts.

Risk: The skill invokes local tools such as yt-dlp and whisper.cpp and downloads or converts media files.

Mitigation: Run it in a constrained environment and pin or review yt-dlp, PyAV, whisper.cpp, and model versions before automated use.

Risk: The skill saves transcripts, danmaku, and comments locally, which may include sensitive or copyrighted content.

Mitigation: Keep the output directory private, control retention, and avoid processing content that should not be stored locally.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gkd2323c/skills/bilibili-video-summary)
- [Project Homepage](https://github.com/gkd2323c/bili-summary)
- [whisper.cpp Releases](https://github.com/ggerganov/whisper.cpp/releases)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands; runtime extraction output is JSON plus transcript and community-response files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output directory is ./bili-output/ and includes transcript.txt, danmaku.json, and comments.json when available.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
