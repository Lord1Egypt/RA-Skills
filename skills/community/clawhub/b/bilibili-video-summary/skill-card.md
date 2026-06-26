## Description: <br>
Extract and summarize Bilibili videos by fetching subtitles or GPU-transcribed audio, danmaku, comments, and descriptions into structured outputs for AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gkd2323c](https://clawhub.ai/user/gkd2323c) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to extract Bilibili video transcripts, metadata, danmaku, and comments, then compose a concise summary or deeper content analysis. It is useful when the agent needs local video evidence before summarizing Chinese video content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow runs local Python, yt-dlp, and optionally whisper.cpp binaries and model files. <br>
Mitigation: Install dependencies from trusted sources and use trusted whisper.cpp binaries and models before executing the skill. <br>
Risk: The workflow stores transcripts, danmaku, comments, and video metadata in local output files. <br>
Mitigation: Use a non-sensitive output directory and delete bili-output files when the stored transcript or community data is no longer needed. <br>
Risk: Inputs that are not Bilibili videos or videos that require login, payment, or unrestricted API access may fail or return incomplete data. <br>
Mitigation: Confirm the input is a Bilibili video and treat restricted, rate-limited, or partial outputs as incomplete evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gkd2323c/bilibili-video-summary) <br>
- [Publisher profile](https://clawhub.ai/user/gkd2323c) <br>
- [Project homepage](https://github.com/gkd2323c/bili-summary) <br>
- [whisper.cpp releases](https://github.com/ggerganov/whisper.cpp/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples plus local JSON and transcript files produced by the extraction script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The extraction workflow writes transcript.txt, danmaku.json, and comments.json to the configured output directory; JSON previews may truncate long transcript text.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
