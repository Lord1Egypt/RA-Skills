## Description: <br>
When given a Bilibili URL, BV ID, or b23.tv short link, this skill uses yt-dlp to collect video metadata, prefers official subtitles, and can download audio for SiliconFlow ASR transcription before producing a transcript and summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaa-ljpcoder](https://clawhub.ai/user/aaa-ljpcoder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn Bilibili videos into readable transcripts and concise summaries. It is intended for workflows where official subtitles are preferred and ASR is used only when subtitles are unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video audio may be sent to SiliconFlow for transcription when official subtitles are unavailable. <br>
Mitigation: Use the skill only for videos whose audio may be shared with SiliconFlow, avoid private or sensitive content, and confirm ASR use before running transcription. <br>
Risk: The scanner flagged shell command construction around user-provided URLs. <br>
Mitigation: Review URLs before execution and prefer a revised implementation that passes command arguments through safe spawn-style APIs. <br>
Risk: The workflow requires a sensitive SiliconFlow API key. <br>
Mitigation: Provide the key through the environment or a secret store, avoid placing it in prompts or logs, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaa-ljpcoder/bilibili-ytdlp-summary) <br>
- [Publisher profile](https://clawhub.ai/user/aaa-ljpcoder) <br>
- [SiliconFlow API key setup](https://cloud.siliconflow.cn/me/account/ak) <br>
- [yt-dlp project](https://github.com/yt-dlp/yt-dlp) <br>
- [Original ClawHub skill referenced by artifact](https://clawhub.ai/Markusbetter/bilibili-video-transcribe-summary) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Console JSON plus generated Markdown, text, and JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes summary.md, transcript.txt, probe_result.json, and when ASR runs transcription_result.json; downloaded audio is deleted after successful transcription.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
