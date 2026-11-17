## Description:

Helps an agent obtain Bilibili video subtitles, transcribe speech when subtitles are unavailable, summarize content, and prepare structured Feishu documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adolescen-he](https://clawhub.ai/user/adolescen-he)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to process Bilibili video links into reliable subtitles, summaries, comments, and Feishu-ready Markdown. It is intended for workflows that need signed Bilibili subtitle retrieval, fallback transcription, and documented handling of long or subtitle-less videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Bilibili session cookies.

Mitigation: Run it in an isolated environment, use a low-privilege Bilibili account, restrict cookie file permissions, and remove redundant cookie backups when they are not needed.

Risk: Generated transcripts and comments may be published to Feishu when lark-cli is available.

Mitigation: Disable or remove Feishu publishing unless required, and review transcript content and destination permissions before publishing.

Risk: Runtime behavior depends on external Bilibili APIs, subtitle availability, local transcription engines, ffmpeg, and optional lark-cli tooling.

Mitigation: Pin dependencies, verify required tools before use, review fallback behavior, and require user approval before downloading video for transcription.

## Reference(s):

- [Series Discovery Reference](references/series-discovery.md)
- [Feishu Wiki API Reference](references/feishu-wiki-api.md)
- [ClawHub Skill Page](https://clawhub.ai/adolescen-he/skills/bilibili-video-transcriber)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON output paths, transcript text, summaries, and Feishu-ready document content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write intermediate subtitle, summary, comment, audio, and transcript files under /tmp paths named for the source video.]

## Skill Version(s):

3.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
