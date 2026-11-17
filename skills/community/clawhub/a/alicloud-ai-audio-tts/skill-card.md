## Description:

Generate human-like speech audio with Model Studio DashScope Qwen TTS models (qwen3-tts-flash, qwen3-tts-instruct-flash). Use when converting text to speech, producing voice lines for short drama/news videos, or documenting TTS request/response fields for DashScope.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content production teams use this skill to generate Alibaba Cloud DashScope Qwen TTS audio from text, prepare request payloads, and understand non-streaming and streaming response fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Request data can change the API endpoint before the DashScope API key is used, which could expose the key and submitted text.

Mitigation: Use only trusted request files, avoid any base_url override, and run with a tightly scoped DashScope API key.

Risk: Generated request and audio artifacts can contain private text or voice content.

Mitigation: Keep outputs in a dedicated directory and delete saved request or audio artifacts that contain sensitive content.

Risk: Unpinned SDK dependencies can change behavior over time.

Mitigation: Pin the DashScope SDK version before operational use.

## Reference(s):

- [DashScope SDK Reference (Qwen TTS)](artifact/references/api_reference.md)
- [Official documentation source list](artifact/references/sources.md)
- [DashScope API endpoint](https://dashscope.aliyuncs.com/api/v1)
- [DashScope international API endpoint](https://dashscope-intl.aliyuncs.com/api/v1)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash and Python snippets, plus generated audio files and optional JSON response data when the helper script is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DashScope API key; generated audio defaults to output/ai-audio-tts/audio/.]

## Skill Version(s):

1.0.4 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
