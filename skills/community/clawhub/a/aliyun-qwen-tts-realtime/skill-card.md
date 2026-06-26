## Description: <br>
Use when real-time speech synthesis is needed with Alibaba Cloud Model Studio Qwen TTS Realtime models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure and probe Alibaba Cloud Qwen realtime text-to-speech workflows for low-latency, instruction-controlled speech output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text, voice settings, and instructions are sent to Alibaba DashScope, and fallback audio downloads are provider output. <br>
Mitigation: Use a dedicated or minimally scoped DashScope API key, avoid shared secret files and copied evidence, keep the default endpoint unless another endpoint is intentionally trusted, and choose output paths deliberately. <br>


## Reference(s): <br>
- [Alibaba Cloud Qwen TTS Realtime documentation](https://help.aliyun.com/zh/model-studio/qwen-tts-realtime) <br>
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>
- [Skill source references](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and Python script guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce JSON probe summaries and WAV audio files when the included demo script is executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
