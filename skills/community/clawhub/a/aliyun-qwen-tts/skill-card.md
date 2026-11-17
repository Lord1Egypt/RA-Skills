## Description:

Generates human-like speech audio with Alibaba Cloud Model Studio DashScope Qwen TTS models and documents normalized text-to-speech request and response fields.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate speech audio with DashScope Qwen TTS models, produce voice lines for short video or news workflows, and capture request, response, audio, and validation evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A request can select an arbitrary API endpoint while using the user's DashScope API key.

Mitigation: Use only trusted request JSON and remove endpoint selection or allowlist approved DashScope endpoints before using a real API key.

Risk: Remote TTS requests, generated audio links, request payloads, and output files may contain sensitive or regulated content.

Mitigation: Avoid sending secrets or regulated text, store outputs only in approved locations, and clean generated files when sensitive.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cinience/skills/aliyun-qwen-tts)
- [DashScope SDK Reference (Qwen TTS)](references/api_reference.md)
- [Source List](references/sources.md)
- [DashScope API Endpoint](https://dashscope.aliyuncs.com/api/v1)
- [DashScope International API Endpoint](https://dashscope-intl.aliyuncs.com/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell command examples; helper execution may create audio files and JSON response output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce downloaded WAV audio files, temporary audio URLs, request payloads, and validation logs under configured output paths.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
