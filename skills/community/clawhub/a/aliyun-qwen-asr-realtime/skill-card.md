## Description: <br>
Use when low-latency realtime speech recognition is needed with Alibaba Cloud Model Studio Qwen ASR Realtime models, including streaming microphone input, live captions, or duplex voice agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare and operate realtime speech-to-text requests for Alibaba Cloud Model Studio Qwen ASR Realtime models, including live captions, streaming microphone input, and duplex voice-agent input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill requires an Alibaba Cloud/DashScope API key and may send audio-related data through the user's own client. <br>
Mitigation: Use only in environments where this cloud dependency is acceptable, keep DASHSCOPE_API_KEY out of generated outputs and logs, and review or delete output/aliyun-qwen-asr-realtime/ files that contain transcripts, payloads, or sensitive session details. <br>


## Reference(s): <br>
- [Artifact sources](references/sources.md) <br>
- [Alibaba Cloud Qwen ASR Realtime documentation](https://help.aliyun.com/document_detail/2976098.html) <br>
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-qwen-asr-realtime) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and generated JSON request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write request templates, session payloads, response samples, and transcripts under output/aliyun-qwen-asr-realtime/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
