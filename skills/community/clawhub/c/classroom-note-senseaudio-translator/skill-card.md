## Description:

接收课堂录音、讲座音频或视频文件（视频会先抽取音轨），调用 SenseAudio HTTP ASR API 进行英文转录，可选直出中文翻译；随后整理为结构化 Markdown 学习笔记，包含摘要、关键概念、术语表、时间轴与复习问题，生成到桌面，并支持导出到 Notion 或保存到 Obsidian vault。

This skill is ready for commercial/non-commercial use.

## Publisher:

[klilyz](https://clawhub.ai/user/klilyz)

### License/Terms of Use:

MIT-0

## Use Case:

Students, researchers, educators, and other external users can use this skill to turn English classroom recordings, lecture videos, meeting audio, or media linked from a web page into Chinese study notes. It is intended for transcription, optional bilingual translation, summarization, review materials, and optional export to Notion or an Obsidian vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recordings and generated notes may be uploaded to configured transcription, summarization, or export services.

Mitigation: Use the skill only with content approved for those services, review service terms, and keep API tokens scoped and private.

Risk: Page URL input can trigger broad network fetching before transcription.

Mitigation: Prefer trusted local audio or video files; avoid untrusted page URLs unless the source is known and expected.

Risk: The skill writes transcript, summary, bilingual text, and optional Obsidian files to user-specified locations.

Mitigation: Use a limited output directory or test Obsidian vault first, and skip Obsidian export when vault writes are not desired.

Risk: Custom OpenAI-compatible summarization endpoints can send generated notes to a non-default service.

Mitigation: Use only OpenAI-compatible base URLs that you control or trust, or keep the local summary provider.

## Reference(s):

- [SenseAudio HTTP ASR API documentation](https://senseaudio.cn/docs/speech_recognition/http_api)
- [ClawHub skill page](https://clawhub.ai/klilyz/skills/classroom-note-senseaudio-translator)
- [Setup and usage reference](references/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; generated files include JSON transcript, Markdown summary, and bilingual text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May optionally create a Notion page or write Markdown into an Obsidian vault when configured.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
