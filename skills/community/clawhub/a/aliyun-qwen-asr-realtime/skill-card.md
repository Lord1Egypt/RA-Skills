## Description:

Use when low-latency realtime speech recognition is needed with Alibaba Cloud Model Studio Qwen ASR Realtime models, including streaming microphone input, live captions, or duplex voice agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure low-latency Alibaba Cloud Qwen ASR Realtime speech recognition for streaming microphones, live captions, browser or terminal clients, and duplex voice-agent input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Realtime ASR workflows may expose sensitive audio, transcripts, or Alibaba Cloud credentials if outputs or debug logs are stored in shared locations.

Mitigation: Keep DASHSCOPE_API_KEY and Alibaba Cloud credentials out of source control, avoid saving sensitive audio or transcripts in shared workspaces, and remove debug output after it is no longer needed.

## Reference(s):

- [Artifact source list](references/sources.md)
- [Alibaba Cloud Qwen ASR Realtime documentation](https://help.aliyun.com/document_detail/2976098.html)
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-qwen-asr-realtime)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, json]

**Output Format:** [Markdown guidance with inline shell commands and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write sample realtime ASR request payloads under output/aliyun-qwen-asr-realtime/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
