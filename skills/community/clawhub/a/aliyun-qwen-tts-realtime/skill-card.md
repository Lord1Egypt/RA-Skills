## Description:

Provides real-time speech synthesis workflows for Alibaba Cloud Model Studio Qwen TTS Realtime models, including low-latency and instruction-controlled synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and validate low-latency text-to-speech generation with Alibaba Cloud Qwen realtime TTS models. It supports selecting exact realtime model names, providing voice and instruction parameters, and probing SDK/runtime compatibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The TTS workflow can send the API key and synthesis text to a configured endpoint.

Mitigation: Use the official DashScope endpoint, avoid overriding --base-url unless credential use is removed or a strict allowlist is added, and use a narrowly scoped API key.

Risk: Input text is sent to Alibaba Cloud for synthesis.

Mitigation: Do not synthesize confidential text unless sending that text to Alibaba Cloud is intended and approved.

Risk: The demo can write fallback audio files to a user-specified path.

Mitigation: Check the output path before running fallback generation and keep generated artifacts in the documented output directory.

Risk: Runtime behavior depends on the installed dashscope package and SDK compatibility with realtime models.

Mitigation: Pin the dashscope dependency and run the provided strict compatibility probe before relying on realtime output.

## Reference(s):

- [Qwen TTS Realtime documentation](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime)
- [Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-qwen-tts-realtime)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API Calls, Files]

**Output Format:** [Markdown guidance with inline bash commands, JSON response summaries, and optional WAV audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DASHSCOPE_API_KEY or an Alibaba Cloud credentials profile; fallback audio defaults under output/ai-audio-tts-realtime/audio/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
