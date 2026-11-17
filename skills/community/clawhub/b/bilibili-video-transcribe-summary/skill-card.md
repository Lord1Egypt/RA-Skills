## Description:

Transcribes, extracts subtitles from, and summarizes Bilibili videos from standard links, BV IDs, or b23.tv short links, using official subtitles first and SiliconFlow ASR when subtitles are unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markusbetter](https://clawhub.ai/user/markusbetter)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn Bilibili video links into readable transcripts, summaries, or focused analysis. It is useful when a video has official subtitles or when audio can be downloaded and transcribed with a SiliconFlow API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script may make network requests and follow arbitrary URLs instead of limiting requests to Bilibili.

Mitigation: Run it only on trusted Bilibili or b23.tv inputs until URL restrictions and redirect checks are added.

Risk: Audio may be sent to SiliconFlow for transcription when official subtitles are unavailable.

Mitigation: Avoid using it with sensitive or private video content unless sending audio to SiliconFlow is acceptable.

Risk: API keys can be exposed if passed on the command line.

Mitigation: Prefer providing SILICONFLOW_API_KEY through the environment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/markusbetter/skills/bilibili-video-transcribe-summary)
- [SiliconFlow API key page](https://cloud.siliconflow.cn/me/account/ak)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with transcript text, summaries, JSON status output, and inline shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write probe_result.json, transcript.txt, audio.mp3, transcription_result.json, and .skill-ready.json in the selected output directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
