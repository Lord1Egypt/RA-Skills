## Description:

专业对话稿生成助手。把视频/音频转成【带说话人标注】的专业对话稿——区分谁说的、Clean Verbatim 可读性重排、金句高亮、公众号可直接粘贴。支持 B 站视频作为输入源（下载音频、查询信息），适用于访谈、播客、会议等多人对话场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shengbinxu](https://clawhub.ai/user/shengbinxu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to download public Bilibili audio, run speaker-diarized ASR, and turn interviews, podcasts, meetings, or other multi-speaker recordings into readable transcript files. It also guides clean-verbatim editing, quote highlighting, and WeChat-compatible HTML formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio is uploaded to Tencent Cloud ASR through COS, which can expose private or regulated recordings to a third-party cloud service.

Mitigation: Use only non-sensitive or explicitly approved-for-cloud audio, and delete COS objects after ASR processing completes.

Risk: The workflow requires Tencent Cloud credentials and can read them from environment variables or a local configuration file.

Mitigation: Use least-privilege Tencent credentials, prefer environment variables, do not store SecretKey in the skill directory, and rotate or disable exposed keys after use.

Risk: Initialization and ASR setup may install Python dependencies or call external services.

Mitigation: Review the artifact before installing and run dependency installation in an isolated environment.

Risk: Transcript and intermediate files can contain sensitive speech content and may be written to disk.

Mitigation: Restrict outputs to a known workspace path, avoid system temporary directories for durable work, and remove transcript artifacts when no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shengbinxu/skills/bilibili-subtitle)
- [ClawHub publisher profile](https://clawhub.ai/user/shengbinxu)
- [Bilibili video info API](https://api.bilibili.com/x/web-interface/view)
- [Bilibili player API](https://api.bilibili.com/x/player/playurl)
- [Tencent Cloud API key management](https://console.cloud.tencent.com/cam/capi)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON command responses, plain-text transcripts, JSON ASR detail files, and HTML transcript files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local audio files, Tencent ASR result JSON, speaker-labeled dialogue text, and styled HTML suitable for WeChat public-account editors.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
