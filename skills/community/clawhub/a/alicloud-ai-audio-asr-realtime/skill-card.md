## Description:

Use when low-latency realtime speech recognition is needed with Alibaba Cloud Model Studio Qwen ASR Realtime models, including streaming microphone input, live captions, or duplex voice agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and voice-agent builders use this skill to configure Alibaba Cloud Qwen ASR Realtime sessions for live captions, microphone streaming, and duplex speech-to-text workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alibaba Cloud API keys may be exposed if credentials are committed or shared.

Mitigation: Keep DASHSCOPE_API_KEY and Alibaba Cloud credentials in local secret storage or environment variables, and do not commit them.

Risk: Saved ASR payloads, transcripts, or response samples may contain sensitive speech content.

Mitigation: Redact or exclude generated output files before publishing repositories or sharing workspaces.

## Reference(s):

- [Artifact sources](references/sources.md)
- [Alibaba Cloud Model Studio Qwen ASR Realtime documentation](https://help.aliyun.com/document_detail/2976098.html)
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with shell commands and JSON request payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local ASR request payloads and response samples under the configured output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
