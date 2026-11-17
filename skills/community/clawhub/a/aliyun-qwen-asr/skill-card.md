## Description:

Transcribes recorded audio with Alibaba Cloud Model Studio Qwen ASR models and helps generate timestamped transcripts and document DashScope/OpenAI-compatible request and response fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external teams use this skill to transcribe recorded audio files with Alibaba Cloud Qwen ASR, covering sync short-audio calls and async long-file transcription workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive audio and transcript data may be sent to Alibaba Cloud or persisted locally.

Mitigation: Use only audio that is approved for Alibaba Cloud processing, write outputs to controlled directories, and clean up transcripts when retention is no longer needed.

Risk: Async result retrieval follows a provider result URL that server security evidence says is not allowlisted.

Mitigation: Prefer a release that allowlists provider result URLs before using async wait mode, or review result URLs before retrieval.

Risk: The helper can read stored DashScope credentials from the environment, .env files, or Alibaba Cloud credential files.

Mitigation: Limit credential file access, use least-privilege API keys, and avoid running the helper in workspaces containing unrelated secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-qwen-asr)
- [Qwen ASR API notes](references/api_reference.md)
- [Official Alibaba Cloud source links](references/sources.md)
- [Recorded Speech Recognition - Qwen](https://help.aliyun.com/zh/model-studio/recorded-speech-recognition-qwen)
- [Qwen ASR API Reference](https://help.aliyun.com/zh/model-studio/qwen-asr)
- [Qwen ASR File Transcription API Reference](https://help.aliyun.com/zh/model-studio/qwen-asr-filetrans-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl examples, Python helper commands, and JSON transcript outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normalized outputs include transcript text, optional task ID, status, and raw provider response.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
