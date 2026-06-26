## Description: <br>
Extracts subtitles from Bilibili, Douyin, YouTube, Xiaohongshu, and local videos, then produces structured summaries, information-density scores, and optional danmaku, key-frame, diarization, and SRT outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangligong0826](https://clawhub.ai/user/zhangligong0826) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to process supported video links or local video files, extract subtitles or speech transcripts, and generate concise summaries, credibility notes, and information-density ratings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts supported video platforms, runs local media tools, and may keep transcripts or extracted artifacts on disk. <br>
Mitigation: Use it deliberately on private or sensitive videos, review optional batch, frames, danmaku, and diarize flags before running, and remove cached media or transcript artifacts when they are no longer needed. <br>
Risk: Credibility assessments about authors or people mentioned in videos may be incomplete or incorrect, especially for medical, legal, or financial topics. <br>
Mitigation: Independently verify identities and claims, and preserve explicit uncertainty warnings when background information cannot be confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangligong0826/bilibili-summarizer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown summaries with JSON, SRT, subtitle text, frame, and local cache artifacts produced by helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May contact supported video platforms, invoke yt-dlp and ffmpeg, run local ASR, and store transcripts, subtitles, audio, or frames on disk.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
