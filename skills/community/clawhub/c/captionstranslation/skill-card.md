## Description:

自动化音视频字幕提取与翻译工具，利用 FFmpeg 和本地 Python 脚本生成双语 SRT。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongym1234](https://clawhub.ai/user/kongym1234)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and media operators use this skill to convert local audio or video files into bilingual Chinese-English SRT subtitle files. The workflow compresses audio locally, sends audio for transcription, translates subtitle segments with a configured LLM provider, and returns the generated subtitle path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio and transcript contents are sent to third-party AI services.

Mitigation: Use only with recordings that are approved for those providers, and confirm provider terms, retention, and data handling before processing sensitive media.

Risk: API credentials are required for transcription and translation providers.

Mitigation: Provide only the needed keys through environment variables in a limited runtime environment, and avoid embedding secrets in files or prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kongym1234/skills/captionstranslation)
- [Groq audio transcription endpoint](https://api.groq.com/openai/v1/audio/transcriptions)
- [Default LLM provider base URL](https://api.deepseek.com/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated SRT file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces source and Chinese-translated SRT files derived from the input audio path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
