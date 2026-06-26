## Description: <br>
Bilibili Transcriber helps an agent retrieve Bilibili subtitles or transcribe downloaded audio with cloud Paraformer or local Whisper, then produce timestamped Markdown summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guorui303](https://clawhub.ai/user/guorui303) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn Bilibili URLs or BV identifiers into transcript text, timestamped notes, and structured Markdown summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud transcription mode can upload media to Alibaba DashScope, and the documentation conflicts about whether processing is fully local. <br>
Mitigation: Use local Whisper mode for sensitive or private videos and review any run without official subtitles before allowing audio upload. <br>
Risk: The skill can use OPENAI_API_KEY as a fallback credential for DashScope-compatible access, which may expose an unrelated environment credential. <br>
Mitigation: Prefer a dedicated DASHSCOPE_API_KEY and avoid exposing unrelated API keys in the execution environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/guorui303/bilibili-transcriber) <br>
- [Bilibili player subtitle API endpoint](https://api.bilibili.com/x/player/wbi/v2?cid={cid}&bvid={bvid}) <br>
- [Alibaba Bailian console](https://bailian.console.aliyun.com/) <br>
- [DashScope upload API endpoint](https://dashscope.aliyuncs.com/api/v1/uploads) <br>
- [HF Mirror](https://hf-mirror.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with transcript text, timestamped sections, summaries, and inline command or code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save long summaries as Markdown files in the user's workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
