## Description: <br>
Use when low-latency realtime speech recognition is needed with Alibaba Cloud Model Studio Qwen ASR Realtime models, including streaming microphone input, live captions, or duplex voice agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare realtime ASR request payloads and operational guidance for Alibaba Cloud Model Studio Qwen ASR Realtime models in captioning, streaming speech-to-text, and duplex voice-agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved ASR samples, transcripts, response samples, or metadata may contain sensitive speech content. <br>
Mitigation: Protect or delete files written under output/alicloud-ai-audio-asr-realtime/ before sharing or committing them. <br>
Risk: Using Alibaba Cloud realtime ASR requires Alibaba Cloud credentials. <br>
Mitigation: Use environment-based credential handling such as DASHSCOPE_API_KEY and avoid embedding credentials in generated payloads or committed files. <br>


## Reference(s): <br>
- [Sources](references/sources.md) <br>
- [Alibaba Cloud Model Studio ASR Realtime Documentation](https://help.aliyun.com/document_detail/2976098.html) <br>
- [Alibaba Cloud Model Studio Newly Released Models](https://help.aliyun.com/zh/model-studio/newly-released-models) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON request templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write JSON request payloads under output/alicloud-ai-audio-asr-realtime/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
