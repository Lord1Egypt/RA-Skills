## Description: <br>
抖音视频智能助手可从抖音链接或本地视频文件提取音频，生成中文转录，并按用户意图输出摘要、逐字稿、归档内容或讨论分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[junweiren98-rgb](https://clawhub.ai/user/junweiren98-rgb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to turn Douyin links, Douyin share text, or local video files into transcripts, summaries, knowledge-base notes, or discussion analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio and transcript content may be sent to third-party Groq or OpenAI services for transcription and formatting. <br>
Mitigation: Use the skill only with content appropriate for third-party processing, and avoid sensitive or private videos unless the user accepts where audio and text will be sent. <br>
Risk: The first-use flow can ask for API keys in chat. <br>
Mitigation: Configure keys through a local .env file, secure environment, or secret store instead of pasting secrets into chat; rotate any exposed key. <br>
Risk: The workflow relies on browser-based Douyin access, local command execution, and local transcript storage. <br>
Mitigation: Review command execution and output paths before use, run in a trusted workspace, and keep generated transcript directories scoped to the intended project. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/junweiren98-rgb/douyin-transcribe-skill) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Groq](https://groq.com) <br>
- [FFmpeg](https://ffmpeg.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown summaries, transcripts, analysis, and saved .md transcript or archive files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save transcripts under douyin-transcripts/ and archive notes under douyin-knowledge/; setup requires ffmpeg and a Groq or OpenAI API key.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
