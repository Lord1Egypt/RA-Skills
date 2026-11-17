## Description:

Analyzes Bilibili academic/educational videos to extract knowledge points and generate clean-style study notes with screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[railgun9983](https://clawhub.ai/user/railgun9983)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and education-focused analysts use this skill to turn Bilibili academic or educational videos into structured study notes. It supports download, transcription, LLM-based knowledge extraction, screenshot capture, and Markdown report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Bilibili login credentials and downloaded video data.

Mitigation: Install and run it in an isolated environment, avoid using a high-value Bilibili account, and process only videos whose local storage is acceptable.

Risk: Transcript content may be sent to an external LLM during analysis.

Mitigation: Do not process private, confidential, or sensitive videos unless sharing transcript content with the chosen LLM provider is acceptable.

Risk: Security evidence reports unsafe parsing, dependency, and disclosure gaps, including an eval-based parsing issue.

Mitigation: Review dependency versions and fix the eval parsing path before using untrusted media or deploying the skill broadly.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/railgun9983/skills/bilibili-video-analyzer)
- [Best Practices Guide](references/BEST_PRACTICES.md)
- [Quick Quality Checklist](references/QUICK_QUALITY_CHECKLIST.md)
- [References Index](references/README.md)
- [bilibili-dl](https://github.com/railgun9983/bilibili-download)
- [FFmpeg](https://ffmpeg.org/)
- [Whisper](https://github.com/openai/whisper)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown study report with JSON analysis data, generated screenshots, subtitles, and inline shell/Python workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Expected outputs may include local video files, SRT subtitles, transcripts, analysis JSON, screenshots, and a structured learning-notes Markdown file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
