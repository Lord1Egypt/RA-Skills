## Description:

Converts Douyin video links into Chinese transcripts and a structured interactive HTML analysis report using local Whisper transcription and rule-based analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouq2039-lang](https://clawhub.ai/user/zhouq2039-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and analysts use this skill to turn user-provided Douyin video URLs into timestamped transcripts, readable transcript text, and a local HTML report with summaries, quotes, structure, and content judgments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads video content, downloads or loads a Whisper model, opens a headless browser fallback, and writes transcript and report files locally.

Mitigation: Run it only for user-provided Douyin links, use a dedicated output directory, and execute it in an isolated virtual environment with reviewed dependencies.

Risk: Transcripts, video titles, URLs, and generated reports may contain sensitive content and can persist in local files or terminal logs.

Mitigation: Avoid privacy-sensitive videos on shared or monitored machines, control output with --out-dir, and use the default limited terminal preview unless full transcript printing is required.

Risk: Local Whisper transcription and rule-based report extraction can produce errors, especially for long videos or Chinese wording.

Mitigation: Review generated transcripts and report conclusions before reuse, and choose a larger Whisper model when accuracy matters more than speed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhouq2039-lang/skills/douyin-video-parser)
- [ClawHub publisher profile](https://clawhub.ai/user/zhouq2039-lang)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands plus generated TXT transcript files and a single-file HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include timestamped and continuous transcripts, a local interactive HTML report, and an optional terminal transcript preview.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
