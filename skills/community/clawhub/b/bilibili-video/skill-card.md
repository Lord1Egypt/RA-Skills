## Description:

Extracts Bilibili video subtitles and audio, using CC subtitles, AI subtitles, then audio download plus ASR transcription as fallback paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqunabc](https://clawhub.ai/user/guoqunabc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to retrieve subtitles, transcripts, or audio from Bilibili videos for downstream summarization, analysis, or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Bilibili session cookies locally and may use them automatically.

Mitigation: Use a sandboxed environment, keep the cookie file private, and delete ~/.openclaw/workspace/.bilibili_cookies.json when authenticated access is no longer needed.

Risk: The audio transcription fallback can run a local speech-to-text.sh script that the security evidence identifies as unverified.

Mitigation: Review that script before enabling ASR, or run extraction with --no-asr when the fallback is not required.

Risk: Downloaded transcripts and audio may remain under /tmp/openclaw/bilibili.

Mitigation: Monitor that directory and remove retained files after use, especially for private, paid, or copyrighted videos.

## Reference(s):

- [Bilibili API Notes](references/api-notes.md)
- [Bilibili](https://www.bilibili.com)
- [ClawHub Skill Page](https://clawhub.ai/guoqunabc/skills/bilibili-video)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown guidance with shell commands and generated transcript or audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes transcript and audio artifacts under /tmp/openclaw/bilibili when extraction succeeds.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
