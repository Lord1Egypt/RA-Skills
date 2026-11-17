## Description:

Download Bilibili videos, extract or transcribe subtitles, and generate detailed AI-powered summaries with Google Gemini.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lava-chen](https://clawhub.ai/user/lava-chen)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to inspect, download, transcribe, and summarize Bilibili videos through an agent workflow. It is intended for Bilibili URLs where the user wants video metadata, subtitles, transcripts, downloaded media, or a concise summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make network requests to user-provided video URLs and Bilibili APIs.

Mitigation: Avoid private or internal URLs and run the skill in an isolated environment with reviewed dependencies.

Risk: Subtitle or transcript text may be sent to Google Gemini for summarization.

Mitigation: Use the skill only with content approved for external processing and confirm that Gemini use fits the user's data handling requirements.

Risk: The skill depends on a Gemini API key for AI summaries.

Mitigation: Use a restricted API key and provide it through a temporary environment variable or secret manager.

Risk: Downloaded media, subtitles, transcripts, and summaries may remain in the output directory.

Mitigation: Review and clean the output directory after each run, especially when processing non-public or sensitive content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lava-chen/skills/bili-summary)
- [Google AI Studio API keys](https://aistudio.google.com/app/apikey)
- [Gemini 2.5 Flash generateContent endpoint](https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent)
- [Bilibili player subtitle API](https://api.bilibili.com/x/player/wbi/v2?aid={aid}&cid={cid})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with shell commands; generated runtime files may include JSON video metadata, transcript text, summary text, audio, and video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are generated from Bilibili subtitles or faster-whisper transcripts and may be capped by the Gemini request configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
