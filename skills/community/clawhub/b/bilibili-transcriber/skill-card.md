## Description:

Transcribes Bilibili videos from URLs or BV IDs using Bilibili captions first, then Alibaba DashScope Paraformer cloud transcription or local faster-whisper, and produces timestamped transcript text plus structured Markdown summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guorui303](https://clawhub.ai/user/guorui303)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content analysts, and other agent users use this skill to convert Bilibili videos into timestamped transcripts and concise structured summaries. It is aimed at Chinese-language video review, study, and note-taking workflows where captions may be unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud transcription mode can upload local audio to Alibaba DashScope/OSS.

Mitigation: Use cloud mode only for audio that is approved for external processing; force local faster-whisper transcription for sensitive videos.

Risk: The skill can fall back from DASHSCOPE_API_KEY to OPENAI_API_KEY for Alibaba-compatible requests.

Mitigation: Remove or avoid the OPENAI_API_KEY fallback and set DASHSCOPE_API_KEY only when intentionally using DashScope.

Risk: Unpinned dependencies and model downloads can change behavior across installations.

Mitigation: Pin Python dependencies and model revisions before deployment.

Risk: Arbitrary video URLs can trigger remote fetching and local audio processing.

Mitigation: Limit use to trusted Bilibili URLs or BV IDs and review requested sources before transcription.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guorui303/skills/bilibili-transcriber)
- [Publisher profile](https://clawhub.ai/user/guorui303)
- [Bilibili player subtitle API](https://api.bilibili.com/x/player/wbi/v2?cid={cid}&bvid={bvid})
- [Alibaba Bailian console](https://bailian.console.aliyun.com/)
- [DashScope uploads API](https://dashscope.aliyuncs.com/api/v1/uploads)
- [HF Mirror](https://hf-mirror.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with transcript text, timestamped segments, summary sections, and optional inline shell or Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save longer summaries as Markdown files in the user's workspace when requested or when content is long.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
