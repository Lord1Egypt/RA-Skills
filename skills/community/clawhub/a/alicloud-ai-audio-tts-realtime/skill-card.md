## Description:

Real-time speech synthesis with Alibaba Cloud Model Studio Qwen TTS Realtime models for low-latency interactive and instruction-controlled speech output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and probe Alibaba Cloud Qwen realtime text-to-speech workflows, including low-latency synthesis, instruction-controlled speech, and fallback audio generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The demo script can send the DashScope API key and synthesis text to a user-supplied endpoint.

Mitigation: Use the default Alibaba Cloud endpoint, avoid untrusted --base-url values, and use a narrowly scoped DashScope API key.

Risk: Fallback generation can download audio from URLs returned by the endpoint.

Mitigation: Treat downloaded audio and fallback output paths as untrusted unless the endpoint is known-good.

Risk: .env loading can expose unrelated secrets if broad environment files are used.

Mitigation: Keep only required Alibaba Cloud credentials in the working .env context for this skill.

## Reference(s):

- [Alibaba Cloud Qwen TTS Realtime documentation](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime)
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/alicloud-ai-audio-tts-realtime)
- [ClawHub publisher profile](https://clawhub.ai/user/cinience)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, text]

**Output Format:** [Markdown guidance with inline shell commands and JSON-style response summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local audio files and probe summaries when the demo script is run with valid Alibaba Cloud credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
