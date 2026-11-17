## Description:

Converts Bilibili video links into Chinese transcript text and interactive HTML analysis reports, preferring available CC subtitles and falling back to local faster-whisper transcription when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouq2039-lang](https://clawhub.ai/user/zhouq2039-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content analysts, and agents use this skill to turn provided Bilibili links or BV IDs into readable transcripts and HTML reports for video review, summarization, and content analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound URL handling may contact non-Bilibili or internal network addresses despite the stated network boundary.

Mitigation: Use trusted full bilibili.com/video/BV... URLs, avoid short links when possible, review network access before execution, and run the skill in a constrained environment.

Risk: The skill downloads Python dependencies or Whisper model files and writes transcript and HTML outputs locally.

Mitigation: Install only where outbound model downloads are acceptable, consider pinning faster-whisper before use, and direct outputs to a controlled directory.

Risk: Generated transcripts and reports can contain sensitive video content and metadata.

Mitigation: Use non-sensitive videos in shared or monitored environments, keep the default transcript preview behavior, and store outputs in an access-controlled location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouq2039-lang/skills/bilibili-video-parser-2)
- [Publisher profile](https://clawhub.ai/user/zhouq2039-lang)
- [Bilibili video metadata endpoint](https://api.bilibili.com/x/web-interface/view?bvid={bvid})

## Skill Output:

**Output Type(s):** [Text, HTML, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated artifacts are plain text transcripts, JSON analysis, and standalone HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written locally; terminal output defaults to a 500-character transcript preview unless full printing is requested.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
